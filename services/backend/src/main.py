import dbm
from typing import Optional
from fastapi import FastAPI, HTTPException
from fastapi_utils.tasks import repeat_every
from fastapi.middleware.cors import CORSMiddleware

import random
import io
#from services.backend.src import ADCManager
from starlette.responses import StreamingResponse
import RPi.GPIO as GPIO
import cv2
import json

from src import ADCManager, CamHandler, RelayManager, SwitchManager, DBManager

# init
relays = []
adcs = []
Switchs = []

tempData = []

db = DBManager.SqlLite("Sensor_history")

db.CreateDataTable("Garden_A_Sensor", ["Temp", "Humid", "PH", "EC", "Water_Temp", "Water_LMSW"])
db.CreateDataTable("Garden_A_Output", ["Pump_A", "Pump_B", "LED"])

#test add new record
db.Append("Garden_A_Sensor", [25, 50, 6.2, 2.22, 28, 0])

pumpA = RelayManager.Relay('Pump A', id=relays.count, pin=17)
relays.append(pumpA)
pumpB = RelayManager.Relay('Pump B', id=relays.count, pin=27)
relays.append(pumpB)

led = RelayManager.Relay('led', id=relays.count, pin=22)
relays.append(led)

adc = ADCManager.ADS1115("adc A", id=adcs.count) # i2c pin, default address
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

# Main Fastapi 
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
async def relay_control(number: int, power: bool):
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
async def switch_state(number: int):
    try:
        return {"name":Switchs[number].name, "value":Switchs[number].getState == 0}
    except IndexError:
        raise HTTPException(status_code=404, detail="Item not found")

@app.get("/sensor/temp")
async def get_temp():
    return {"temp": round(random.uniform(26, 27), 1), "humid": random.randrange(50, 60)}

@app.get("/sensor/temp/raw")
async def get_temp_raw():
    return {"temp": round(random.uniform(26, 27), 1), "humid": random.randrange(50, 60)}

@app.get("/sensor/water_temp")
async def get_water_temp():
    return {"temp": round(random.uniform(25, 26), 1)}

@app.get("/sensor/ph")
async def get_ph():
    return {"ph": round(random.uniform(6.0, 7.0), 2)}

@app.get("/sensor/ec")
async def get_ec():
    return {"ec": round(random.uniform(1.6, 1.9), 2), "unit": "(dS/m)"} #dS/m

@app.get("/cam")
async def get_image():
    live_img = CamHandler.GetImage(180)
    return StreamingResponse(io.BytesIO(live_img.tobytes()), media_type="image/jpg")

@app.get("/data/{dataTableName}")
async def get_record(dataTableName: str):
    return db.GetRecords(dataTableName)

@app.get("/data")
async def get_record_tables():
    return db.GetRecords()