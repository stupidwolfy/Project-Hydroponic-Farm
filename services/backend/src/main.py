import dbm
from typing import Optional
from fastapi import FastAPI, HTTPException
from fastapi_utils.tasks import repeat_every
from fastapi.middleware.cors import CORSMiddleware

import random
import io
import os
from starlette.responses import StreamingResponse
import RPi.GPIO as GPIO

from src import DBManager, FileManager

from src.devices import ADCManager, CamHandler, RelayManager, SwitchManager

HOST_HOSTNAME = os.getenv('HOST_HOSTNAME')

#tempData = []

#Test wirte to database. should removed after Auto-save sensor function is coded
db = DBManager.SqlLite("Sensor_history")

db.CreateDataTable("Garden_A_Sensor", ["Temp", "Humid", "PH", "EC", "Water_Temp", "Water_LMSW"])
db.CreateDataTable("Garden_A_Output", ["Pump_A", "Pump_B", "LED"])

#test add new record
db.Append("Garden_A_Sensor", [25, 50, 6.2, 2.22, 28, 0])

devices = FileManager.LoadObjFromJson("devices.json")

if devices is None:
    devices = {'relays': [], 'adcs': [],'switchs': [], 'camera': []}
    
    #Test create device object. Should remove after Load/Save json is coded
    pumpA = RelayManager.Relay('Pump A', id=len(devices['relays']), pin=17)
    devices['relays'].append(pumpA)
    pumpB = RelayManager.Relay('Pump B', id=len(devices['relays']), pin=27)
    devices['relays'].append(pumpB)
    
    led = RelayManager.Relay('led', id=len(devices['relays']), pin=22)
    devices['relays'].append(led)
    
    adc = ADCManager.ADS1115("adc A", id=len(devices['adcs'])) # i2c pin, default address
    devices['adcs'].append(adc)
    
    waterLMSW = SwitchManager.Switch("Water LMSW", id=len(devices['switchs']), pin=18,testmode=True)
    devices['switchs'].append(waterLMSW)
    
    FileManager.SaveObjAsJson("devices.json", devices)

#init Fastapi
app = FastAPI()

origins = [
    "http://pi-zero.local:8080",
    "http://pi-Project.local:8080",
    "http://raspberrypi.local:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins= [f"http://{HOST_HOSTNAME}.local:8080"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#Main Fastapi 
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
            devices['relays'][number].ON()
        else:
            devices['relays'][number].OFF()
        return {devices['relays'][number].name: power}
    except IndexError:
        raise HTTPException(status_code=404, detail="Item not found")

@app.get("/relay/{number}")
async def pump_state(number: int):
    try:
        return {devices['relays'][number].name:devices['relays'][number].isON is True}
    except IndexError:
        raise HTTPException(status_code=404, detail="Item not found")

@app.get("/switch/{number}")
async def switch_state(number: int):
    try:
        return {"name":devices['switchs'][number].name, "value":devices['switchs'][number].getState == 0}
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

@app.get("/data")
async def get_record_tables():
    return db.GetRecords()

@app.get("/data/{dataTableName}")
async def get_records(dataTableName: str):
    return db.GetRecords(dataTableName)
