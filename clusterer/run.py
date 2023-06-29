from src.unknown_clusterer import UnknownFacesClusterer
from utils.application import run
from utils.events.src.message_clients.rabbitmq import Consumer
from utils.orm.src.database import connect

FACES_BATCH_SIZE_KEY = 'faces_batch_size'
SKIP_OUTLIERS_KEY = 'skip_outliers'
TRACER_KEY = 'tracer'
CONSUMER_KEY = 'consumer'
DB_KEY = 'db'


if __name__ == "__main__":
    with run('argus-clusterer') as application:
        configuration = application.configuration

        connect(**configuration[DB_KEY])

        # init
        unknown_faces_clusterer = UnknownFacesClusterer(faces_batch_size=configuration[FACES_BATCH_SIZE_KEY],
                                                        skip_outliers=configuration[SKIP_OUTLIERS_KEY],
                                                        tracer_configuration=configuration[TRACER_KEY])

        consumer_from_sampler = Consumer.new(**configuration[CONSUMER_KEY],
                                             on_message_callback=unknown_faces_clusterer.process,
                                             stop_event=application.stop_event)

        print(f'[*] {application.name} started successfully!')

        # keep consuming messages
        consumer_from_sampler.start()
        # stop signal received

    print(f'[*] {application.name} stopped successfully!')
