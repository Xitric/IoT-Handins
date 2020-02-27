import logging
import os
import time
from serial import Serial

baud_rate = 115200
conn = Serial(port=os.environ["DEVICE_PORT"], baudrate=baud_rate)

logging.basicConfig(filename='thermistor_readings.csv', filemode='w', format='%(message)s', level=logging.INFO)

while True:
    # Read the next measurement and drop the last two characters (\n\r)
    reading = conn.readline().decode("utf-8")[:-2]
    timestamp = time.time_ns()
    logging.info("{};{}".format(timestamp, reading))
