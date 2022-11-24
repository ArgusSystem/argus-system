class VideoChunkMessage:

    def __init__(self, camera_id, timestamp, trace, encoding, duration, sequence_id, samples=None):
        if samples is None:
            samples = []

        self.camera_id = camera_id
        self.timestamp = timestamp
        self.trace = trace
        self.encoding = encoding
        self.duration = duration
        self.samples = samples
        self.sequence_id = sequence_id

    def to_json(self):
        return {
            'camera_id': self.camera_id,
            'timestamp': self.timestamp,
            'trace': self.trace,
            'encoding': self.encoding,
            'samples': self.samples,
            'duration': self.duration,
            'sequence_id': self.sequence_id
        }

    def __str__(self):
        return f'{self.camera_id}-{self.timestamp}'

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.camera_id == other.camera_id and \
                   self.timestamp == other.timestamp and \
                   self.encoding == other.encoding and \
                   self.samples == other.samples and \
                   self.duration == other.duration and \
                   self.sequence_id == other.sequence_id

        return False
