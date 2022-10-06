from detector import FaceDetectionTask
from utils.application import run
from utils.events.src.message_clients.rabbitmq import Consumer

CONSUMER_KEY = 'consumer'

if __name__ == "__main__":
    with run('argus-detector') as application:

        # init
        face_detection_task = FaceDetectionTask(application.configuration)
        consumer_from_sampler = Consumer.new(**application.configuration[CONSUMER_KEY],
                                             on_message_callback=face_detection_task.execute_with,
                                             stop_event=application.stop_event)

        print(f'[*] {application.name} started successfully!')

        # keep consuming messages
        consumer_from_sampler.start()
        # stop signal received

        # close everything
        face_detection_task.close()

    print(f'[*] {application.name} stopped successfully!')
