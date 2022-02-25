import requests
#import paho.mqtt.client as mqttClient
import time
import json
import base64

from src.devices import CamHandler

class Repeatable:
    #For make some methode run repeatly
    #For performance safety, change interval to 1min (X60sec) instead of 1sec 
    def PeriodicTask(self, func, interval, scheduler, args):
        func(*args)
        scheduler.enter(interval*60, 1, self.PeriodicTask,
                        (func, interval, scheduler, args))

class Webhook(Repeatable):
    def __init__(self, name, url, bodyTemplate, sendCam=True):
        self.name = name
        self.url = url
        self.bodyTemplate = bodyTemplate #ex. """{"content": "test"}"""
        self.sendCam = sendCam
        

    def Send(self):
        body = self.bodyTemplate

        if self.sendCam:
            cam_img = CamHandler.GetImage(180)
            file = {'file': ('image.jpg', cam_img, 'image/jpeg', {'Expires': '0'})}
            #img_str = base64.b64encode(cam_img).decode()
        
        req = json.loads(body)
        res = requests.post(self.url, data=req, files=file)
        return res

    def PeriodicSend(self, interval, scheduler, args):
        return super().PeriodicTask(self.Send, interval, scheduler, args)

class MQTT(Repeatable):
    def __init__(self, name, broker_address, port, url, channel,  dataTemplate, user=None, password=None):
        self.name = name
        self.broker_address =broker_address
        self.port = port
        self.url = url
        self.user = user
        self.password = password
        self.channel = channel
        self.dataTemplate = dataTemplate

    def Publish(self):
        pass

    def PeriodicPublish(self, interval, scheduler, args):
        return super().PeriodicTask(self.Publish, interval, scheduler, args)