import pytest

from bottle.runner import acquire_data_from_sensor
from bottle.bottle import SENSOR_STATUS_IDLE, SimpleMemory, SimpleSensor, ReachThresholdException, \
    AcquisitionInvalidException


def test_memory_at_init():
    # __Given__
    memory = SimpleMemory()

    # __When__Then__
    assert memory.get_ratio() == pytest.approx(0.0)
    assert memory.get_nb_of_acquisitions() == 0
    assert memory.get_threshold() == pytest.approx(80.0)


def test_memory_push():
    # __Given__
    memory = SimpleMemory()

    # __When__
    memory.push({})

    # __Then
    assert memory.get_ratio() == pytest.approx(20.0)
    assert memory.get_nb_of_acquisitions() == 1


def test_acquire_data_from_sensor():
    # __Given__
    sensor = SimpleSensor()
    memory = SimpleMemory()

    # __When__
    acquire_data_from_sensor(sensor=sensor, memory=memory)

    # __Then__
    assert memory.get_nb_of_acquisitions() == 1
    assert sensor.get_status() == SENSOR_STATUS_IDLE


def test_to_many_times_acquire_data_from_sensor_raise_exception():
    # __Given__
    sensor = SimpleSensor()
    memory = SimpleMemory()

    # __When__
    reached = False
    for _ in range(10):
        try:
            acquire_data_from_sensor(sensor=sensor, memory=memory)
        except ReachThresholdException:
            reached = True

    # __Then__
    assert reached is True
    assert memory.get_ratio() >= 80.0


def test_wrong_status_raise_exception():
    # __Given__
    class WrongSensor(SimpleSensor):
        def start_acquisition(self):
            self._status = SENSOR_STATUS_IDLE

    sensor = WrongSensor()
    memory = SimpleMemory()

    # __When__
    invalid_raised = False
    for _ in range(10):
        try:
            acquire_data_from_sensor(sensor=sensor, memory=memory)
        except AcquisitionInvalidException:
            invalid_raised = True
    # __Then__

    assert invalid_raised is True
