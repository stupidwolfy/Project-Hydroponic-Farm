import RPi.GPIO as GPIO
from pydantic import BaseModel, BaseConfig, create_model

GPIO.setmode(GPIO.BCM)   

class Relay:
    def __init__(self, name, id, pin, activeLOW=False, ininState = None):
        self.name = name
        self.pin = pin
        self.activeLOW = activeLOW
        self.id = id
        
        GPIO.setup(self.pin, GPIO.OUT)  

        if (not ininState is None):
            GPIO.output(self.pin, ininState)

    def ON(self):
        if (self.activeLOW is True):
            GPIO.output(self.pin, 0)
        else:
            GPIO.output(self.pin, 1)

    def OFF(self):
        if (self.activeLOW is True):
            GPIO.output(self.pin, 1)
        else:
            GPIO.output(self.pin, 0) 

    def setState(self, state):
        GPIO.output(self.pin, state)   
    
    def isON(self):
        if (self.activeLOW == True):
            return GPIO.input(self.pin) == 0
        else:
            return GPIO.input(self.pin) == 1

    def getState(self):
        return GPIO.input(self.pin)