from src.summarizer import Summarizer
from utils.application import run
from utils.events.src.message_clients.rabbitmq import Consumer
from utils.orm.src.database import connect

TRACER_KEY = 'tracer'
CONSUMER_KEY = 'consumer'
DB_KEY = 'db'


if __name__ == "__main__":
    with run('argus-summarizer') as application:
        configuration = application.configuration

        connect(**configuration[DB_KEY])

        summarizer = Summarizer(tracer_configuration=configuration[TRACER_KEY])

        consumer_from_classifier = Consumer.new(**configuration[CONSUMER_KEY],
                                                on_message_callback=summarizer.execute_with,
                                                stop_event=application.stop_event)

        print(f'[*] {application.name} started successfully!')

        # keep consuming messages
        consumer_from_classifier.start()
        # stop signal received

    print(f'[*] {application.name} stopped successfully!')
