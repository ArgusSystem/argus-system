from classifier import FaceClassificationTask
from utils.application import run
from utils.events.src.message_clients.rabbitmq import Consumer

# esto hace falta porque el .pkl actualmente se crea en el modulo __main__
# asi que tiene que existir SVClassifier en __main__
from classifier import SVClassifier

CONSUMER_KEY = 'consumer'

if __name__ == "__main__":
    with run('argus-classifier') as application:

        # init
        face_classification_task = FaceClassificationTask(application.configuration)
        consumer_from_sampler = Consumer.new(**application.configuration[CONSUMER_KEY],
                                             on_message_callback=face_classification_task.execute_with,
                                             stop_event=application.stop_event)

        # keep consuming messages
        consumer_from_sampler.start()
        # stop signal received

        # close everything
        face_classification_task.close()

    print(f'[*] {application.name} stopped successfully!')