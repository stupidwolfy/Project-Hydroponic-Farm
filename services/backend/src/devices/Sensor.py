from abc import ABC, abstractmethod
import time
import RPi.GPIO as GPIO
import Adafruit_ADS1x15
import random
import board
import busio
import adafruit_sht31d

GPIO.setmode(GPIO.BCM)

i2c = board.I2C()

def mapRange(value, inMin, inMax, outMin, outMax):
    return outMin + (((value - inMin) / (inMax - inMin)) * (outMax - outMin))

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
    def __init__(self, name, device_id, gain=2/3,  address=None):
        super().__init__(name, device_id, address)
        self.gain = gain
        self.values = [-1,-1,-1,-1]
        if (address is None):
            self.adc = Adafruit_ADS1x15.ADS1115()
        else:
            self.adc = Adafruit_ADS1x15.ADS1115(address)

    def update(self):
        self.values = [0]*4
        if (False): #Testmode
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
    #when loaded from file
    def __getinitargs__(self):
        return self.name, self.device_id, self.pin, self.pullUpDown

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

class WaterLevel(Sensor):
    #when loaded from file
    def __getinitargs__(self):
        return self.name, self.device_id, self.pinTrig, self.pinEcho, self.long, self.width

    def __init__(self, name, device_id, pinTrig, pinEcho, long, width):
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
    
class SHT31(I2cSensor):
    def __init__(self, name, device_id, address=None):
        super().__init__(name, device_id, address)
        self.sensor = adafruit_sht31d.SHT31D(i2c)

    def Get_temp(self):
        return round(self.sensor.temperature, 2)

    def Get_Humid(self):
        return round(self.sensor.relative_humidity, 2)

    