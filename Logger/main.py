from serial import Serial
import time
import logging

serCon = Serial('COM3',115200)
logging.basicConfig(filename='log.log',filemode='w',format='%(message)s',level=logging.INFO)

def signalTurnOn():
    logTimeStamp('1')

def signalTurnOff():
    logTimeStamp('0')

def logTimeStamp(signal):
    logging.info('before_send\t{}\t{}'.format(signal,time.time_ns()))

    serCon.write(signal.encode('utf-8'))
    logging.info('after_send\t{}\t{}'.format(signal,time.time_ns()))

for _ in range(10):
    signalTurnOn()
    time.sleep(1)
    signalTurnOff()
    time.sleep(1)

serCon.close()

