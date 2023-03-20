#!/usr/bin/env python3

from .src.notifier import Notifier
from utils.application import run
from utils.events.src.message_clients.rabbitmq import Consumer
from utils.orm.src.database import connect as db_connect
from utils.tracing.src.tracer import get_tracer

CONSUMER_KEY = 'consumer'
DB_KEY = 'db'
TRACER_KEY = 'tracer'


if __name__ == "__main__":
    with run('argus-warden') as application:
        db_connect(**application.configuration[DB_KEY])

        notifier = Notifier(tracer=get_tracer(**application.configuration[TRACER_KEY], service_name=application.name))

        consumer = Consumer.new(**application.configuration[CONSUMER_KEY],
                                on_message_callback=notifier.on_broken_rule,
                                stop_event=application.stop_event)

        print(f'[*] {application.name} started successfully!')

        consumer.start()

    print(f'[*] {application.name} stopped successfully!')