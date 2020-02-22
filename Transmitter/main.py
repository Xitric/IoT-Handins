import machine
import sys

ledAzure = machine.Pin(33, machine.Pin.OUT)
ledWifi = machine.Pin(32, machine.Pin.OUT)

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

turnOff()
while True:
    readInput()
