import logging

from utils.application import run


with run('endless_application') as application:
    logging.info('Waiting for shutdown signal!')
    application.wait()
