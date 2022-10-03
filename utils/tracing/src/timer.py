from contextlib import contextmanager
from timeit import default_timer


@contextmanager
def timer(logger, task):
    start = default_timer()
    yield
    end = default_timer()
    logger.debug('%s: %f', task, end - start)
