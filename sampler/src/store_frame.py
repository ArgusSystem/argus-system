from big_fiubrother_core import QueueTask
from big_fiubrother_core.db import Database, Frame
from big_fiubrother_core.messages import FrameMessage
from big_fiubrother_core.synchronization import ProcessSynchronizer


class StoreFrame(QueueTask):

    def __init__(self, configuration, input_queue, output_queue):
        super().__init__(input_queue)
        self.output_queue = output_queue
        self.configuration = configuration

    def init(self):
        self.db = Database(self.configuration['db'])
        self.process_synchronizer = ProcessSynchronizer(self.configuration['synchronization']) 

    def execute_with(self, messages):
        for message in messages:
            frame = Frame(
                offset=message["offset"],
                video_chunk_id=message['video_chunk_id'])

            self.db.add(frame)

            message['frame_id'] = frame.id

            self.process_synchronizer.register_frame_task(
                str(message['video_chunk_id']),
                str(frame.id))

        for message in messages:
            self.output_queue.put(
                FrameMessage(
                    video_chunk_id=message['video_chunk_id'],
                    frame_id=message['frame_id'],
                    payload=message['payload'])
            )

    def close(self):
        self.db.close()
        self.process_synchronizer.close()