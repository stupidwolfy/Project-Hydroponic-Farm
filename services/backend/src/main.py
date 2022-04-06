import dbm
from typing import Optional
from fastapi import FastAPI, HTTPException, Depends, WebSocket
from fastapi_utils.tasks import repeat_every
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

import time
import sched
import asyncio
import threading
import random
import io
import os
from starlette.responses import StreamingResponse
import RPi.GPIO as GPIO

from src import DBManager, FileManager

from src.devices import Output, Sensor, CamHandler

HOST_HOSTNAME = os.getenv('HOST_HOSTNAME')

#tempData = []

devices = FileManager.LoadObjFromJson("devices.json")
#create device if no json file
if devices is None:
    devices = {'output':{ 'relays': []},'sensor':{ 'adcs': [], 'switchs': [], 'air-temp': []}}

    #Test create device object. Should remove after Load/Save json is coded
    pumpA = Output.Relay('Pump A', device_id=0, pin=17)
    devices['output']['relays'].append(pumpA)
    pumpB = Output.Relay('Pump B', device_id=1, pin=27)
    devices['output']['relays'].append(pumpB)
    
    led = Output.Relay('led', device_id=2, pin=22)
    devices['output']['relays'].append(led)
    
    adc = Sensor.ADS1115("adc A", device_id=0) # i2c pin, default address
    devices['sensor']['adcs'].append(adc)
    
    waterLMSW = Sensor.Switch("Water LMSW", device_id=0, pin=18)
    devices['sensor']['switchs'].append(waterLMSW)
    waterLMSW2 = Sensor.Switch("Water LMSW222", device_id=1, pin=19)
    devices['sensor']['switchs'].append(waterLMSW2)
    waterLMSW3 = Sensor.Switch("Water LMSW3333333", device_id=2, pin=20)
    devices['sensor']['switchs'].append(waterLMSW3)

    airtempSensor = Sensor.SHT31("air temp indoor", 0)
    devices['sensor']['air-temp'].append(airtempSensor)
    
    FileManager.SaveObjAsJson("devices.json", devices)

#do background save sensor data to DB
def Background_DBAutoSave():
    #Test wirte to database. should removed after Auto-save sensor function is coded
    dbThread = DBManager.SqlLite("Sensor_history")
    dbThread.CreateDataTable("Garden_A_Sensor", ["Temp", "Humid", "PH", "EC", "Water_Temp", "Water_LMSW"])
    dbThread.CreateDataTable("Garden_A_Output", ["Pump_A", "Pump_B", "LED"])
    #test add new record
    dbThread.Append("Garden_A_Sensor", [25, 50, 6.2, 2.22, 28, 0])

    #init scheduler
    scheduler = sched.scheduler(time.time, time.sleep)
    devices['sensor']['switchs'][0].PeriodicSaveToDB(30, scheduler, (dbThread,))
    devices['sensor']['switchs'][1].PeriodicSaveToDB(30, scheduler, (dbThread,))
    devices['sensor']['switchs'][2].PeriodicSaveToDB(30, scheduler, (dbThread,))
    #devices['EC sensor'][0].PeriodicSaveToDB(1, scheduler, (db,))
    #devices['PH sensor'][0].PeriodicSaveToDB(1, scheduler, (db,))
    #devices['Light sensor'][0].PeriodicSaveToDB(1, scheduler, (db,))
    #devices['Water level'][0].PeriodicSaveToDB(1, scheduler, (db,))
    
    scheduler.run()

# Start a thread to run the events
t1 = threading.Thread(target=Background_DBAutoSave)
t1.setDaemon(True)
t1.start()

db = DBManager.SqlLite("Sensor_history")

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
#def pumpA_pow(new_pump: Output.Relay):
#    ## %Todo Add dynamic create new pump
#    return {"status":"Pump xxx added", "new_pump":new_pump.name}

#Get request
@app.get("/relay")
async def get_relays():
    return{"Relays":devices['output']['relays']}

@app.get("/relay/{number}")
async def pump_state(number: int):
    try:
        return {devices['output']['relays'][number]}
    except IndexError:
        raise HTTPException(status_code=404, detail="Item not found")

@app.get("/relay/{number}/{power}")
async def relay_control(number: int, power: bool):
    try:
        #Pumps code
        if power:
            devices['output']['relays'][number].ON()
        else:
            devices['output']['relays'][number].OFF()
        return {devices['output']['relays'][number].name: power}
    except IndexError:
        raise HTTPException(status_code=404, detail="Item not found")

@app.get("/switch/{number}")
async def switch_state(number: int):
    try:
        return {"name":devices['sensor']['switchs'][number].name, "value":devices['sensor']['switchs'][number].getState == 0}
    except IndexError:
        raise HTTPException(status_code=404, detail="Item not found")

@app.get("/sensor/temp")
async def get_temp():
    temp = devices['sensor']['air-temp'][0].Get_temp()
    humid = devices['sensor']['air-temp'][0].Get_Humid()
    #return {"temp": round(random.uniform(26, 27), 1), "humid": random.randrange(50, 60)}
    return {"temp": temp, "humid": humid}

@app.websocket("/sensor/temp")
async def websocket_get_ph(websocket: WebSocket):
    await websocket.accept()
    while True:
        await websocket.send_json({"temp": round(random.uniform(26, 27), 1), "humid": random.randrange(50, 60)})
        await asyncio.sleep(1)

@app.get("/sensor/temp/raw")
async def get_temp_raw():
    return {"temp": round(random.uniform(26, 27), 1), "humid": random.randrange(50, 60)}

@app.get("/sensor/water_temp")
async def get_water_temp():
    return {"temp": round(random.uniform(25, 26), 1)}

@app.get("/sensor/ph")
async def get_ph():
    return {"ph": round(random.uniform(6.0, 7.0), 2)}

@app.websocket("/sensor/ph")
async def websocket_get_ph(websocket: WebSocket):
    await websocket.accept()
    while True:
        await websocket.send_json({"ph": round(random.uniform(6.0, 7.0), 2)})
        await asyncio.sleep(1)

@app.get("/sensor/ec")
async def get_ec():
    return {"ec": round(random.uniform(1.6, 1.9), 2), "unit": "(dS/m)"} #dS/m

@app.get("/cam")
async def get_image():
    live_img = CamHandler.GetImage(180)
    if live_img is None:
        raise HTTPException(status_code=404, detail="Camera not found")
    return StreamingResponse(io.BytesIO(live_img.tobytes()), media_type="image/jpg")

@app.get("/data")
async def get_record_tables():
    return db.GetRecords()

@app.get("/data/{dataTableName}")
async def get_records(dataTableName: str):
    return db.GetRecords(dataTableName)

#Post request
@app.post("/relay")
async def add_relay(new_relay : Output.Relay = Depends()):
    #<todo> Add new relay to device list, then save it to json file
    #check if device-id and pin of new device in not duplicate
    if not any(saved_relay.device_id == new_relay.device_id for saved_relay in devices['output']['relays'])\
    and not any(saved_relay.pin == new_relay.pin for saved_relay in devices['output']['relays']):
      devices['output']['relays'].append(new_relay)
      FileManager.SaveObjAsJson("devices.json", devices)
      return {"status": "ok", "new_device": new_relay}
    else:
        if any(saved_relay.device_id == new_relay.device_id for saved_relay in devices['output']['relays']):
          return {"status": "Error. Duplicate device_id, try another"}
        else:
          return {"status": "Error. Duplicate GPIO pin, try another"}

#Websocket
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"Message text was: {data}")