from .publisher import Publisher
from .consumer import Consumer
import logging

# Set pika logging to WARNING, it can get too verbose
logging.getLogger('pika').setLevel(logging.WARNING)
