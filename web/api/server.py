from src.app import make_app
from src.controllers.factory import ControllersFactory
from src.server_thread import ServerThread
import ssl

from utils.application import run
from utils.tracing.src.tracer import get_tracer

DB_KEY = 'db'
PUBLISHER_TO_WARDEN_KEY = 'publisher_to_warden'
PUBLISHER_TO_CLUSTERER_KEY = 'publisher_to_clusterer'
SERVER_KEY = 'server'
TRACER_KEY = 'tracer'
VIDEO_STORAGE_KEY = 'video_storage'
SSL_CONFIG = 'ssl'
SSL_CERT = 'certfile'
SSL_KEY = 'keyfile'


if __name__ == "__main__":
    with run('argus-web-api') as application:
        tracer = get_tracer(**application.configuration[TRACER_KEY], service_name=application.name)

        # Init controllers
        controllers_factory = ControllersFactory(db_configuration=application.configuration[DB_KEY],
                                                 storage_configuration=application.configuration[VIDEO_STORAGE_KEY],
                                                 publisher_to_warden_configuration=application.configuration[PUBLISHER_TO_WARDEN_KEY],
                                                 publisher_to_clusterer_configuration=application.configuration[PUBLISHER_TO_CLUSTERER_KEY],
                                                 tracer=tracer)

        ssl_context = None
        # Configure SSL context
        if SSL_CONFIG in application.configuration and application.configuration[SSL_CONFIG][SSL_CERT] and application.configuration[SSL_CONFIG][SSL_KEY]:
            ssl_context = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
            ssl_context.load_cert_chain(**application.configuration[SSL_CONFIG])

        # Create server thread
        server = ServerThread(**application.configuration[SERVER_KEY],
                              app=make_app(application.name, controllers_factory.all()),
                              ssl_context=ssl_context)

        server.start()
        print(f'[*] {application.name} started successfully!')

        application.wait()

        server.shutdown()
        server.join()

    print(f'[*] {application.name} stopped successfully!')
