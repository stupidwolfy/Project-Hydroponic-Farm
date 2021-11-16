from typing import Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

import random
import io
from starlette.responses import StreamingResponse
import RPi.GPIO as GPIO
import cv2
import json

from src import CamHandler, ADS1x15Manager, RelayManager, SwitchManager

relays = []
adcs = []
Switchs = []

pumpA = RelayManager.Relay('Pump A', id=relays.count, pin=17)
relays.append(pumpA)
pumpB = RelayManager.Relay('Pump B', id=relays.count, pin=27)
relays.append(pumpB)

led = RelayManager.Relay('led', id=relays.count, pin=22)
relays.append(led)

adc = ADS1x15Manager.ADS1115("adc A", id=adcs.count) # i2c pin, default address
adcs.append(adc)

waterLMSW = SwitchManager.Switch("Water LMSW", id=Switchs.count, pin=18,testmode=True)
Switchs.append(waterLMSW)

app = FastAPI()

origins = [
    "http://localhost:8080/",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def home():
    return {"Hello": "World"}

@app.get("/manager")
async def device_manager():
    return {"Hello": "ssss"}

#@app.get("/pump/add", )
#def pumpA_pow(new_pump: RelayManager.Relay):
#    ## %Todo Add dynamic create new pump
#    return {"status":"Pump xxx added", "new_pump":new_pump.name}

@app.get("/relay/{number}/{power}")
async def pump_pow(number: int, power: bool):
    try:
        #Pumps code
        if power:
            relays[number].ON()
        else:
            relays[number].OFF()
        return {relays[number].name: power}
    except IndexError:
        raise HTTPException(status_code=404, detail="Item not found")

@app.get("/relay/{number}")
async def pump_state(number: int):
    try:
        return {relays[number].name:relays[number].isON is True}
    except IndexError:
        raise HTTPException(status_code=404, detail="Item not found")

@app.get("/switch/{number}")
async def pump_state(number: int):
    try:
        return {"name":Switchs[number].name, "value":Switchs[number].getState == 0}
    except IndexError:
        raise HTTPException(status_code=404, detail="Item not found")

@app.get("/sensor/temp")
async def cam_stillImage():
    return {"temp": round(random.uniform(26, 27), 1), "humid": random.randrange(50, 60)}

@app.get("/sensor/water_temp")
async def cam_stillImage():
    return {"temp": round(random.uniform(25, 26), 1)}

@app.get("/sensor/ph")
async def cam_stillImage():
    return {"ph": round(random.uniform(6.0, 7.0), 2)}

@app.get("/sensor/ec")
async def cam_stillImage():
    return {"ec": round(random.uniform(1.6, 1.9), 2), "unit": "(dS/m)"} #dS/m

@app.get("/cam")
async def cam_stillImage():
    live_img = CamHandler.GetImage()
    return StreamingResponse(io.BytesIO(live_img.tobytes()), media_type="image/jpg")