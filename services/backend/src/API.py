import requests
#import paho.mqtt.client as mqttClient
import time
import json
import base64
import sched
from typing import Callable, Tuple, List, Optional
from firebase import Firebase

from src.devices import CamHandler
from src import Config


class Repeatable:
    # To make some methode run repeatly
    # For performance safety, change interval to 1min (X60sec) instead of 1sec
    def PeriodicTask(self, func: Callable, interval: int, scheduler: sched.scheduler, args: Tuple):
        func(*args)
        scheduler.enter(interval*60, 1, self.PeriodicTask,
                        (func, interval, scheduler, args))


class Webhook(Repeatable):
    def __init__(self, name: str, url: str, bodyTemplate: str, sendCam: bool = True):
        self.name = name
        self.url = url
        self.bodyTemplate = bodyTemplate  # ex. """{"content": "test"}"""
        self.sendCam = sendCam

    def Send(self):
        body = self.bodyTemplate

        if self.sendCam:
            cam_img = CamHandler.GetImage(180)
            file = {'file': ('image.jpg', cam_img,
                             'image/jpeg', {'Expires': '0'})}
            #img_str = base64.b64encode(cam_img).decode()

        req = json.loads(body)
        res = requests.post(self.url, data=req, files=file)
        return res

    def PeriodicSend(self, interval, scheduler, args):
        return super().PeriodicTask(self.Send, interval, scheduler, args)


class MQTT(Repeatable):
    def __init__(self, name: str, broker_address: str, port: int, url: str, channel: str,  dataTemplate: str, user=None, password=None):
        self.name = name
        self.broker_address = broker_address
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


class FirebaseHandler(Repeatable):
    def __init__(self, allowed_data_name: List[str]= None):
        # <todo> connect to firebase without using email/password directly
        self.username = ""
        self.config = Config.firebase
        self.device_code = ""
        self.localId = ""
        self.isActivated = False
        if allowed_data_name is None:
            self.allowed_data_name = ["ph", "ec", "tds",
                                      "air-temp", "air-humid", "water-temp"]
            for i in range(8):
                self.allowed_data_name.append(f"relay-{i}")

        # ex.
        # config = {
        # "apiKey": "apiKey",
        # "authDomain": "projectId.firebaseapp.com",
        # "databaseURL": "https://databaseName.firebaseio.com",
        # "storageBucket": "projectId.appspot.com
        # }

        self.firebase = Firebase(self.config)
        self.auth = self.firebase.auth()
        self.db = self.firebase.database()

        # try:
        #    self.user = auth.sign_in_with_email_and_password(email, password)
        # except HTTPError as e:
        #    print("Firebase Login failed,please check email/password")
        #    self.user = None

    def Setup(self):
        # For Re-setup when load from file
        #self.firebase = Firebase(self.config)
        #self.auth = self.firebase.auth()
        self.RefreshToken()

    def RequestVerifyDevice(self) -> int:
        # Verify device by ask user to login and enter device code in web browser
        Result = requests.post("https://oauth2.googleapis.com/device/code",
                               data={"client_id": Config.oAuth2clientID, "scope": Config.scope})
        if Result.status_code == 200:
            deviceVerificationResult = Result.json()
            # self.user_code = deviceVerificationResult["user_code"] #Code to let user enter on web browser
            # self.verification_url = deviceVerificationResult["verification_url"] #url for user to login and enter Code
            self.device_code = deviceVerificationResult["device_code"]

            return {"user_code": deviceVerificationResult["user_code"], "verification_url": deviceVerificationResult["verification_url"]}
        else:
            return {"error": Result.status_code}

    def VerifyDevice(self) -> bool():
        # After user finish login / enter code on browser
        # Exchange device code to get id token
        Result = requests.post("https://oauth2.googleapis.com/token", data={
                               "client_id": Config.oAuth2clientID, "client_secret": Config.oAuth2clientSecret, "code": self.device_code, "grant_type": "http://oauth.net/grant_type/device/1.0"})
        if Result.status_code == 200:
            getUserIDTokenResult = Result.json()
            #self.id_token = getUserIDTokenResult["id_token"]
            Result = requests.post(f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithIdp?key={Config.firebase['apiKey']}", data={
                                   "postBody": f"id_token={getUserIDTokenResult['id_token']}&providerId=google.com", "requestUri": "http://localhost", "returnIdpCredential": True, "returnSecureToken": True})
            if Result.status_code == 200:
                LoginResult = Result.json()
                self.user = self.auth.refresh(LoginResult['refreshToken'])
                self.localId = LoginResult['localId']
                self.isActivated = True
                return True

        return False

    def RefreshToken(self):
        if self.isActivated:
            self.user = self.auth.refresh(self.user['refreshToken'])

    def AutoRefreshToken(self):
        return super().PeriodicTask(self.RefreshToken, 30, scheduler, args)

    def SendtoDB(self, data_name: str, data):
        if self.isActivated:
            if data_name in self.allowed_data_name:
                results = self.db.child(
                    f"users/{self.localId}/device").update({data_name: data}, self.user['idToken'])
            else:
                print(f"FirebaseDB ERROR: Not allow data_name: {data_name}")

    def AutoSendToDB(self, interval: int, scheduler: sched.scheduler, args: Tuple):
        return super().PeriodicTask(self.SendtoDB, interval, scheduler, args)
