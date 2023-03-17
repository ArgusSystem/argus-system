from src.warden import Warden
from utils.application import run
from utils.events.src.message_clients.rabbitmq import Consumer

TRACER_KEY = 'tracer'
CONSUMER_KEY = 'consumer'
DB_KEY = 'db'


if __name__ == "__main__":
    with run('argus-warden') as application:
        configuration = application.configuration

        summarizer = Warden(tracer_configuration=configuration[TRACER_KEY], db_configuration=configuration[DB_KEY])

        consumer_from_classifier = Consumer.new(**configuration[CONSUMER_KEY],
                                                on_message_callback=summarizer.execute_with,
                                                stop_event=application.stop_event)

        print(f'[*] {application.name} started successfully!')

        # keep consuming messages
        consumer_from_classifier.start()
        # stop signal received

    print(f'[*] {application.name} stopped successfully!')
