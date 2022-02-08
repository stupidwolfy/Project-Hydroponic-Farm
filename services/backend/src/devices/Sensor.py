from abc import ABC, abstractmethod
import time
import RPi.GPIO as GPIO
import Adafruit_ADS1x15
import random

GPIO.setmode(GPIO.BCM)


class Repeatable:
    #For make some methode run repeatly
    #For performance safety, change interval to 1min (X60sec) instead of 1sec 
    def PeriodicTask(self, func, interval, scheduler, args):
        func(*args)
        scheduler.enter(interval*60, 1, self.PeriodicTask,
                        (func, interval, scheduler, args))

class Sensor(ABC):
    @abstractmethod
    def __init__(self, name, device_id):
        self.name = name
        self.device_id = device_id
        self.data = None

class I2cSensor(Sensor):
    @abstractmethod
    def __init__(self, name, device_id, address):
        super().__init__(name, device_id)
        self.address = address

class AnalogSensor(Sensor):
    @abstractmethod
    def __init__(self, name, device_id, analogDevice):
        super(AnalogSensor, self).__init__(name, device_id)
        self.analogDevice = analogDevice

class ADS1115(I2cSensor):
    def __init__(self, name, device_id, gain=1,  address=None):
        super().__init__(name, device_id, address)
        self.gain = gain
        if (address is None):
            self.adc = Adafruit_ADS1x15.ADS1115()
        else:
            self.adc = Adafruit_ADS1x15.ADS1115(address)

    def update(self):
        self.values = [0]*4
        if (True): #Testmode
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

class Switch(Sensor, Repeatable):
    def __init__(self, name, device_id, pin, pullUpDown=None): #pullUpDown: True --> pullup | False --> pulldown | null --> not pull up/down):
        super().__init__(name, device_id)
        self.pin = pin
        self.pullUpDown = pullUpDown

        #do optional pull up / pull down 
        if (pullUpDown is None):
            GPIO.setup(self.pin, GPIO.IN)  
        elif (pullUpDown is True):
            GPIO.setup(self.pin, GPIO.IN, pull_up_down =GPIO.PUD_UP)
        else:
            GPIO.setup(self.pin, GPIO.IN, pull_up_down =GPIO.PUD_DOWN)
        
    def SaveToDB(self, db):
        self.data = self.getState()
        db.CreateDataTable("Sensor_"+self.name, ["data"])
        db.Append("Sensor_"+self.name, [self.data])

    def PeriodicSaveToDB(self, interval, scheduler, args):
        return super().PeriodicTask(self.SaveToDB, interval, scheduler, args)

    def getState(self):
        if (True): #Testmode
            gpioStates = [GPIO.HIGH, GPIO.LOW]
            return random.choice(gpioStates)
        else:
            return GPIO.input(self.pin)