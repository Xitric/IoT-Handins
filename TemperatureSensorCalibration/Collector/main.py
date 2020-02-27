from machine import Pin, ADC, PWM
from micropython import const
import utime

TEMP_IO = const(39)
adc = ADC(Pin(TEMP_IO, Pin.IN))
adc.atten(ADC.ATTN_6DB)

# The piezo speaker (buzzer) is on pin IO27
BUZ_IO27 = 27
buzzer = Pin(BUZ_IO27, Pin.OUT)
delay = 12


def beep(tone=440):
    beeper = PWM(buzzer, freq=tone, duty=512)
    utime.sleep_ms(500)
    beeper.deinit()


while True:
    print(adc.read())

    # Sample every 10 seconds
    utime.sleep(10)

    # Notify that we need to make a ground-truth measurement every 2 minutes
    delay = delay - 1
    if delay == 0:
        beep()
        delay = 12
