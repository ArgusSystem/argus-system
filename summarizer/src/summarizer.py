from utils.events.src.messages.marshalling import decode
from utils.events.src.messages.detected_face_message import DetectedFaceMessage
from utils.events.src.messages.helper import get_camera_id
from utils.tracing.src.tracer import get_context, get_tracer, set_span_in_context, get_trace_parent
from utils.orm.src.models import Sighting
from utils.orm.src.models.camera import get_camera
from collections import defaultdict
import bisect
from logging import getLogger

logger = getLogger(__name__)

TIME_START = 0
CAMERA = 1
TIME_END = 2

LAST = -1
FIRST = 0


class Summarizer:
    def __init__(self, tracer_configuration):

        self.sightings_per_person = defaultdict(list, {})
        self.summarize_window = 10 * 1000
        self.extend_sighting_window = 60 * 1000
        self.tracer = get_tracer(**tracer_configuration, service_name='argus-summarizer')
        self.people_traces = {}

    def execute_with(self, message):
        sighting_message: DetectedFaceMessage = decode(DetectedFaceMessage, message)

        if sighting_message.name not in self.people_traces:
            with self.tracer.start_as_current_span(sighting_message.name):
                self.people_traces[sighting_message.name] = get_trace_parent()

        with self.tracer.start_as_current_span('accumulate-sightings', context=get_context(self.people_traces[sighting_message.name])):
            # Prepare sighting record
            sightings = self.sightings_per_person[sighting_message.name]
            sighting_time = sighting_message.timestamp
            sighting_camera = get_camera_id(sighting_message.video_chunk_id)

            # Insert into sightings list like [ start_time, camera_id, end_time==start_time]
            bisect.insort(sightings, [sighting_time, sighting_camera, sighting_time])

        # Check if elapsed time of accumulated data is over the window time
        if sightings[LAST][TIME_START] - sightings[FIRST][TIME_START] > self.summarize_window:

            with self.tracer.start_as_current_span('insert-sightings', context=get_context(self.people_traces[sighting_message.name])):

                # Reduce continuous elements with same CAMERA to only one element
                summarized_sightings = [sightings[FIRST]]
                for sighting in sightings:
                    if sighting[CAMERA] != summarized_sightings[LAST][CAMERA]:
                        summarized_sightings.append(sighting)
                    else:
                        summarized_sightings[LAST][TIME_END] = sighting[TIME_START]

                # Insert summarized sightings into db
                for sighting in summarized_sightings:
                    camera = get_camera(sighting_camera)

                    # If there is a sighting within 'extend_sighting_window' time from this one to the left
                    # extend it
                    extended_a_sighting = False
                    rows = Sighting.select() \
                        .where(Sighting.person == sighting_message.person_id,
                               Sighting.end_time > sighting[TIME_START] - self.extend_sighting_window) \
                        .order_by(Sighting.end_time.desc()) \
                        .limit(1)
                    for closest_sighting_left in rows:
                        if closest_sighting_left.camera == camera: # esto llama una subquery en Camera, evitar?
                            closest_sighting_left.end_time = sighting[TIME_END]
                            closest_sighting_left.save()
                            extended_a_sighting = True

                    # Otherwise, insert as a new sighting
                    if not extended_a_sighting:
                        sighting_db = Sighting(camera=camera,
                                               person=sighting_message.person_id,
                                               start_time=sighting[TIME_START],
                                               end_time=sighting[TIME_END])
                        sighting_db.save()

                # TODO: Send NOTIFICATION

                # Clean local sightings for this person
                self.sightings_per_person[sighting_message.name] = []

        logger.info("Finished - %s", sighting_message)
