from machine import Pin, ADC, I2C, RTC
from micropython import const
import utime
from bh1750 import BH1750
from socket import socket
from network import WLAN, STA_IF
import time_manager as ntptime
import secrets

ECONNRESET = 104
EHOSTUNREACH = 113
ENONETWORK = 118


class WiFi:

    def __init__(self, ssid: str, pw: str):
        self.station = WLAN(STA_IF)
        self.station.active(True)
        self.ssid = ssid
        self.pw = pw
        self.connection = None

    def renew_connection(self):
        if self.connection:
            self.connection.close()

        self.connection = socket()


class NetworkLed:

    def __init__(self, pin: int):
        self.led = Pin(pin, Pin.OUT)

    def on(self):
        self.led.on()

    def off(self):
        self.led.off()


class StateMachine:
    def __init__(self):
        self.current_state = None

    def run(self):
        previous_state = None
        while previous_state != self.current_state and self.current_state:
            previous_state = self.current_state
            self.current_state.perform()


class State:

    def __init__(self, state_machine: StateMachine, wifi: WiFi):
        self.state_machine = state_machine
        self.wifi = wifi

    def perform(self):
        pass


class NoNetworkState(State):
    def perform(self):
        while not self.wifi.station.isconnected():
            print("Trying to connect to WiFi")
            self.wifi.station.connect(self.wifi.ssid, self.wifi.pw)
            utime.sleep(1)
        print("WiFi enabled")
        self.state_machine.current_state = state_network


class NetworkState(State):
    def perform(self):
        self.wifi.renew_connection()
        while True:
            print("Connecting to host")
            try:
                self.wifi.connection.connect(('192.168.87.24', 5000))
                print("Connection established")
                self.state_machine.current_state = state_connected
                break
            except OSError as e:
                if e.args[0] == ENONETWORK:
                    print("Lost network")
                    self.state_machine.current_state = state_no_network
                    break
                elif e.args[0] not in [EHOSTUNREACH, ECONNRESET]:
                    raise
                self.wifi.renew_connection()
                utime.sleep(1)


class ConnectedState(State):

    def __init__(self, state_machine: StateMachine, wifi: WiFi):
        super().__init__(state_machine, wifi)
        self.measurement_count = 0

    def perform(self):
        print("Sending values")
        ntptime.settime()
        while True:
            try:
                self.measurement_count += 1
                send_time = RTC().datetime()
                temperature = adc.read()
                light_level = light_sensor.luminance(BH1750.CONT_HIRES_1)

                self.wifi.connection.sendall('{};{};{};{};'
                                             .format(self.measurement_count, send_time, temperature, light_level)
                                             .encode('utf-8'))
                led.on()
                utime.sleep(10)
            except OSError as e:
                if e.args[0] not in [ECONNRESET, EHOSTUNREACH]:
                    raise
                led.off()
                print("Lost connection to host")
                self.state_machine.current_state = state_network
                break


utime.sleep(5)
wifi = WiFi(secrets.network_ssid, secrets.network_password)
led = NetworkLed(33)
led.off()

state_machine = StateMachine()
state_no_network = NoNetworkState(state_machine, wifi)
state_network = NetworkState(state_machine, wifi)
state_connected = ConnectedState(state_machine, wifi)
state_machine.current_state = state_no_network

TEMP_IO = const(39)
adc = ADC(Pin(TEMP_IO, Pin.IN))
adc.atten(ADC.ATTN_6DB)

I2C0_SCL = const(26)
I2C0_SDA = const(25)

scl = Pin(I2C0_SCL, Pin.IN)
sda = Pin(I2C0_SDA, Pin.OUT)
i2c = I2C(-1, scl=scl, sda=sda)

light_sensor = BH1750(i2c)

state_machine.run()
