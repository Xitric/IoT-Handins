from serial import Serial
import time
import logging
import os

baud_rate = 115200
serConOut = Serial(os.environ['TRANSMITTER_PORT'], baud_rate)
serConIn = Serial(os.environ['RECEIVER_PORT'], baud_rate)

logging.basicConfig(filename='measurements1.csv', filemode='w', format='%(message)s', level=logging.INFO)


def signalTurnOn():
    logTimeStamp('1')


def signalTurnOff():
    logTimeStamp('0')


def logTimeStamp(signal):
    logging.info('before_send;{};{}'.format(signal, time.time_ns()))
    serConOut.write(signal.encode('utf-8'))
    logging.info('after_send;{};{}'.format(signal, time.time_ns()))
    readSignal()


def readSignal():
    value = serConIn.read().decode('utf-8')
    logging.info('receive;{};{}'.format(value, time.time_ns()))


for _ in range(1800):
    signalTurnOn()
    time.sleep(1)
    signalTurnOff()
    time.sleep(1)

serConOut.close()
