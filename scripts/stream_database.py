from time import sleep

from peewee import prefetch

from utils.events.src.message_clients.rabbitmq import Publisher
from utils.events.src.messages.detected_face_message import DetectedFaceMessage
from utils.events.src.messages.marshalling import encode
from utils.events.src.messages.video_chunk_message import VideoChunkMessage
from utils.orm.src.models import Camera, Face, Person, VideoChunk
from utils.orm.src.database import connect
from utils.tracing.src.tracer import get_trace_parent, get_tracer

if __name__ == "__main__":
    connect('argus', 'argus', 5432, 'argus', 'panoptes')
    chunk_publisher = Publisher.new('argus', 'argus', 'panoptes', 'argus', 'published_video_chunks')
    face_publisher = Publisher.new('argus', 'argus', 'panoptes', 'argus', 'published_detected_faces')
    tracer = get_tracer('argus', 6831, 'database_streamer')

    chunks_query = VideoChunk.select(VideoChunk, Camera).join(Camera).order_by(VideoChunk.timestamp)
    # faces_query = Face.select(Face, Person).join(Person)
    #
    # chunks_with_faces = prefetch(chunks_query, faces_query)

    sequence_id = 0

    for chunk in chunks_query:
        with tracer.start_as_current_span(f'stream_chunk_{sequence_id}'):
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

        sequence_id += 1
        print(f'Sent {sequence_id} with {len(chunk.faces)}')
        sleep(0.5)
