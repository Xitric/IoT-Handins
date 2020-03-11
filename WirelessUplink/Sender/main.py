from machine import Pin, ADC, I2C
from micropython import const
import utime
from bh1750 import BH1750
from socket import socket
import select
from network import WLAN, STA_IF

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

    def connect(self, ip: str, port: int) -> socket:
        print("Try to connect")
        while not self.station.isconnected():
            print("Connect loop")
            # self.station.active(True)
            self.station.connect(self.ssid, self.pw)
            # print(self.station.isconnected())
            # print(self.station.status())
            utime.sleep(1)
        print("Now connected to WiFi")
        while True:
            try:
                self.connection.connect((ip, port))
                break
            except OSError as e:
                if e.args[0] not in [EHOSTUNREACH, ENONETWORK, ENOTCONN]:
                    raise
                utime.sleep(1)
        return self.connection

    # def is_connected(self) -> bool:
    #     if self.station.isconnected() and self.connection is not None:
    #         try:
    #             _, write_ready, _ = select.select([], [self.connection], [], 5)
    #         except select.error:
    #             self.connection.shutdown(2)
    #             self.connection.close()
    #             return False
    #     else:
    #         return False
    #
    #     return True


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
        while True:
            if self.current_state:
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
        self.wifi.connection = socket()
        while True:
            print("Connecting to host")
            try:
                self.wifi.connection.connect(('192.168.43.95', 5000))
                print("Connection established")
                self.state_machine.current_state = state_connected
                break
            except OSError as e:
                if e.args[0] == ENONETWORK:
                    print("Lost network")
                    self.state_machine.current_state = state_no_network
                    break
                elif e.args[0] != EHOSTUNREACH:
                    raise
                self.wifi.connection.close()
                self.wifi.connection = socket()
                utime.sleep(1)


class ConnectedState(State):
    def perform(self):
        print("Sending value")
        try:
            self.wifi.connection.sendall('Hello, world\n'.encode('utf-8'))
            led.on()
        except OSError as e:
            if e.args[0] not in [ECONNRESET, EHOSTUNREACH]:
                raise
            led.off()
            print("Lost connection to host")
            self.wifi.connection.close()
            self.state_machine.current_state = state_network


utime.sleep(5)
print("Hello :)")
wifi = WiFi('AndroidAP', 'vaqz2756')
import errno
state_machine = StateMachine()
state_no_network = NoNetworkState(state_machine, wifi)
state_network = NetworkState(state_machine, wifi)
state_connected = ConnectedState(state_machine, wifi)
state_machine.current_state = state_no_network


led = NetworkLed(33)
led.off()
state_machine.run()
# connection = wifi.connect('192.168.43.95', 5000)
# while True:
#     try:
#         connection.sendall('Hello, world\n'.encode('utf-8'))
#         led.on()
#     except OSError as e:
#         if e.args[0] not in [ECONNRESET, EHOSTUNREACH]:
#             raise
#         led.off()
#         connection = wifi.connect('192.168.43.95', 5000)

    # if not wifi.is_connected():
    #     led.off()
    #     connection = wifi.connect('192.168.43.95', 5000)
    # else:



# def enable_wifi() -> WLAN:
#     wifi_station = WLAN(STA_IF)
#     wifi_station.active(True)
#
#
#
#
#
#
# def connect() -> socket:
#
#     sta_if.connect('AndroidAP', 'vaqz2756')
#     s = socket()
#     s.connect(('192.168.43.95', 5000))
#     return s
#
#
# def update_network_status():
#     if sta_if.isconnected():
#         ledAzure.on()
#     else:
#         ledAzure.off()
#
#
# TEMP_IO = const(39)
# adc = ADC(Pin(TEMP_IO, Pin.IN))
# adc.atten(ADC.ATTN_6DB)
#
# I2C0_SCL = const(26)
# I2C0_SDA = const(25)
#
# scl = Pin(I2C0_SCL, Pin.IN)
# sda = Pin(I2C0_SDA, Pin.OUT)
# i2c = I2C(-1, scl=scl, sda=sda)
#
# light_sensor = BH1750(i2c)
#
# measurementCount = 0
# # socket = connect()
# while True:
#     update_network_status()
#     temperature = adc.read()
#     lightLevel = light_sensor.luminance(BH1750.CONT_HIRES_1)
#     measurementCount += 1
#
#     socket.sendall('{};{};{}'
#                    .format(temperature, lightLevel, measurementCount)
#                    .encode('utf-8'))
#
#     # Sample every 1 seconds
#     utime.sleep(1)
