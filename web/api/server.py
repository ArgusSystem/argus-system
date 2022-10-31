from src.app import make_app
from src.controllers.factory import ControllersFactory
from src.server_thread import ServerThread

from utils.application import run

DB_KEY = 'db'
VIDEO_STORAGE_KEY = 'video_storage'
SERVER_KEY = 'server'

if __name__ == "__main__":
    with run('argus-web-api') as application:
        controllers_factory = ControllersFactory(db_configuration=application.configuration[DB_KEY])

        server = ServerThread(**application.configuration[SERVER_KEY],
                              app=make_app(application.name, controllers_factory.all()))

        server.start()
        print(f'[*] {application.name} started successfully!')

        application.wait()

        server.shutdown()
        server.join()

    print(f'[*] {application.name} stopped successfully!')