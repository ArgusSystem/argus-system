SIGNED_INT_MASK = (1 << 31) - 1


class SequenceGenerator:

    def __init__(self):
        self.current = 0

    def get(self):
        value = self.current
        self.current += 1
        return value & SIGNED_INT_MASK
