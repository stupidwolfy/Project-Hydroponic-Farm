from abc import ABC, abstractmethod
import time
import RPi.GPIO as GPIO
import Adafruit_ADS1x15
import random

GPIO.setmode(GPIO.BCM)   

class Sensor(ABC):
    @abstractmethod
    def __init__(self, name, device_id):
        self.name = name
        self.device_id = device_id

    @abstractmethod
    def StartBackgroundRead(self):
        pass

class I2cSensor(Sensor):
    @abstractmethod
    def __init__(self, name, device_id, address):
        super(I2cSensor, self).__init__(name, device_id)
        self.address = address

    def StartBackgroundRead(self):
        pass

class AnalogSensor(Sensor):
    @abstractmethod
    def __init__(self, name, device_id, analogDevice):
        super(AnalogSensor, self).__init__(name, device_id)
        self.analogDevice = analogDevice

class ADS1115(I2cSensor):
    def __init__(self, name, device_id, gain=1,  address=None):
        super(ADS1115, self).__init__(name, device_id, address)
        self.gain = gain
        if (address is None):
            self.adc = Adafruit_ADS1x15.ADS1115()
        else:
            self.adc = Adafruit_ADS1x15.ADS1115(address)

    def update(self):
        self.values = [0]*4
        if (self.testMode is True):
            for i in range(4):
                self.values[i] = random.randint(0, 1023)
        else:
            for i in range(4):
                self.values[i] = self.adc.read_adc(i, gain=self.gain)

    def get_Value(self, pointer):
        return self.values[pointer]

    def get_Values(self):
        return self.values

    def set_Gain(self, gain):
        self.gain = gain

    def set_Name(self, name):
        self.name = name

class Switch(Sensor):
    def __init__(self, name, device_id, pin, pullUpDown=None): #pullUpDown: True --> pullup | False --> pulldown | null --> not pull up/down):
        super(Switch, self).__init__(name, device_id)
        self.pin = pin
        self.pullUpDown = pullUpDown

        if (pullUpDown is None):
            GPIO.setup(self.pin, GPIO.IN)  
        elif (pullUpDown is True):
            GPIO.setup(self.pin, GPIO.IN, pull_up_down =GPIO.PUD_UP)
        else:
            GPIO.setup(self.pin, GPIO.IN, pull_up_down =GPIO.PUD_DOWN)

    def StartBackgroundRead(self):
        super(Switch, self).StartBackgroundRead()

    def getState(self):
        if (self.testMode is True):
            gpioStates = [GPIO.HIGH, GPIO.LOW]
            return random.choice(gpioStates)
        else:
            return GPIO.input(self.pin)