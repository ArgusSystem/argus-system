class VideoChunkMessage:

    def __init__(self, camera_id, timestamp, encoding, framerate, width, height, sampling_rate=1):
        self.camera_id = camera_id
        self.timestamp = timestamp
        self.encoding = encoding
        self.framerate = framerate
        self.width = width
        self.height = height
        self.sampling_rate = sampling_rate

    def to_json(self):
        return {
            'camera_id': self.camera_id,
            'timestamp': self.timestamp,
            'encoding': self.encoding,
            'framerate': self.framerate,
            'width': self.width,
            'height': self.height,
            'sampling_rate': self.sampling_rate
        }

    def __str__(self):
        return f'{self.camera_id}-{self.timestamp}'

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.camera_id == other.camera_id and \
                   self.timestamp == other.timestamp and \
                   self.encoding == other.encoding and \
                   self.framerate == other.framerate and \
                   self.width == other.width and \
                   self.height == other.height and \
                   self.sampling_rate == other.sampling_rate

        return False
