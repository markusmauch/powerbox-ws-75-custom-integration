class LowPassFilter():
    def __init__(self, size = 20):
        self._size = 1 if size < 1 else size
        self._values = []
        self._index = -1

    def add(self, value):
        if self._values.__len__() < self._size:
            if self._values.__len__() == 0 or value != self._values[self._values.__len__() - 1]:
                self._values.append(value)
        else:
            if value != self._values[self._index]:
                self._index = (self._index + 1) % self._size
                self._values[self._index] = value

    @property
    def value(self):
        sum = 0
        for value in self._values:
            sum = sum + value
        return sum / self._values.__len__()