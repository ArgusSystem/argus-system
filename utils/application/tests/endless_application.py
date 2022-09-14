from ..src.application import run


with run('endless_application') as application:
    print('Waiting for shutdown signal!')
    application.wait()
