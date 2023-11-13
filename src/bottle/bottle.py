import time
from typing import Protocol

MEMORY_THRESHOLD = 80.0
SENSOR_STATUS_IDLE = 0
SENSOR_STATUS_ACQUIRING = 10
SENSOR_STATUS_ACQUISITION_DONE = 20
ACQUISITION_IS_VALID = 100
ACQUISITION_IS_INVALID = 110


class ReachThresholdException(Exception):
    pass


class AcquisitionInvalidException(Exception):
    pass


class Bottle:
    pass


class Memory(Protocol):
    def get_ratio(self):
        ...

    def set_threshold(self):
        ...

    def get_threshold(self):
        ...

    def push(self, data):
        ...

    def get_data(self):
        ...

    def get_nb_of_acquisitions(self):
        ...


class Sensor(Protocol):
    def get_status(self):
        pass

    def start_acquisition(self):
        pass

    def stop_acquisition(self):
        pass

    def pop_acquisition(self):
        pass


class Controller(Protocol):
    pass


class SimpleMemory(Memory):
    def __init__(self, threshold=MEMORY_THRESHOLD):
        self._max_length = 5
        self._storage = []
        self._threshold = threshold

    def get_data(self):
        return self._storage

    def get_ratio(self):
        return len(self._storage) / self._max_length * 100.0

    def get_threshold(self):
        return self._threshold

    def get_nb_of_acquisitions(self):
        return len(self._storage)

    def push(self, data):
        self._storage.append(data)


class SimpleSensor(Sensor):
    def __init__(self, max_data=5):
        self._buffer = []
        self._status = SENSOR_STATUS_IDLE
        self._max_data = max_data

    def get_status(self):
        return self._status

    def start_acquisition(self):
        self._status = SENSOR_STATUS_ACQUIRING
        acq = dict(time=time.time(), data=[])
        for _ in range(self._max_data):
            acq["data"].append(dict(time=time.time(), data=self._get_data()))
        self._buffer.append(acq)

        self._status = SENSOR_STATUS_ACQUISITION_DONE

    def pop_acquisition(self):
        _r = self._buffer.pop() if len(self._buffer) else None
        if _r is None:
            self._status = SENSOR_STATUS_IDLE
        return _r

    def _get_data(self):
        from random import randint

        return [randint(0, 256) for i in range(10)]
