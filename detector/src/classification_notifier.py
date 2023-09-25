from utils.events.src.message_clients.rabbitmq import Publisher
from utils.events.src.messages.face_message import FaceMessage
from utils.events.src.messages.marshalling import encode

PUBLISHER_KEY = 'publisher'


class ClassificationNotifier:

    def __init__(self, configuration):
        self.publisher = Publisher.new(**configuration[PUBLISHER_KEY])

    def notify(self, video_chunk, offset, timestamp, face_num, bounding_box, trace):
        message = FaceMessage(video_chunk_id=video_chunk,
                              offset=offset,
                              timestamp=timestamp,
                              face_num=face_num,
                              bounding_box=bounding_box,
                              trace=trace)

        self.publisher.publish(encode(message))
