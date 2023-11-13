import time
from typing import Protocol

MM_THOLD = 80.0
SSR_ST_IDLE = 0
SENSOR_STATUS_ACQUIRING = 10
SSR_ST_ACQ_OK = 20
ACQ_VAL = 100
ACQ_INVAL = 110


class ReachTholdEx(Exception):
    pass


class AcqInvalEx(Exception):
    pass


class Bottle:
    pass


class Memory(Protocol):
    def ratio(self):
        ...

    def setthold(self):
        ...

    def thold(self):
        ...

    def push(self, data):
        ...

    def data(self):
        ...

    def nbacq(self):
        ...


class Sensor(Protocol):
    def st(self):
        pass

    def startacq(self):
        pass

    def stop_acquisition(self):
        pass

    def popacq(self):
        pass


class SimpleMemory(Memory):
    def __init__(self, threshold=MM_THOLD):
        self._max_length = 5
        self._storage = []
        self._threshold = threshold

    def data(self):
        return self._storage

    def ratio(self):
        return len(self._storage) / self._max_length * 100.0

    def thold(self):
        return self._threshold

    def nbacq(self):
        return len(self._storage)

    def push(self, data):
        self._storage.append(data)


class SimpleSensor(Sensor):
    def __init__(self, max_data=5):
        self._buffer = []
        self._status = SSR_ST_IDLE
        self._max_data = max_data

    def st(self):
        return self._status

    def startacq(self):
        self._status = SENSOR_STATUS_ACQUIRING
        acq = dict(time=time.time(), data=[])
        for _ in range(self._max_data):
            acq["data"].append(dict(time=time.time(), data=self._get_data()))
        self._buffer.append(acq)

        self._status = SSR_ST_ACQ_OK

    def popacq(self):
        _r = self._buffer.pop() if len(self._buffer) else None
        if _r is None:
            self._status = SSR_ST_IDLE
        return _r

    def _get_data(self):
        from random import randint

        return [randint(0, 256) for i in range(10)]
