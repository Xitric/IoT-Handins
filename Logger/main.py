from serial import Serial
import time
import logging

serConOut = Serial('COM3', 115200)
serConIn = Serial('/dev/cu.SLAB_USBtoUART', 115200)

logging.basicConfig(filename='log.log', filemode='w', format='%(message)s', level=logging.INFO)


def signalTurnOn():
    logTimeStamp('1')


def signalTurnOff():
    logTimeStamp('0')


def logTimeStamp(signal):
    logging.info('before_send\t{}\t{}'.format(signal, time.time_ns()))
    serConOut.write(signal.encode('utf-8'))
    logging.info('after_send\t{}\t{}'.format(signal, time.time_ns()))
    readSignal()


def readSignal():
    value = str(serConIn.read())
    logging.info('recieve\t{}\t{}'.format(value, time.time_ns()))


for _ in range(10):
    signalTurnOn()
    time.sleep(1)
    signalTurnOff()
    time.sleep(1)

serConOut.close()
