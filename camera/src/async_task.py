from threading import Thread, Event


class AsyncTask:

    def __init__(self, callback):
        self._thread = Thread(target=lambda: callback(self.is_running))
        self._start_event = Event()
        self._end_event = Event()

    def is_running(self):
        return self._start_event.is_set() and not self._end_event.is_set()

    def start(self):
        self._start_event.set()
        self._end_event.clear()
        self._thread.start()

    def stop(self):
        self._end_event.set()

    def wait(self):
        self._thread.join()
