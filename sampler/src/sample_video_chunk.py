from big_fiubrother_core import QueueTask
from big_fiubrother_core.utils import image_to_bytes
from cv2 import VideoCapture
import os


class SampleVideoChunk(QueueTask):

    def __init__(self, configuration, input_queue, output_queue):
        super().__init__(input_queue)
        self.output_queue = output_queue
        self.sampling_rate = configuration['sampling_rate']

    def execute_with(self, message):
        cap = VideoCapture(message['path'])
        
        frames = []

        while True:
            ret, frame = cap.read()

            if ret:
                frames.append(frame)
            else:
                break

        os.remove(message['path'])

        step = round(len(frames) / self.sampling_rate)

        messages = []
        
        for i in range(self.sampling_rate):
            offset = i * step

            messages.append({
                'offset': i * step,
                'video_chunk_id': message['video_chunk_id'],
                'payload': image_to_bytes(frames[offset])
            })        

        self.output_queue.put(messages)