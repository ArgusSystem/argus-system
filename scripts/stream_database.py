from time import sleep

from peewee import prefetch

from utils.events.src.message_clients.rabbitmq import Publisher
from utils.events.src.messages.detected_face_message import DetectedFaceMessage
from utils.events.src.messages.marshalling import encode
from utils.events.src.messages.matched_face_message import MatchedFaceMessage
from utils.events.src.messages.unknown_face_message import UnknownFaceMessage
from utils.events.src.messages.video_chunk_message import VideoChunkMessage
from utils.orm.src.models import BrokenRestriction, Camera, Face, Notification, Person, VideoChunk, UnknownCluster, \
    UnknownFace
from utils.orm.src.database import connect
from utils.tracing.src.tracer import get_trace_parent, get_tracer


def clean():
    UnknownFace.truncate_table(restart_identity=True)
    UnknownCluster.truncate_table(restart_identity=True, cascade=True)
    Notification.truncate_table(restart_identity=True)
    BrokenRestriction.truncate_table(restart_identity=True, cascade=True)


if __name__ == "__main__":
    connect('argus', 'argus', 5432, 'argus', 'panoptes')
    chunk_publisher = Publisher.new('argus', 'argus', 'panoptes', 'argus', 'published_video_chunks')
    face_publisher = Publisher.new('argus', 'argus', 'panoptes', 'argus', 'published_detected_faces')
    warden_publisher = Publisher.new('argus', 'argus', 'panoptes', 'argus', 'face_rule_check')
    clusterer_publisher = Publisher.new('argus', 'argus', 'panoptes', 'argus', 'unknown_faces')
    tracer = get_tracer('argus', 6831, 'database_streamer')

    clean()

    chunks_query = VideoChunk.select(VideoChunk, Camera).join(Camera).order_by(VideoChunk.timestamp)
    faces_query = Face.select(Face, Person).join(Person)

    chunks_with_faces = prefetch(chunks_query, faces_query)

    sequence_id = -1
    timestamp = None

    for chunk in chunks_with_faces:
        if timestamp != chunk.timestamp:
            sequence_id += 1
            timestamp = chunk.timestamp
            sleep(0.9)

        with tracer.start_as_current_span(f'stream_chunk'):
            context = get_trace_parent()

            chunk_publisher.publish(encode(VideoChunkMessage(
                camera_id=chunk.camera.alias,
                timestamp=chunk.timestamp,
                trace=context,
                encoding='mp4',
                samples=chunk.samples,
                duration=chunk.duration,
                sequence_id=sequence_id
            )))

            video_chunk_id = f'{chunk.camera.alias}-{chunk.timestamp}'

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

                if face.is_match:
                    matched_face_message = MatchedFaceMessage(face_id=str(face.id), trace=context)
                    warden_publisher.publish(encode(matched_face_message))
                else:
                    unknown_face_message = UnknownFaceMessage(face_id=str(face.id), embedding=face.embedding,
                                                              trace=context)
                    clusterer_publisher.publish(encode(unknown_face_message))

        print(f'Sent {sequence_id} with {len(chunk.faces)}')
