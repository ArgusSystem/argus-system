import sys
import graypy
import logging
from logging import StreamHandler
from logging.handlers import QueueListener, QueueHandler
from queue import Queue

REMOTE_KEY = 'remote'
LEVEL_KEY = 'level'

LOGGING_LEVEL = logging.INFO
LOGGING_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'


def remote_logging(application_name, configuration):
    log_queue = Queue()

    graylog_handler = graypy.GELFUDPHandler(
        host=configuration['host'],
        port=configuration['port'],
        facility=application_name)

    return QueueHandler(log_queue), QueueListener(log_queue, graylog_handler)


def _level(configuration):
    return configuration[LEVEL_KEY] if LEVEL_KEY in configuration else LOGGING_LEVEL


class LoggingService:

    def __init__(self, application_name, configuration):
        self.services = []

        handlers = [StreamHandler(sys.stdout)]

        if REMOTE_KEY in configuration:
            handler, service = remote_logging(application_name, configuration[REMOTE_KEY])
            handlers.append(handler)
            self.services.append(service)

        logging.basicConfig(level=_level(configuration),
                            format=LOGGING_FORMAT,
                            handlers=handlers)

    def start(self):
        for service in self.services:
            service.start()

    def stop(self):
        for service in self.services:
            service.stop()
