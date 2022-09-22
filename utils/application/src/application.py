from contextlib import contextmanager
from threading import Event

from setproctitle import setproctitle

from .arguments import parse_arguments
from .configuration import load_configuration
from .logging_service import LoggingService
from .signal_handler import SignalHandler


@contextmanager
def run(name):
    # Parse arguments of the application
    arguments = parse_arguments(name)

    # Load configuration
    configuration = load_configuration(arguments.config_file)

    # Set application name
    setproctitle(name)

    # Enable signal handling
    signal_handler = SignalHandler()

    # Start logging
    logging_service = LoggingService(name, configuration['logging'])
    logging_service.start()

    application = Application(name, configuration)
    signal_handler.subscribe(application.stop)

    yield application

    # Stop logging
    logging_service.stop()


class Application:

    def __init__(self, name, configuration):
        self.name = name
        self.configuration = configuration
        self.stop_event = Event()

    def is_stopped(self):
        return self.stop_event.is_set()

    def stop(self):
        self.stop_event.set()

    def wait(self):
        self.stop_event.wait()
