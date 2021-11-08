import time
# Import the ADS1x15 module.
import Adafruit_ADS1x15
import random

class ADS1115:
    def __init__(self, name, id, gain=1,  address=None, testmode=False):
        self.name = name
        self.gain = gain
        self.testMode = testmode
        if (address is None):
            self.adc = Adafruit_ADS1x15.ADS1115()
        else:
            self.adc = Adafruit_ADS1x15.ADS1115(address)

    def update(self):
        self.values = [0]*4
        if (self.testMode is True):
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
