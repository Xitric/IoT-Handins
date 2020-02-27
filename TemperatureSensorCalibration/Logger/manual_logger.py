import logging
import time

logging.basicConfig(filename='ground_readings.csv', filemode='w', format='%(message)s', level=logging.INFO)

print("Enter your measurements whenever you wish:")
while True:
    reading = input("> ")
    if reading == "q":
        break

    timestamp = time.time_ns()
    logging.info("{};{}".format(timestamp, reading))
