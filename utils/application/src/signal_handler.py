import signal


class SignalHandler:

    def __init__(self):
        self.callbacks = []

        signal.signal(signal.SIGINT, self.__stop_signal_received)
        signal.signal(signal.SIGTERM, self.__stop_signal_received)

    def subscribe(self, callback):
        self.callbacks.append(callback)

    def __stop_signal_received(self, _signum, _frame):
        print('Stop signal received!')

        for callback in self.callbacks:
            callback()
