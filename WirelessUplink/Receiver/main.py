import socket
from filelock import FileLock
from datetime import datetime


def get_connection() -> socket.socket:
    # UDP connection
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(("", 5000))
    # s.listen()
    # c, a = s.accept()
    # print("Connection from {}".format(a))
    # return c
    return s


with FileLock("logs.csv.lock"):
    connection = get_connection()

    log = open("logs.csv", "a")
    while True:
        byte_data, addr = connection.recvfrom(4096)
        msg = byte_data.decode("utf-8")
        elements = msg.split(";")

        send_time = datetime.strptime(elements[1], "%Y-%m-%d %H:%M:%S.%f")
        reception_time = datetime.now()
        reception_time_string = reception_time.strftime("%Y-%m-%d %H:%M:%S.%f")
        latency = (reception_time - send_time).total_seconds() * 1_000_000

        # Format is:
        # Message number; send time; reception time; latency; temperature; light level
        log.write("{};{};{};{};{};{}\n".format(elements[0], elements[1], reception_time_string,
                                             latency, elements[2], elements[3]))
        log.flush()
