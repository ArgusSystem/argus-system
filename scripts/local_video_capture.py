import cv2


class LocalVideoCapture:

    def __init__(self, filepath):
        self.capture = cv2.VideoCapture(filepath)
        self.fps = int(self.capture.get(cv2.CAP_PROP_FPS))
        self.width = int(self.capture.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(self.capture.get(cv2.CAP_PROP_FRAME_HEIGHT))

        print(f'Source video file: {filepath}. Native resolution: ({self.width}, {self.height}). Native FPS: {self.fps}')

    def read(self):
        return self.capture.read()

    def close(self):
        self.capture.release()
