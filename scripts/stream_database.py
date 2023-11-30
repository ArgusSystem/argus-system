from time import sleep, time_ns

from peewee import prefetch

from utils.events.src.message_clients.rabbitmq import Publisher
from utils.events.src.messages.detected_face_message import DetectedFaceMessage
from utils.events.src.messages.marshalling import encode
from utils.events.src.messages.matched_face_message import MatchedFaceMessage
from utils.events.src.messages.video_chunk_message import VideoChunkMessage
from utils.metadata.src.naming.face import to_object_storage_key as face_object_key
from utils.metadata.src.naming.frame import to_object_storage_key as frame_object_key
from utils.metadata.src.naming.video_chunk import to_object_storage_key as video_chunk_object_key
from utils.orm.src.models import BrokenRestriction, Camera, Face, Notification, Person, VideoChunk, UnknownCluster, \
    UnknownFace
from utils.orm.src.database import connect
from utils.tracing.src.tracer import get_trace_parent, get_tracer
from utils.video_storage import StorageFactory, StorageType

ONLY_CLEAN = False


def clean():
    UnknownFace.truncate_table(restart_identity=True)
    UnknownCluster.truncate_table(restart_identity=True, cascade=True)
    Notification.truncate_table(restart_identity=True)
    BrokenRestriction.truncate_table(restart_identity=True, cascade=True)


if __name__ == "__main__":
    database = connect('argus', 'argus', 5432, 'argus', 'panoptes')
    chunk_publisher = Publisher.new('argus', 'argus', 'panoptes', 'argus', 'published_video_chunks')
    face_publisher = Publisher.new('argus', 'argus', 'panoptes', 'argus', 'published_detected_faces')
    warden_publisher = Publisher.new('argus', 'argus', 'panoptes', 'argus', 'face_rule_check')
    tracer = get_tracer('argus', 6831, 'database_streamer')

    storage_factory = StorageFactory('argus', 9500, 'argus', 'panoptes')
    video_chunks_storage = storage_factory.new(StorageType.VIDEO_CHUNKS)
    frame_storage = storage_factory.new(StorageType.VIDEO_FRAMES)
    faces_storage = storage_factory.new(StorageType.FRAME_FACES)

    clean()

    if ONLY_CLEAN:
        exit(0)

    chunks_query = VideoChunk.select(VideoChunk, Camera).join(Camera).order_by(VideoChunk.timestamp)
    faces_query = Face.select(Face, Person).join(Person)

    chunks_with_faces = prefetch(chunks_query, faces_query)

    sequence_id = -1
    last_chunk_timestamp = None
    new_timestamp = (time_ns() // 1_000_000_000) * 1_000
    new_timestamp -= 5 * 1000

    DEBUG_TIME = time_ns()

    for chunk in chunks_with_faces:
        if last_chunk_timestamp != chunk.timestamp:
            sequence_id += 1
            last_chunk_timestamp = chunk.timestamp
            new_timestamp += 1_000  # Assumes that difference between chunk is 1 second
            # sleep(0.25)

            CURRENT_TIME = time_ns()
            print(f'{sequence_id} : {(CURRENT_TIME - DEBUG_TIME) // 1_000_000}')
            DEBUG_TIME = CURRENT_TIME

        with tracer.start_as_current_span(f'stream_chunk'):
            context = get_trace_parent()

            # Update video chunk name in minio
            camera = chunk.camera.alias
            video_chunks_storage.rename(video_chunk_object_key(camera, last_chunk_timestamp),
                                        video_chunk_object_key(camera, new_timestamp))

            # Update timestamp in VideoChunk
            chunk.timestamp = new_timestamp
            chunk.save()

            # Update frame name in minio
            for offset in chunk.samples:
                frame_storage.rename(frame_object_key(camera, last_chunk_timestamp, offset),
                                     frame_object_key(camera, new_timestamp, offset))

            # Update timestamp in Face
            for face in chunk.faces:
                # Update face name in minio
                faces_storage.rename(face_object_key(camera, last_chunk_timestamp, face.offset, face.face_num),
                                     face_object_key(camera, new_timestamp, face.offset, face.face_num))

                face.timestamp = new_timestamp + (face.timestamp - last_chunk_timestamp)
                face.save()

            chunk_publisher.publish(encode(VideoChunkMessage(
                camera_id=camera,
                timestamp=chunk.timestamp,
                trace=context,
                encoding='mp4',
                samples=chunk.samples,
                duration=chunk.duration,
                sequence_id=sequence_id
            )))

            video_chunk_id = f'{camera}-{chunk.timestamp}'

            # Generalize face classification task
            for face in chunk.faces:
                name = 'Unknown'
                person_id = -1

                if face.person:
                    name = face.person.name
                    person_id = face.person.id

                face_publisher.publish(encode(DetectedFaceMessage(video_chunk_id=video_chunk_id,
                                                                  offset=face.offset,
                                                                  timestamp=face.timestamp,
                                                                  face_num=face.face_num,
                                                                  name=name,
                                                                  person_id=person_id,
                                                                  bounding_box=face.bounding_box,
                                                                  probability=face.probability,
                                                                  is_match=face.is_match,
                                                                  trace=context)
                                              ))

                matched_face_message = MatchedFaceMessage(face_id=str(face.id), trace=context)
                warden_publisher.publish(encode(matched_face_message))

        # print(f'Sent {sequence_id} with {len(chunk.faces)}')
