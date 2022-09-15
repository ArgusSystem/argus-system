from queue import Queue, Empty

TIMEOUT_S = 1


class InterThreadingQueue:

    def __init__(self):
        self._queue = Queue()

    def put(self, message):
        self._queue.put(message)

    def compute(self, callback):
        try:
            message = self._queue.get(timeout=TIMEOUT_S)
            callback(message)
        except Empty:
            pass
