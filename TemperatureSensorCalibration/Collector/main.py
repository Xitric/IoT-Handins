from machine import Pin, ADC
import utime
ad = ADC(Pin(39))

while True:
    print(ad.read())
    utime.sleep_ms(100)
