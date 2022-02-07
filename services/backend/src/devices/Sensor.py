from abc import ABC, abstractmethod
import time
import RPi.GPIO as GPIO
import Adafruit_ADS1x15
import random

GPIO.setmode(GPIO.BCM)


class Sensor(ABC):
    @abstractmethod
    def __init__(self, name, device_id, db):
        self.name = name
        self.device_id = device_id
        self.db = db
        self.save_interval = 60
        self.data = None

    def PeriodicBackgroundSave(self, scheduler):
        #schedule next save
        scheduler.enter(self.save_interval, 1, self.PeriodicBackgroundSave,
                         (scheduler))
        
        #Save to db
        self.db.CreateDataTable("Sensor_"+self.name, ["data"])
        self.db.Append("Sensor_"+self.name, [self.data])

    def StartBackgroundSave(self, db):
        self.db = db

class I2cSensor(Sensor):
    @abstractmethod
    def __init__(self, name, device_id, db, address):
        super().__init__(name, device_id, db)
        self.address = address


class AnalogSensor(Sensor):
    @abstractmethod
    def __init__(self, name, device_id, db, analogDevice):
        super(AnalogSensor, self).__init__(name, device_id, db)
        self.analogDevice = analogDevice

class ADS1115(I2cSensor):
    def __init__(self, name, device_id, db, gain=1,  address=None):
        super().__init__(name, device_id, db, address)
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

class Switch(Sensor):
    def __init__(self, name, device_id, db, pin, pullUpDown=None): #pullUpDown: True --> pullup | False --> pulldown | null --> not pull up/down):
        super().__init__(name, device_id, db)
        self.pin = pin
        self.pullUpDown = pullUpDown

        if (pullUpDown is None):
            GPIO.setup(self.pin, GPIO.IN)  
        elif (pullUpDown is True):
            GPIO.setup(self.pin, GPIO.IN, pull_up_down =GPIO.PUD_UP)
        else:
            GPIO.setup(self.pin, GPIO.IN, pull_up_down =GPIO.PUD_DOWN)
    
    def PeriodicBackgroundSave(self, scheduler):
        self.data = self.getState()
        super(Switch, self).PeriodicBackgroundSave(scheduler)

    def StartBackgroundSave(self, db, scheduler):
        super().StartBackgroundSave(db)
        self.PeriodicBackgroundSave(scheduler)

    def getState(self):
        if (True): #Testmode
            gpioStates = [GPIO.HIGH, GPIO.LOW]
            return random.choice(gpioStates)
        else:
            return GPIO.input(self.pin)