from typing import Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

import io
from starlette.responses import StreamingResponse
import RPi.GPIO as GPIO
import cv2

from src import CamHandler, ADS1x15Manager, RelayManager, SwitchManager

pumps = []
adcs = []
Switchs = []

pumpA = RelayManager.Relay('Pump A', id=pumps.count, pin=17)
pumps.append(pumpA)
pumpB = RelayManager.Relay('Pump B', id=pumps.count, pin=27)
pumps.append(pumpB)

adc = ADS1x15Manager.ADS1115("adc A", id=adcs.count) # i2c pin, default address
adcs.append(adc)

waterLMSW = SwitchManager.Switch("Water LMSW", id=Switchs.count, pin=18)
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

@app.get("/pump/{number}/{power}")
async def pump_pow(number: int, power: bool):
    try:
        #Pumps code
        if power:
            pumps[number].ON()
        else:
            pumps[number].OFF()
        return {pumps[number].name: power}
    except IndexError:
        raise HTTPException(status_code=404, detail="Item not found")

@app.get("/pump/{number}")
async def pump_state(number: int):
    try:
        return {pumps[number].name:pumps[number].isON}
    except IndexError:
        raise HTTPException(status_code=404, detail="Item not found")

@app.get("/cam")
async def cam_stillImage():
    live_img = CamHandler.GetImage()
    return StreamingResponse(io.BytesIO(live_img.tobytes()), media_type="image/jpg")