class FrameMessage:

    def __init__(self, video_chunk, offset, timestamp, trace):
        self.video_chunk = video_chunk
        self.offset = offset
        self.timestamp = timestamp
        self.trace = trace

    def to_json(self):
        return {
            'video_chunk': self.video_chunk,
            'offset': self.offset,
            'timestamp': self.timestamp,
            'trace': self.trace
        }

    def __str__(self):
        return f'{self.video_chunk}-{self.offset}'

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.video_chunk == other.video_chunk and self.offset == other.offset

        return False
