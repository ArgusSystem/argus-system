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
        self.summarize_window = 50 * 1000
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

        # TODO: que tambien corra esto si paso x tiempo. como esta ahora, puede quedar info parcial que nunca se procesa
        # TODO: si la persona no vuelve a aparecer
        # Check if elapsed time of accumulated data is over the window time
        if sightings[LAST][TIME_END] - sightings[FIRST][TIME_START] > self.summarize_window:

            with self.tracer.start_as_current_span('insert-sightings', context=get_context(self.people_traces[sighting_message.name])):

                # Reduce continuous elements with same CAMERA to only one element
                summarized_sightings = [sightings[FIRST]]
                for sighting in sightings:
                    if sighting[CAMERA] != summarized_sightings[LAST][CAMERA] \
                            or summarized_sightings[LAST][TIME_END] < sighting[TIME_START] - self.extend_sighting_window:
                        summarized_sightings.append(sighting)
                    else:
                        summarized_sightings[LAST][TIME_END] = sighting[TIME_START]
                logger.debug("sightings: " + str(sightings))
                logger.debug("summarized sightings" + str(summarized_sightings))

                # Insert summarized sightings into db
                for sighting in summarized_sightings:
                    camera = get_camera(sighting[CAMERA])

                    # If I am fully inside another sighting in the same camera, dont insert
                    rows = Sighting.select() \
                        .where(Sighting.person == sighting_message.person_id,
                               Sighting.start_time <= sighting[TIME_START],
                               Sighting.end_time >= sighting[TIME_END],
                               Sighting.camera == camera) \
                        .limit(1)
                    sighting_containing = None
                    for row in rows:
                        sighting_containing = row
                    if sighting_containing is not None:
                        logger.debug("Skipping sighting contained in: %d", sighting_containing.id)
                        continue

                    # Check if there is a sighting to the left that we need to merge into
                    rows = Sighting.select() \
                        .where(Sighting.person == sighting_message.person_id,
                               sighting[TIME_START] - Sighting.end_time <= self.extend_sighting_window,
                               Sighting.end_time <= sighting[TIME_END],
                               Sighting.start_time <= sighting[TIME_START]) \
                        .order_by(Sighting.end_time.desc()) \
                        .limit(1)
                    closest_sighting_left = None
                    for row in rows:
                        if row.camera == camera:
                            closest_sighting_left = row

                    # Check if there is a sighting to the right that we need to merge into
                    rows = Sighting.select() \
                        .where(Sighting.person == sighting_message.person_id,
                               Sighting.start_time - sighting[TIME_END] <= self.extend_sighting_window,
                               Sighting.end_time >= sighting[TIME_END],
                               Sighting.start_time >= sighting[TIME_START]) \
                        .order_by(Sighting.start_time) \
                        .limit(1)
                    closest_sighting_right = None
                    for row in rows:
                        if row.camera == camera:
                            closest_sighting_right = row

                    final_db_sighting = None
                    # Merge to the left and right. Delete left and extend right's start_time
                    if closest_sighting_left is not None and closest_sighting_right is not None:
                        logger.debug("Merging to the left and right")
                        closest_sighting_right.start_time = closest_sighting_left.start_time
                        sighting[TIME_START] = closest_sighting_right.start_time
                        sighting[TIME_END] = closest_sighting_right.end_time
                        closest_sighting_left.delete()
                        closest_sighting_right.save()
                        final_db_sighting = closest_sighting_right

                    # Merge to the left. Extend db record's end_time
                    elif closest_sighting_left is not None:
                        logger.debug("Merging to the left with: %d", closest_sighting_left.id)
                        closest_sighting_left.end_time = sighting[TIME_END]
                        sighting[TIME_START] = closest_sighting_left.start_time
                        closest_sighting_left.save()
                        final_db_sighting = closest_sighting_left

                    # Merge to the right. Extend db record's start_time
                    elif closest_sighting_right is not None:
                        logger.debug("Merging to the right with: %d", closest_sighting_right.id)
                        closest_sighting_right.start_time = sighting[TIME_START]
                        sighting[TIME_END] = closest_sighting_right.end_time
                        closest_sighting_right.save()
                        final_db_sighting = closest_sighting_right

                    # Otherwise, insert as a new sighting
                    if final_db_sighting is None:
                        final_db_sighting = Sighting(camera=camera,
                                                     person=sighting_message.person_id,
                                                     start_time=sighting[TIME_START],
                                                     end_time=sighting[TIME_END])
                        final_db_sighting.save()

                    # If there are any sightings within this one, delete them
                    rows = Sighting.select() \
                        .where(Sighting.person == sighting_message.person_id,
                               Sighting.start_time >= sighting[TIME_START],
                               Sighting.end_time <= sighting[TIME_END],
                               Sighting.camera == camera)
                    for sighting_inside in rows:
                        if final_db_sighting is None or sighting_inside.id != final_db_sighting.id:
                            logger.debug("Deleting sighting: %d", sighting_inside.id)
                            sighting_inside.delete()

                # TODO: Send NOTIFICATION

                # Clean local sightings for this person
                self.sightings_per_person[sighting_message.name] = []

        logger.info("Finished - %s - person: %s - camera: %s", sighting_message, sighting_message.person_id, sighting_camera)
