from typing import Optional
from fastapi import FastAPI

import io
from fastapi.responses import FileResponse
from src import CamHandler

import RPi.GPIO as GPIO

pumpA_GPIO = 17
pumpB_GPIO = 27

GPIO.setmode(GPIO.BCM)   

GPIO.setup(pumpA_GPIO, GPIO.OUT)  
GPIO.setup(pumpB_GPIO, GPIO.OUT)  

app = FastAPI()


@app.get("/")
def home():
    return {"Hello": "World"}

@app.get("/pumpA/{power}")
def pumpA_pow(power: bool):
    #Pump A code
    if power:
        GPIO.output(pumpA_GPIO, 1)   
    else:
        GPIO.output(pumpA_GPIO, 0)   
    return {"pumpA": power}

@app.get("/pumpB/{power}")
def pumpB_pow(power: bool):
    #Pump B on code
    if power:
        GPIO.output(pumpB_GPIO, 1)   
    else:
        GPIO.output(pumpB_GPIO, 0)   
    return {"pumpB": power}

@app.get("/cam")
def cam_endpoint():
    im_png = CamHandler.GetImage()
    #return StreamingResponse(io.BytesIO(im_png.tobytes()), media_type="image/png")
    return FileResponse(im_png)
