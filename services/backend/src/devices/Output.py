from abc import ABC, abstractmethod
import time
import RPi.GPIO as GPIO
import random
from typing import Optional
from fastapi import Body
from typing import AnyStr, Callable, Tuple
import sched
from src import DBManager

GPIO.setmode(GPIO.BCM) # Use GPIOxx number

class Repeatable:
    #To make some methode run repeatly
    #For performance and safety, change interval to 1min (X60sec) instead of 1sec 
    def PeriodicTask(self, func:Callable, interval:int, scheduler:sched.scheduler, args:Tuple):
        func(*args)
        scheduler.enter(interval*60, 1, self.PeriodicTask,
                        (func, interval, scheduler, args))

class Relay(Repeatable):
    #when loaded from file
    def __getinitargs__(self):
        return self.name, self.device_id, self.pin, self.activeLOW

    def __init__(self, name: str = Body(""), device_id: int = Body(0), pin: int = Body(0), activeLOW: bool= Body(False), ininState: Optional[bool] = Body(False)):
        self.name = name
        self.pin = pin
        self.activeLOW = activeLOW
        self.device_id = device_id
        self.isOn = False
        
        GPIO.setup(self.pin, GPIO.OUT)  

        #if (not ininState is None):
        #    GPIO.output(self.pin, ininState)

    def ON(self):
        self.isON = True
        if (self.activeLOW is True):
            GPIO.output(self.pin, 0)
        else:
            GPIO.output(self.pin, 1)
        

    def OFF(self):
        self.isON = False
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

    def SaveToDB(self, db:DBManager.DBManager):
        db.CreateDataTable(self.name, ["data"])
        db.Append(self.name, [self.getState()])

    def AutoSaveToDB(self, interval:int, scheduler:sched.scheduler, args:Tuple):
        return super().PeriodicTask(self.SaveToDB, interval, scheduler, args)

