from collections import deque

class LowPassFilter:
    def __init__(self, size = 10):
        self._values = deque(maxlen=size)

    def add(self, value):
        self._values.append(value)

    @property
    def value(self):
        return round(sum(self._values) / len(self._values), 1)
