#!/usr/bin/env python3

from classifier import FaceClassificationTask
from utils.application import run
from utils.events.src.message_clients.rabbitmq import Consumer
from utils.orm.src.database import connect

# este import hace falta porque el .pkl de SVClassifier actualmente se crea en el modulo __main__
# asi que tiene que existir SVClassifier en __main__
from classifier import SVClassifier

FACE_CLASSIFIER_KEY = 'face_classifier'
FACE_EMBEDDER_KEY = 'face_embedder'
PUBLISHER_WEB_KEY = 'publisher_web'
PUBLISHER_SUMMARIZER_KEY = 'publisher_summarizer'
PUBLISHER_CLUSTERER_KEY = 'publisher_clusterer'
STORAGE_KEY = 'storage'
TRACER_KEY = 'tracer'
CONSUMER_KEY = 'consumer'
DB_KEY = 'db'


if __name__ == "__main__":
    with run('argus-classifier') as application:
        configuration = application.configuration

        connect(**configuration[DB_KEY])

        # init
        face_classification_task = FaceClassificationTask(
            face_classifier_configuration=configuration[FACE_CLASSIFIER_KEY],
            face_embedder_configuration=configuration[FACE_EMBEDDER_KEY],
            publisher_to_web_configuration=configuration[PUBLISHER_WEB_KEY],
            publisher_to_warden_configuration=configuration[PUBLISHER_SUMMARIZER_KEY],
            publisher_to_clusterer_configuration=configuration[PUBLISHER_CLUSTERER_KEY],
            storage_configuration=configuration[STORAGE_KEY],
            tracer_configuration=configuration[TRACER_KEY])

        consumer_from_sampler = Consumer.new(**configuration[CONSUMER_KEY],
                                             on_message_callback=face_classification_task.execute_with,
                                             stop_event=application.stop_event)

        print(f'[*] {application.name} started successfully!')

        # keep consuming messages
        consumer_from_sampler.start()
        # stop signal received

        # close everything
        face_classification_task.close()

    print(f'[*] {application.name} stopped successfully!')
