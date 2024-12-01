
class LowPassFilter:
    def __init__(self, alpha: float = 0.8):
        """
        Initialize the LowPassFilter.
        :param alpha: Smoothing factor (0 < alpha < 1), determines the weight of new vs old values.
        """
        if not (0 < alpha <= 1):
            raise ValueError("Alpha must be between 0 and 1.")
        self.alpha = alpha
        self._current_value = None

    def add(self, value: float):
        """
        Add a new measurement and update the smoothed value.
        :param value: The new measurement to add.
        """
        if self._current_value is None:
            self._current_value = value
        else:
            self._current_value = self.alpha * value + (1 - self.alpha) * self._current_value

    @property
    def value(self):
        """
        Return the current smoothed value.
        :return: The smoothed value, or None if no values have been added yet.
        """
        return round(self._current_value, 1) if self._current_value is not None else None




# class LowPassFilter:
#     def __init__(self, size = 10):
#         self._values = deque(maxlen=size)

#     def add(self, value):
#         self._values.append(value)

#     @property
#     def value(self):
#         return round(sum(self._values) / len(self._values), 1)


# class LowPassFilter:
#     def __init__(self, cutoff=0.005, sampling_interval=20, order=2):
#         """
#         Initialize the low-pass filter with the given parameters.
#         :param cutoff: Cutoff frequency in Hz (default 0.005 Hz)
#         :param sampling_interval: Time between readings in seconds (default 20 seconds)
#         :param order: Order of the Butterworth filter (default 2)
#         """
#         self._cutoff = cutoff
#         self._fs = 1 / sampling_interval  # Sampling frequency in Hz
#         self._order = order
#         self._values = []
#         self._b, self._a = self._design_filter()

#     def _design_filter(self):
#         """Design the Butterworth filter coefficients."""
#         nyquist = 0.5 * self._fs
#         normal_cutoff = self._cutoff / nyquist
#         b, a = signal.butter(self._order, normal_cutoff, btype='low', analog=False)
#         return b, a

#     def add(self, new_reading):
#         """
#         Add a new temperature reading and return the filtered value.
#         :param new_reading: New temperature reading (float)
#         :return: Filtered temperature value (float)
#         """
#         self._values.append(new_reading)
#         filtered_value = signal.lfilter(self._b, self._a, self._values)[-1]
#         return filtered_value

#     @property
#     def value(self):
#         """Return the entire list of filtered readings."""
#         if self._values is not None and self._values[0] is not None:
#             return self._values[0]

