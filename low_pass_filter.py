class LowPassFilter():
    def __init__(self, size = 10):
        self._size = 1 if size < 1 else size
        self._values = []
        for i in range(self._size):
            self._values.append(0)
        self._index = 0

    def add(self, value):
        self._values[self._index] = value
        self._index = (self._index + 1) % self._size

    @property
    def value(self):
        sum = 0
        for value in self._values:
            sum = sum + value
        return sum / self._size