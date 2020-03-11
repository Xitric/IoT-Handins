# Since the standard implementation is clearly broken, this is adapted from:
# https://github.com/micropython/micropython/blob/master/ports/esp8266/modules/ntptime.py
# We essentially fixed a bug in the official code...
import socket
import struct
import utime
import machine

NTP_DELTA = 3155673600
host = "dk.pool.ntp.org"


def time():
    ntp_query = bytearray(48)
    ntp_query[0] = 0x1B
    addr = socket.getaddrinfo(host, 123)[0][-1]
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.settimeout(1)
        _ = s.sendto(ntp_query, addr)
        msg = s.recv(48)
    finally:
        s.close()

    val = struct.unpack("!I", msg[40:44])[0]
    return val - NTP_DELTA


def settime():
    t = utime.localtime(time())
    machine.RTC().init((t[0], t[1], t[2], 0, t[3] + 1, t[4], t[5], t[6]))
