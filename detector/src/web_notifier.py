from utils.events.src.message_clients.rabbitmq import Publisher
from utils.events.src.messages.detected_face_message import DetectedFaceMessage
from utils.events.src.messages.helper import unwrap_video_chunk_id
from utils.events.src.messages.marshalling import encode
from utils.orm.src import Camera
from utils.orm.src.database import connect
from utils.orm.src.models import Face, VideoChunk

PUBLISHER_KEY = 'publisher'
DATABASE_KEY = 'db'
UNKNOWN = 'UNKNOWN'


class WebNotifier:

    def __init__(self, configuration):
        self.publisher = Publisher.new(**configuration[PUBLISHER_KEY])
        connect(**configuration[DATABASE_KEY])

    def notify(self, video_chunk, offset, timestamp, face_num, bounding_box, trace):
        message = DetectedFaceMessage(video_chunk_id=video_chunk,
                                      offset=offset,
                                      timestamp=timestamp,
                                      face_num=face_num,
                                      name=UNKNOWN,
                                      person_id=-1,
                                      bounding_box=bounding_box,
                                      probability=0.0,
                                      is_match=False,
                                      trace=trace)

        self.publisher.publish(encode(message))

        chunk_camera, chunk_timestamp = unwrap_video_chunk_id(video_chunk)

        camera_query = Camera.select(Camera.id).where(Camera.alias == chunk_camera)
        Face(video_chunk=VideoChunk.select(VideoChunk.id).where((VideoChunk.camera == camera_query) &
                                                                (VideoChunk.timestamp == chunk_timestamp)),
             offset=offset,
             timestamp=timestamp,
             face_num=face_num,
             bounding_box=bounding_box,
             probability=0.0,
             is_match=False).save()
