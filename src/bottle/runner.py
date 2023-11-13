from bottle.bottle import (
    MEMORY_THRESHOLD,
    SENSOR_STATUS_IDLE,
    SENSOR_STATUS_ACQUISITION_DONE,
    ACQUISITION_IS_VALID,
    ACQUISITION_IS_INVALID,
    Memory,
    Sensor,
    ReachThresholdException,
    AcquisitionInvalidException,
)

def check_acquisition(acquisition):
    return ACQUISITION_IS_VALID if acquisition else ACQUISITION_IS_INVALID


def acquire_data_from_sensor(sensor: Sensor, memory: Memory):
    if memory.get_ratio() > MEMORY_THRESHOLD:
        print(f"Memory is full. Send data")
        raise ReachThresholdException()

    if sensor.get_status() == SENSOR_STATUS_IDLE:
        sensor.start_acquisition()
        if sensor.get_status() == SENSOR_STATUS_ACQUISITION_DONE:
            print("Done")
            while True:
                acquisition = sensor.pop_acquisition()
                if acquisition is None:
                    break
                acquisition_status = check_acquisition(acquisition)
                print(acquisition_status)
                if acquisition_status == ACQUISITION_IS_VALID:
                    memory.push(acquisition)
                else:
                    raise AcquisitionInvalidException("Invalid acquisition")
        else:
            raise AcquisitionInvalidException("Invalid acquisition")
    else:
        print(f"Sensor is busy")


def run():
    pass
