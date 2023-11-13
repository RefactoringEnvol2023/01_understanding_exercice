from bottle.bottle import (
    MM_THOLD,
    SSR_ST_IDLE,
    SSR_ST_ACQ_OK,
    ACQ_VAL,
    ACQ_INVAL,
    Memory,
    Sensor,
    ReachTholdEx,
    AcqInvalEx,
)

def chkacq(acq):
    return ACQ_VAL if acq else ACQ_INVAL


def acqdata(s: Sensor, mem: Memory):
    if mem.ratio() > MM_THOLD:
        print(f"Memory is full. Send data")
        raise ReachTholdEx()

    if s.st() == SSR_ST_IDLE:
        s.startacq()
        if s.st() == SSR_ST_ACQ_OK:
            print("Done")
            while True:
                acq = s.popacq()
                if acq is None:
                    break
                acq_st = chkacq(acq)
                print(acq_st)
                if acq_st == ACQ_VAL:
                    mem.push(acq)
                else:
                    raise AcqInvalEx("Invalid acquisition")
        else:
            raise AcqInvalEx("Invalid acquisition")
    else:
        print(f"Sensor is busy")


def run():
    pass
