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

def is_valid(acquisition):
    return check_acquisition(acquisition) == ACQUISITION_IS_VALID

def acquire_data_from_sensor(sensor: Sensor, memory: Memory):
    check_memory(memory)
    if not check_sensor_is_ready(sensor):
        return
    
    sensor.start_acquisition()
    check_sensor_has_finished_acquisition(sensor)
    transfert_acquisitions_to_memory(sensor, memory)

def transfert_acquisitions_to_memory(sensor, memory):
    for acquisition in unload_sensor(sensor):
        push_checked_acquisition_to_memory(memory, acquisition)

def push_checked_acquisition_to_memory(memory, acquisition):
    if is_valid(acquisition):
        memory.push(acquisition)
    else:
        raise AcquisitionInvalidException("Invalid acquisition")

def check_sensor_has_finished_acquisition(sensor):
    if sensor.get_status() != SENSOR_STATUS_ACQUISITION_DONE:
        raise AcquisitionInvalidException("Invalid acquisition")

def check_sensor_is_ready(sensor):
    if sensor.get_status() != SENSOR_STATUS_IDLE:
        print("Sensor is busy")
        return False
    return True
    
        

def check_memory(memory):
    if memory.get_ratio() > MEMORY_THRESHOLD:
        print(f"Memory is full. Send data")
        raise ReachThresholdException()

        
def unload_sensor(sensor: Sensor):
    while True:
        acquisition = sensor.pop_acquisition()
        if acquisition is None:
            break
        yield acquisition




def run():
    pass
