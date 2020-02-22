import machine
import utime
import sys

ledAzure = machine.Pin(33)
ledWifi = machine.Pin(32)

def turnOn():
    ledAzure.on()
    ledWifi.on()

def turnOff():
    ledAzure.off()
    ledWifi.off()

def readInput():
    value = sys.stdin.read(1)
    if value == '1':
        turnOn()
    elif value == '0':
        turnOff()

while True:
    readInput()
