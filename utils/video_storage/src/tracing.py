from math import trunc
from time import time
from contextlib import contextmanager
import logging


@contextmanager
def timer(self, key, operation):
    start = time()
    yield
    end = time()

    logging.info("S3 {} - {} for {} time elapsed: {}".format(
        self.bucket,
        operation,
        key,
        trunc((end - start) * 1000)))
