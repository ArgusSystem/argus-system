
from events.src.messages.face_message import FaceMessage
from utils.events.src.message_clients.rabbitmq import Publisher

from utils.events.src.messages.marshalling import encode

from utils.orm.src.models import BrokenRestriction, Face, Notification, Person, UnknownCluster, UnknownFace, VideoChunk
from utils.orm.src.database import connect
from utils.tracing.src.tracer import get_tracer, get_trace_parent


def clean():
    UnknownFace.truncate_table(restart_identity=True)
    UnknownCluster.truncate_table(restart_identity=True, cascade=True)
    Notification.truncate_table(restart_identity=True)
    BrokenRestriction.truncate_table(restart_identity=True, cascade=True)
    Face.truncate_table(restart_identity=True, cascade=True)


if __name__ == "__main__":
    database = connect('argus', 'argus', 5432, 'argus', 'panoptes')
    face_publisher = Publisher.new('argus', 'argus', 'panoptes', 'argus', 'faces', None)
    tracer = get_tracer('argus', 6831, 'reclassify_faces')

    faces_query = Face.select(Face, Person).join(Person)
    face_messages = []

    for face in faces_query:
        with tracer.start_as_current_span(f'reclassify_face'):
            context = get_trace_parent()
            video_chunk_id = face.video_chunk.camera.alias + "-" + str(face.video_chunk.timestamp)
            message = FaceMessage(video_chunk_id=video_chunk_id,
                                  offset=face.offset,
                                  timestamp=face.timestamp,
                                  face_num=face.face_num,
                                  bounding_box=face.bounding_box,
                                  trace=context)
            face_messages.append(message)

    clean()

    for message in face_messages:
        face_publisher.publish(encode(message))
