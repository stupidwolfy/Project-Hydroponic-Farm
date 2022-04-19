from abc import ABC, abstractmethod
import time
import RPi.GPIO as GPIO
import random
from typing import AnyStr, Callable, Tuple, Optional
import sched
from src import DBManager
from pydantic import BaseModel

GPIO.setmode(GPIO.BCM)  # Use GPIOxx number



class Repeatable:
    # To make some methode run repeatly
    # For performance safety, change interval to 1min (X60sec) instead of 1sec
    def PeriodicTask(self, func: Callable, interval: int, scheduler: sched.scheduler, args: Tuple):
        func(*args)
        scheduler.enter(interval*60, 1, self.PeriodicTask,
                        (func, interval, scheduler, args))


class Relay(Repeatable):
    # when loaded from file
    # def __getinitargs__(self):
        # GPIO.setup(self.pin, GPIO.OUT)
        # return self.name, self.device_id, self.pin, self.activeLOW

    def __init__(self, name: str, device_id: int, pin: int, activeLOW=False, autoSaveInterval = 30):
        self.name = name
        self.pin = pin
        self.activeLOW = activeLOW
        self.device_id = device_id
        self.isOn = False
        self.autoSaveInterval = autoSaveInterval

        GPIO.setup(self.pin, GPIO.OUT)
        if (self.activeLOW is True):
            GPIO.output(self.pin, 1)
        else:
            GPIO.output(self.pin, 0)

    def Setup(self):
        GPIO.setup(self.pin, GPIO.OUT)
        if (self.activeLOW is True):
            GPIO.output(self.pin, 1)
        else:
            GPIO.output(self.pin, 0)
        
    def ON(self):
        self.isON = True
        try:
            if (self.activeLOW is True):
                GPIO.output(self.pin, 0)
            else:
                GPIO.output(self.pin, 1)
            
        except RuntimeError:
            self.Setup()
            if (self.activeLOW is True):
                GPIO.output(self.pin, 0)
            else:
                GPIO.output(self.pin, 1)

    def OFF(self):
        self.isON = False
        try:
            if (self.activeLOW is True):
                GPIO.output(self.pin, 1)
            else:
                GPIO.output(self.pin, 0)
            
        except RuntimeError:
            self.Setup()
            if (self.activeLOW is True):
                GPIO.output(self.pin, 1)
            else:
                GPIO.output(self.pin, 0)

    def setState(self, state):
        GPIO.output(self.pin, state)

    def isON(self):
        # if (self.activeLOW == True):
        #     return GPIO.input(self.pin) == 0
        # else:
        #     return GPIO.input(self.pin) == 1
        return self.isON

    def getState(self):
        return GPIO.input(self.pin)

    def SaveToDB(self, db: DBManager.DBManager):
        self.data = self.getState()
        db.CreateDataTable(self.name, ["data"])
        db.Append(self.name, [self.data])

    def AutoSaveToDB(self, scheduler: sched.scheduler, args: Tuple):
        return super().PeriodicTask(self.SaveToDB, self.autoSaveInterval, scheduler, args)


class RelayModel(BaseModel):
    name: str
    #device_id: int
    #pin: int
    activeLOW: bool