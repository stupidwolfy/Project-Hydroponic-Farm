from abc import ABC, abstractmethod
import time
import RPi.GPIO as GPIO
import random
from typing import Optional
from fastapi import Body

GPIO.setmode(GPIO.BCM)   

class Relay:
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

