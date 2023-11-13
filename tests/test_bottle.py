import pytest

from bottle.runner import acqdata
from bottle.bottle import SSR_ST_IDLE, SimpleMemory, SimpleSensor, ReachTholdEx, \
    AcqInvalEx


def test_memory_at_init():
    # __Given__
    memory = SimpleMemory()

    # __When__Then__
    assert memory.ratio() == pytest.approx(0.0)
    assert memory.nbacq() == 0
    assert memory.thold() == pytest.approx(80.0)


def test_memory_push():
    # __Given__
    memory = SimpleMemory()

    # __When__
    memory.push({})

    # __Then
    assert memory.ratio() == pytest.approx(20.0)
    assert memory.nbacq() == 1


def test_acquire_data_from_sensor():
    # __Given__
    sensor = SimpleSensor()
    memory = SimpleMemory()

    # __When__
    acqdata(s=sensor, mem=memory)

    # __Then__
    assert memory.nbacq() == 1
    assert sensor.st() == SSR_ST_IDLE


def test_to_many_times_acquire_data_from_sensor_raise_exception():
    # __Given__
    sensor = SimpleSensor()
    memory = SimpleMemory()

    # __When__
    reached = False
    for _ in range(10):
        try:
            acqdata(s=sensor, mem=memory)
        except ReachTholdEx:
            reached = True

    # __Then__
    assert reached is True
    assert memory.ratio() >= 80.0


def test_wrong_status_raise_exception():
    # __Given__
    class WrongSensor(SimpleSensor):
        def startacq(self):
            self._status = SSR_ST_IDLE

    sensor = WrongSensor()
    memory = SimpleMemory()

    # __When__
    invalid_raised = False
    for _ in range(10):
        try:
            acqdata(s=sensor, mem=memory)
        except AcqInvalEx:
            invalid_raised = True
    # __Then__

    assert invalid_raised is True
