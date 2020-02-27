from machine import I2C, Pin
from micropython import const
import utime
import sys

# IO Pin numbers on U1 connecting to I2C0_SCL and I2C0_SDA which make up the I2C bus that the light sensor is
# connected to
from bh1750 import BH1750

I2C0_SCL = const(26)
I2C0_SDA = const(25)

scl = Pin(I2C0_SCL, Pin.IN)
sda = Pin(I2C0_SDA, Pin.OUT)
i2c = I2C(-1, scl=scl, sda=sda)

s = BH1750(i2c)
light = False

for _ in range(100000):
    luminance = s.luminance(BH1750.CONT_HIRES_1)

    if luminance > 6 and not light:
        light = True
        sys.stdout.write('1')

    elif luminance < 6 and light:
        light = False
        sys.stdout.write('0')

    utime.sleep_ms(1)
