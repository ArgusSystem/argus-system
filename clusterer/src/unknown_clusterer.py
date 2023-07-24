from logging import getLogger

from utils.events.src.message_clients.rabbitmq import Publisher
from utils.events.src.messages.matched_face_message import MatchedFaceMessage
from utils.events.src.messages.unknown_face_message import UnknownFaceMessage
from utils.events.src.messages.marshalling import decode, encode
from utils.tracing.src.tracer import get_context, get_trace_parent, get_tracer
import hdbscan
import numpy as np
from utils.orm.src.models import UnknownCluster, UnknownFace

logger = getLogger(__name__)


class UnknownFacesClusterer:

    def __init__(self, faces_batch_size, skip_outliers, publisher_configuration, tracer_configuration):
        self.tracer = get_tracer(**tracer_configuration, service_name='argus-clusterer')
        self.publisher = Publisher.new(**publisher_configuration)

        self.faces_batch = []
        self.faces_batch_size = faces_batch_size

        self.skip_outliers = skip_outliers

    def process(self, message):
        unknown_face_message: UnknownFaceMessage = decode(UnknownFaceMessage, message)

        with self.tracer.start_as_current_span('clusterer', context=get_context(unknown_face_message.trace)):

            with self.tracer.start_as_current_span('accumulate-face'):
                self.faces_batch.append(unknown_face_message)

            logger.info('Added face %s to batch', unknown_face_message)

            if len(self.faces_batch) >= self.faces_batch_size:

                with self.tracer.start_as_current_span('cluster-batch'):
                    encodings = [message.embedding for message in self.faces_batch]
                    # print(encodings)

                    # cluster the embeddings
                    # clt = DBSCAN(eps=0.7, min_samples=20, metric='euclidean', metric_params=None)
                    clt = hdbscan.HDBSCAN()
                    clt.fit(encodings)

                with self.tracer.start_as_current_span('insert-db-results'):
                    # determine the total number of unique faces found in the dataset
                    label_ids = np.unique(clt.labels_)

                    # loop over the unique faces
                    for label_id in label_ids:

                        # skip label 0 consisting of outliers that didn't fit into any cluster
                        if self.skip_outliers and label_id < 0:
                            continue

                        # find all indexes into the faces_batch array that belong to the current label_id
                        batch_idxs = np.where(clt.labels_ == label_id)[0]

                        # insert new unknown faces cluster in db
                        cluster = UnknownCluster()
                        cluster.save()

                        for i in batch_idxs:
                            face_id = self.faces_batch[i].face_id

                            with self.tracer.start_as_current_span(face_id):
                                # insert new unknown face record for each face in this cluster
                                UnknownFace(cluster=cluster.id, face=face_id).save()

                                # Send event to warden
                                trace = get_trace_parent()
                                self.publisher.publish(encode(MatchedFaceMessage(face_id=face_id, trace=trace)))

                self.faces_batch.clear()

                logger.info('Finished processing a batch of %d faces', self.faces_batch_size)
