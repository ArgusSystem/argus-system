from src.warden import Warden
from utils.application import run
from utils.events.src.message_clients.rabbitmq import Consumer
from utils.orm.src.database import connect
from utils.tracing.src.tracer import get_tracer

CONSUMER_KEY = 'consumer'
DB_KEY = 'db'
PUBLISHER_KEY = 'publisher'
TRACER_KEY = 'tracer'

if __name__ == "__main__":
    with run('argus-warden') as application:
        configuration = application.configuration

        connect(**configuration[DB_KEY])

        warden = Warden(tracer=get_tracer(**configuration[TRACER_KEY], service_name=application.name),
                        publisher_configuration=configuration[PUBLISHER_KEY])

        consumer = Consumer.new(**configuration[CONSUMER_KEY],
                                on_message_callback=warden.execute_with,
                                stop_event=application.stop_event)

        print(f'[*] {application.name} started successfully!')

        consumer.start()

    print(f'[*] {application.name} stopped successfully!')
