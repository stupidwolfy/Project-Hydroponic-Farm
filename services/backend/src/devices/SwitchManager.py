import RPi.GPIO as GPIO
import random

GPIO.setmode(GPIO.BCM)   

class Switch:
    def __init__(self, name, id, pin, pullUpDown=None, testmode=False): #pullUpDown: True --> pullup | False --> pulldown | null --> not pull up/down):
        self.name = name
        self.pin = pin
        self.testMode = testmode

        if (pullUpDown is None):
            GPIO.setup(self.pin, GPIO.IN)  
        elif (pullUpDown is True):
            GPIO.setup(self.pin, GPIO.IN, pull_up_down =GPIO.PUD_UP)
        else:
            GPIO.setup(self.pin, GPIO.IN, pull_up_down =GPIO.PUD_DOWN)

    def getState(self):
        if (self.testMode is True):
            gpioStates = [GPIO.HIGH, GPIO.LOW]
            return random.choice(gpioStates)
        else:
            return GPIO.input(self.pin)