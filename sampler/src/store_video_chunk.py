from big_fiubrother_core import QueueTask
from big_fiubrother_core.db import Database, VideoChunk
from big_fiubrother_core.storage import raw_storage
from big_fiubrother_core.synchronization import ProcessSynchronizer
from os import path
import logging


class StoreVideoChunk(QueueTask):

    def __init__(self, configuration, input_queue, output_queue):
        super().__init__(input_queue)
        self.output_queue = output_queue
        self.configuration = configuration

    def init(self):
        self.db = Database(self.configuration['db'])
        self.storage = raw_storage(self.configuration['storage'])
        self.process_synchronizer = ProcessSynchronizer(
            self.configuration['synchronization'])

    def execute_with(self, message):
        video_chunk = VideoChunk(camera_id=message.camera_id,
                                 timestamp=message.timestamp)

        self.db.add(video_chunk)

        logging.info(f"{video_chunk.id} created in DB. Sampling starting!")

        self.process_synchronizer.register_video_task(str(video_chunk.id))
        
        filepath = path.join('tmp', '{}.h264'.format(video_chunk.id))

        with open(filepath, 'wb') as file:
            file.write(message.payload)

        self.storage.store_file(str(video_chunk.id), filepath)

        self.output_queue.put({
            'video_chunk_id': video_chunk.id,
            'path': filepath
        })

    def close(self):
        self.db.close()
        self.process_synchronizer.close()
