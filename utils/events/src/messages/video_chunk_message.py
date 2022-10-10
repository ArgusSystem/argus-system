class VideoChunkMessage:

    def __init__(self, camera_id, timestamp, trace, encoding, framerate, width, height, duration, sampling_rate=1):
        self.camera_id = camera_id
        self.timestamp = timestamp
        self.trace = trace
        self.encoding = encoding
        self.framerate = framerate
        self.width = width
        self.height = height
        self.sampling_rate = sampling_rate
        self.duration = duration

    def to_json(self):
        return {
            'camera_id': self.camera_id,
            'timestamp': self.timestamp,
            'trace': self.trace,
            'encoding': self.encoding,
            'framerate': self.framerate,
            'width': self.width,
            'height': self.height,
            'sampling_rate': self.sampling_rate,
            'duration': self.duration
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
                   self.sampling_rate == other.sampling_rate and \
                   self.duration == other.duration

        return False
