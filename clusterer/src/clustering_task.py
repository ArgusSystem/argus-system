from logging import getLogger

from utils.events.src.message_clients.rabbitmq import Publisher
from utils.events.src.messages.matched_face_message import MatchedFaceMessage
from utils.events.src.messages.unknown_face_message import UnknownFaceMessage
from utils.events.src.messages.marshalling import decode, encode
from utils.tracing.src.tracer import get_context, get_trace_parent, get_tracer
from .clustering import fit

from .cluster_storage import ClusterStorage

logger = getLogger(__name__)


class ClusteringTask:

    def __init__(self, faces_batch_size, skip_outliers, publisher_configuration, tracer_configuration):
        self.tracer = get_tracer(**tracer_configuration, service_name='argus-clusterer')
        self.publisher = Publisher.new(**publisher_configuration)

        self.faces_batch = []
        self.faces_batch_size = faces_batch_size

        self.skip_outliers = skip_outliers

    def process(self, message):
        unknown_face_message: UnknownFaceMessage = decode(UnknownFaceMessage, message)

        with self.tracer.start_as_current_span('clusterer', context=get_context(unknown_face_message.trace)):
            self.faces_batch.append(unknown_face_message)
            logger.debug('Added face %s to batch', unknown_face_message)

        if len(self.faces_batch) >= self.faces_batch_size:
            with self.tracer.start_as_current_span('clusterer'):
                with self.tracer.start_as_current_span('process-batch'):
                    encodings = [message.embedding for message in self.faces_batch]
                    clt = fit(encodings)

                cluster_storage = ClusterStorage(self.skip_outliers)

                trace = get_trace_parent()

                with self.tracer.start_as_current_span('store-batch-results'):
                    for face, label in zip(map(lambda f: f.face_id, self.faces_batch), clt.labels_):
                        cluster_storage.store(face, label)
                        self.publisher.publish(encode(MatchedFaceMessage(face_id=face, trace=trace)))

                self.faces_batch.clear()

                logger.debug('Finished processing a batch of %d faces', self.faces_batch_size)
