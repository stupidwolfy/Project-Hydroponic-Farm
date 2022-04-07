from abc import ABC, abstractmethod
import time
import RPi.GPIO as GPIO
import random
import board
import busio
import sched
from typing import AnyStr, Callable, Tuple
from src import DBManager

#import Adafruit_ADS1x15 DEPRECATED
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
import adafruit_sht31d

GPIO.setmode(GPIO.BCM)

i2c = board.I2C()

def mapRange(value, inMin, inMax, outMin, outMax):
    return outMin + (((value - inMin) / (inMax - inMin)) * (outMax - outMin))

class Repeatable:
    #For make some methode run repeatly
    #For performance safety, change interval to 1min (X60sec) instead of 1sec 
    def PeriodicTask(self, func:Callable, interval:int, scheduler:sched.scheduler, args:Tuple):
        func(*args)
        scheduler.enter(interval*60, 1, self.PeriodicTask,
                        (func, interval, scheduler, args))

class Sensor(ABC):
    @abstractmethod
    def __init__(self, name:str, device_id:int):
        self.name = name
        self.device_id = device_id
        self.data = None

class ADS1115(Sensor):
    def __init__(self, name:str, device_id:int, gain = 2/3, address=0x48):
        super().__init__(name, device_id)
        self.address = address
        self.adc = ADS.ADS1115(i2c, gain=gain, address=address)
        self.chan = [AnalogIn(self.adc, ADS.P0),AnalogIn(self.adc, ADS.P1),AnalogIn(self.adc, ADS.P2),AnalogIn(self.adc, ADS.P3)]

    def getVoltage(self, pointer:int):
        return self.chan[pointer].voltage

    def getVoltags(self):
        voltages = []
        for i in range(4):
            voltages[i] = self.chan[i].voltage
        return voltages

    def getValue(self, pointer:int):
        return self.chan[pointer].value

    def getValues(self):
        values = []
        for i in range(4):
            values[i] = self.chan[i].value
        return values

class AnalogSensor(Sensor):
    @abstractmethod
    def __init__(self, name:str, device_id:int, ADCDevice:ADS1115, ADCChannel:int):
        super().__init__(name, device_id)
        self.ADCDevice = ADCDevice
        self.ADCChannel = ADCChannel

class Switch(Sensor, Repeatable):
    #when loaded from file
    def __getinitargs__(self):
        return self.name, self.device_id, self.pin, self.pullUpDown

    def __init__(self, name:str, device_id:int, pin:int, pullUpDown:bool =None): #pullUpDown: True --> pullup | False --> pulldown | null --> not pull up/down):
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
        
    def SaveToDB(self, db:DBManager.DBManager):
        self.data = self.getState()
        db.CreateDataTable("Sensor_"+self.name, ["data"])
        db.Append("Sensor_"+self.name, [self.data])

    def PeriodicSaveToDB(self, interval:int, scheduler:sched.scheduler, args:Tuple):
        return super().PeriodicTask(self.SaveToDB, interval, scheduler, args)

    def getState(self):
        if (True): #Testmode
            gpioStates = [GPIO.HIGH, GPIO.LOW]
            return random.choice(gpioStates)
        else:
            return GPIO.input(self.pin)

class WaterLevel(Sensor):
    #when loaded from file
    def __getinitargs__(self):
        return self.name, self.device_id, self.pinTrig, self.pinEcho, self.long, self.width

    def __init__(self, name:str, device_id:int, pinTrig:int, pinEcho:int, long:int, width:int):
        super().__init__(name, device_id)
        self.long = long
        self.width = width
        self.pinTrig = pinTrig
        self.pinEcho = pinEcho
        self.emptyDistance = 100
        self.fullDistance = 10
        self.currentDistance = 10

        GPIO.setup(pinTrig, GPIO.OUT)
        GPIO.setup(pinEcho, GPIO.IN)

    def CalDistance(self):
        # set Trigger to HIGH
        GPIO.output(self.pinTrig, True)
     
        # set Trigger after 0.01ms to LOW
        time.sleep(0.00001)
        GPIO.output(self.pinTrig, False)
     
        StartTime = time.time()
        StopTime = time.time()
     
        # save StartTime
        while GPIO.input(self.pinEcho) == 0:
            StartTime = time.time()
     
        # save time of arrival
        while GPIO.input(self.pinEcho) == 1:
            StopTime = time.time()
     
        # time difference between start and arrival
        TimeElapsed = StopTime - StartTime
        # multiply with the sonic speed (34300 cm/s)
        # and divide by 2, because there and back
        distance = (TimeElapsed * 34300) / 2
        return distance

    def SetFullDistance(self):
        self.fullDistance = self.CalDistance()
        return self.fullDistance

    def SetEmptyDistance(self):
        self.emptyDistance = self.CalDistance()
        return self.emptyDistance

    def GetWaterLeft(self):
        self.currentDistance = self.CalDistance()

        waterLeftPercent = mapRange(self.currentDistance, self.fullDistance, self.emptyDistance, 0, 100)
        return waterLeftPercent
    
class SHT31(Sensor):
    def __init__(self, name:str, device_id:int, address=0x44):
        super().__init__(name, device_id)
        self.address = address
        self.sensor = adafruit_sht31d.SHT31D(i2c, address=address)

    def Get_temp(self):
        return round(self.sensor.temperature, 2)

    def Get_Humid(self):
        return round(self.sensor.relative_humidity, 2)

class PHSensor(AnalogSensor):
    """ Linear equation to calculate ph from analog value
    y = mx + b
    m is slope | b is intercept 
    y is ph [0..14] | x is analog value [0.00..1.00]
    ex..
       ph: analog
       4 : 0.615
       7 : 0.455
    
       m = (4-7)/(0.615-0.455) = -18.75
    """
    
    def __init__(self, name:str, device_id:int, ADCDevice:ADS1115, ADCChannel:int, m:float, b:float):
        super().__init__(name, device_id, ADCDevice, ADCChannel)
        self.m = m
        self.b = b

    #Get current PH, Must calibate first!
    def GetPH(self):
        x = self.ADCDevice.getVoltage(self.ADCChannel) / 5.00
        y = (self.m * x) + self.b
        return y

    #Get raw Voltage, for calibation
    def getVoltage(self):
        return self.ADCDevice.getVoltage(self.ADCChannel)
