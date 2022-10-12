from detector import FaceDetectionTask
from utils.application import run
from utils.events.src.message_clients.rabbitmq import Consumer

DEBUG_KEY = 'debug'
FACE_DETECTOR_KEY = 'face_detector'
PUBLISHER_KEY = 'publisher'
STORAGE_KEY = 'storage'
TRACER_KEY = 'tracer'
CONSUMER_KEY = 'consumer'


if __name__ == "__main__":
    with run('argus-detector') as application:
        configuration = application.configuration

        # init
        face_detection_task = FaceDetectionTask(
            debug_mode=configuration[DEBUG_KEY],
            face_detector_configuration=configuration[FACE_DETECTOR_KEY],
            publisher_to_classifier_configuration=configuration[PUBLISHER_KEY],
            storage_configuration=configuration[STORAGE_KEY],
            tracer_configuration=configuration[TRACER_KEY])

        consumer_from_sampler = Consumer.new(**configuration[CONSUMER_KEY],
                                             on_message_callback=face_detection_task.execute_with,
                                             stop_event=application.stop_event)

        print(f'[*] {application.name} started successfully!')

        # keep consuming messages
        consumer_from_sampler.start()
        # stop signal received

        # close everything
        face_detection_task.close()

    print(f'[*] {application.name} stopped successfully!')
