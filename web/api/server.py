from src.app import make_app
from src.controllers.factory import ControllersFactory
from src.server_thread import ServerThread

from utils.application import run
from utils.tracing.src.tracer import get_tracer

DB_KEY = 'db'
PUBLISHER_KEY = 'publisher'
SERVER_KEY = 'server'
TRACER_KEY = 'tracer'
VIDEO_STORAGE_KEY = 'video_storage'

if __name__ == "__main__":
    with run('argus-web-api') as application:
        tracer = get_tracer(**application.configuration[TRACER_KEY], service_name=application.name)

        controllers_factory = ControllersFactory(db_configuration=application.configuration[DB_KEY],
                                                 storage_configuration=application.configuration[VIDEO_STORAGE_KEY],
                                                 publisher_configuration=application.configuration[PUBLISHER_KEY],
                                                 tracer=tracer)

        server = ServerThread(**application.configuration[SERVER_KEY],
                              app=make_app(application.name, controllers_factory.all()))

        server.start()
        print(f'[*] {application.name} started successfully!')

        application.wait()

        server.shutdown()
        server.join()

    print(f'[*] {application.name} stopped successfully!')