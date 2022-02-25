from abc import ABC, abstractmethod
import time
import RPi.GPIO as GPIO
import Adafruit_ADS1x15
import random

GPIO.setmode(GPIO.BCM)   

class Relay:
    #if loaded from file
    def __getinitargs__(self):
        return self.name, self.device_id, self.pin, self.activeLOW, self.ininState

    def __init__(self, name, device_id, pin, activeLOW=False, ininState = None):
        self.name = name
        self.pin = pin
        self.activeLOW = activeLOW
        self.device_id = device_id
        self.isOn = False
        
        GPIO.setup(self.pin, GPIO.OUT)  

        if (not ininState is None):
            GPIO.output(self.pin, ininState)

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

