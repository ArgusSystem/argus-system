from utils.events.src.message_clients.rabbitmq import Publisher
from utils.events.src.messages.detected_face_message import DetectedFaceMessage
from utils.events.src.messages.marshalling import encode

PUBLISHER_KEY = 'publisher'
UNKNOWN = 'UNKNOWN'


class WebNotifier:

    def __init__(self, configuration):
        self.publisher = Publisher.new(**configuration[PUBLISHER_KEY])

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
