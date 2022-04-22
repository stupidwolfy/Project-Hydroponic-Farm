from abc import ABC, abstractmethod
import time
import RPi.GPIO as GPIO
import random
import board
import busio
import sched
from typing import AnyStr, Callable, Tuple, Optional
from src import DBManager
# import Adafruit_ADS1x15 # DEPRECATED
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
import adafruit_sht31d
import math
from pydantic import BaseModel

GPIO.setmode(GPIO.BCM)

i2c = board.I2C()


class Repeatable:
    # To make some methode run repeatly
    # For performance safety, change interval to 1min (X60sec) instead of 1sec
    def PeriodicTask(self, func: Callable, interval: int, scheduler: sched.scheduler, args: Tuple):
        func(*args)
        scheduler.enter(interval*60, 1, self.PeriodicTask,
                        (func, interval, scheduler, args))


class Sensor(ABC):
    @abstractmethod
    def __init__(self, name: str, device_id: int):
        self.name = name
        self.device_id = device_id
        self.data = None


class ADS1115(Sensor):
    def __init__(self, name: str, device_id: int, gain=2/3, address=0x48):
        super().__init__(name, device_id)
        self.address = address
        self.gain = gain
        self.isActivated = False

        self.Setup()

    def Setup(self):
        # Re setup adc, to make sure correct gain is used
        try:
            self.adc = ADS.ADS1115(i2c, gain=self.gain, address=self.address)
            self.chan = [AnalogIn(self.adc, ADS.P0), AnalogIn(
                self.adc, ADS.P1), AnalogIn(self.adc, ADS.P2), AnalogIn(self.adc, ADS.P3)]
            self.isActivated = True
        except ValueError:
            self.isActivated = False

    def getVoltage(self, pointer: int):
        if self.isActivated:
            return self.chan[pointer].voltage

    def getVoltags(self):
        if self.isActivated:
            voltages = []
            for i in range(4):
                voltages[i] = self.chan[i].voltage
            return voltages

    def getValue(self, pointer: int):
        if self.isActivated:
            return self.chan[pointer].value

    def getValues(self):
        if self.isActivated:
            values = []
            for i in range(4):
                values[i] = self.chan[i].value
            return values


class AnalogSensor(Sensor):
    """ AnalogSensor is Use to convert anoalog value 
    from ads1115 to desire output for each hardware"""
    @abstractmethod
    def __init__(self, name: str, device_id: int, ADCDevice: ADS1115, ADCChannel: int):
        super().__init__(name, device_id)
        self.ADCDevice = ADCDevice
        self.ADCChannel = ADCChannel


class Switch(Sensor, Repeatable):
    # when loaded from file
    def __getinitargs__(self):
        return self.name, self.device_id, self.pin, self.pullUpDown

    # pullUpDown: True --> pullup | False --> pulldown | null --> not pull up/down):
    def __init__(self, name: str, device_id: int, pin: int, pullUpDown: bool = None, autoSaveInterval=30):
        super().__init__(name, device_id)
        self.pin = pin
        self.pullUpDown = pullUpDown
        self.autoSaveInterval = autoSaveInterval

        # do optional pull up / pull down
        if (self.pullUpDown is None):
            GPIO.setup(self.pin, GPIO.IN)
        elif (self.pullUpDown is True):
            GPIO.setup(self.pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        else:
            GPIO.setup(self.pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    def Setup(self):
        if (self.pullUpDown is None):
            GPIO.setup(self.pin, GPIO.IN)
        elif (self.pullUpDown is True):
            GPIO.setup(self.pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        else:
            GPIO.setup(self.pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    def SaveToDB(self, db: DBManager.DBManager):
        self.data = self.getState()
        db.CreateDataTable(self.name, ["data"])
        db.Append(self.name, [self.data])

    def AutoSaveToDB(self, scheduler: sched.scheduler, args: Tuple):
        return super().PeriodicTask(self.SaveToDB, self.autoSaveInterval, scheduler, args)

    def getState(self):
        return GPIO.input(self.pin)


class WaterLevel(Sensor, Repeatable):
    # when loaded from file
    def __getinitargs__(self):
        return self.name, self.device_id, self.pinTrig, self.pinEcho, self.long, self.width

    def __init__(self, name: str, device_id: int, pinTrig: int, pinEcho: int, long: int, width: int, autoSaveInterval=30):
        super().__init__(name, device_id)
        self.long = long
        self.width = width
        self.pinTrig = pinTrig
        self.pinEcho = pinEcho
        self.emptyDistance = None
        self.fullDistance = None
        self.currentDistance = None
        self.autoSaveInterval = autoSaveInterval

        GPIO.setup(self.pinTrig, GPIO.OUT)
        GPIO.setup(self.pinEcho, GPIO.IN)

    def Setup(self):
        GPIO.setup(self.pinTrig, GPIO.OUT)
        GPIO.setup(self.pinEcho, GPIO.IN)

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

    def mapRange(value, inMin, inMax, outMin, outMax):
        return outMin + (((value - inMin) / (inMax - inMin)) * (outMax - outMin))

    def GetWaterLeft(self):
        if(self.emptyDistance is None | self.fullDistance is None | self.currentDistance is None):
            raise IOError("Distance is not set.")
        self.currentDistance = self.CalDistance()
        waterLeftPercent = self.mapRange(
            self.currentDistance, self.fullDistance, self.emptyDistance, 0, 100)
        return waterLeftPercent

    def SaveToDB(self, db: DBManager.DBManager):
        db.CreateDataTable(self.name, ["data"])
        db.Append(self.name, [self.GetWaterLeft()])

    def AutoSaveToDB(self, scheduler: sched.scheduler, args: Tuple):
        return super().PeriodicTask(self.SaveToDB, self.autoSaveInterval, scheduler, args)


class SHT31(Sensor, Repeatable):
    def __init__(self, name: str, device_id: int, address=0x44, autoSaveInterval=30):
        super().__init__(name, device_id)
        self.address = address
        self.autoSaveInterval = autoSaveInterval
        self.isActivated = False

        self.Setup()

    def Setup(self):
        try:
            self.sensor = adafruit_sht31d.SHT31D(i2c, address=self.address)
            self.isActivated = True
        except ValueError:
            self.isActivated = False

    def Get_temp(self):
        if self.isActivated:
            return round(self.sensor.temperature, 2)

    def Get_Humid(self):
        if self.isActivated:
            return round(self.sensor.relative_humidity, 2)

    def SaveToDB(self, db: DBManager.DBManager):
        if self.isActivated:
            db.CreateDataTable(self.name+"-temperature", ["data"])
            db.CreateDataTable(self.name+"-humidity", ["data"])
            db.Append(self.name+"-temperature", [self.Get_temp()])
            db.Append(self.name+"-humidity", [self.Get_Humid()])

    def AutoSaveToDB(self, scheduler: sched.scheduler, args: Tuple):
        return super().PeriodicTask(self.SaveToDB, self.autoSaveInterval, scheduler, args)


class TempSensor(AnalogSensor, Repeatable):
    def __init__(self, name: str, device_id: int, ADCDevice: ADS1115, ADCChannel: int, multiplier: float = 10, autoSaveInterval=30):
        super().__init__(name, device_id, ADCDevice, ADCChannel)
        self.multiplier = multiplier
        self.autoSaveInterval = autoSaveInterval

    # Get raw Voltage, for calibation
    def getVoltage(self):
        return self.ADCDevice.getVoltage(self.ADCChannel)

    def GetTemp(self):
        voltage = self.getVoltage()
        if voltage is not None:
            return voltage*self.multiplier

    def SaveToDB(self, db: DBManager.DBManager):
        temp = self.GetTemp()
        if temp is not None:
            db.CreateDataTable(self.name, ["data"])
            db.Append(self.name, [temp])

    def AutoSaveToDB(self, scheduler: sched.scheduler, args: Tuple):
        return super().PeriodicTask(self.SaveToDB, self.autoSaveInterval, scheduler, args)


class PHSensor(AnalogSensor, Repeatable):
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

    def __init__(self, name: str, device_id: int, ADCDevice: ADS1115, ADCChannel: int, m: float = -1, b: float = -1, autoSaveInterval=30):
        super().__init__(name, device_id, ADCDevice, ADCChannel)
        self.m = m
        self.b = b
        self.autoSaveInterval = autoSaveInterval
        self.calibrationV = []
        self.calibrationPH = []
        #y = mx + b
        #y is ph
        #x is voltage

    def Setm(self, m):
        self.m = m

    def Setb(self, b):
        self.b = b

    # Get raw Voltage, for calibation
    def getVoltage(self):
        return self.ADCDevice.getVoltage(self.ADCChannel)

    def AddCalibratePoint(self, refPH):
        if len(self.calibrationPH) < 2:
            self.calibrationV.append(self.getVoltage())
            self.calibrationPH.append(refPH)
            if len(self.calibrationPH) == 2:
                self.m = (self.calibrationPH[1] - self.calibrationPH[0]) / (self.calibrationV[1] - self.calibrationV[0])
                self.b = ((self.calibrationPH[0] + self.calibrationPH[1]) - (self.m * (self.calibrationV[0] + self.calibrationV[1])))/2
            return True
        else:
            return False

    def ResetCalibratePoint(self):
        self.calibrationV = []
        self.calibrationPH = []
        self.m = -1
        self.b = -1

    # Get current PH, Must calibate first!
    def GetPH(self):
        if len(self.calibrationPH) < 2:
            return -1
        
        rawPH = []
        for i in range(10):
            voltage = self.ADCDevice.getVoltage(self.ADCChannel)
            if voltage is not None:
              #x = voltage / 5.00
              x = voltage
              y = (self.m * x) + self.b
              rawPH.append(y)
        return sum(rawPH)/len(rawPH) 

    def SaveToDB(self, db: DBManager.DBManager):
        if self.m > 0 and self.b > 0:
            ph = self.GetPH()
            if ph is not None:
                db.CreateDataTable(self.name, ["data"])
                db.Append(self.name, [ph])

    def AutoSaveToDB(self, scheduler: sched.scheduler, args: Tuple):
        return super().PeriodicTask(self.SaveToDB, self.autoSaveInterval, scheduler, args)


class TDSSensor(AnalogSensor, Repeatable):
    def __init__(self, name: str, device_id: int, ADCDevice: ADS1115, ADCChannel: int, autoSaveInterval=30):
        super().__init__(name, device_id, ADCDevice, ADCChannel)
        self.autoSaveInterval = autoSaveInterval

    # Get raw Voltage, for calibation
    def getVoltage(self):
        return self.ADCDevice.getVoltage(self.ADCChannel)

    def GetPPM(self, waterTemp: float):
        voltage = self.getVoltage()
        if voltage is not None:
            compensationCoefficient = 1.0+0.02*(waterTemp-25.0)
            compensationVolatge = voltage / compensationCoefficient
            tdsValue = (133.42*math.pow(compensationVolatge, 3) - 255.86*math.pow(compensationVolatge, 2)
                        + 857.39*compensationVolatge)*0.5
            return tdsValue

    def SaveToDB(self, db: DBManager.DBManager, tempSensor: TempSensor):
        temp = tempSensor.GetTemp()
        if temp is not None:
            ppm = self.GetPPM(tempSensor.GetTemp())
            if ppm is not None:
                db.CreateDataTable(self.name, ["data"])
                db.Append(self.name, [ppm])

    def AutoSaveToDB(self, scheduler: sched.scheduler, args: Tuple):
        return super().PeriodicTask(self.SaveToDB, self.autoSaveInterval, scheduler, args)

# Model class


class SHT31Model(BaseModel):
    name: str
    device_id: int
    address: int


class TempSensorModel(BaseModel):
    name: str
    device_id: int
    ADCDevice: ADS1115
    ADCChannel: int
    multiplier: Optional[float]

    class Config:
        arbitrary_types_allowed = True


class PHSensorModel(BaseModel):
    name: str
    device_id: int
    ADCDevice: ADS1115
    ADCChannel: int
    m: Optional[float]
    b: Optional[float]

    class Config:
        arbitrary_types_allowed = True


class TDSSensorModel(BaseModel):
    name: str
    device_id: int
    ADCDevice: ADS1115
    ADCChannel: int

    class Config:
        arbitrary_types_allowed = True
