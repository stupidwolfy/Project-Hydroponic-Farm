import dbm
from typing import Optional
from fastapi import FastAPI, HTTPException, Depends, WebSocket
from fastapi_utils.tasks import repeat_every
from fastapi.middleware.cors import CORSMiddleware

import time
import sched
import asyncio
import threading
import random
import io
import os
from starlette.responses import StreamingResponse
from sqlite3 import OperationalError
import RPi.GPIO as GPIO

from src import DBManager, FileManager

from src.devices import Output, Sensor, CamHandler

HOST_HOSTNAME = os.getenv('HOST_HOSTNAME')

devices = FileManager.LoadObjFromJson("devices.json")
GPIO.cleanup()
# create device if no json file
if devices is None:
    print("Device config file not found, createing...")
    devices = {'relays': [], 'sensor': {}}

    # Create Relay
    relay1 = Output.Relay('Fertilizer-A', device_id=0, pin=24, activeLOW=True)
    relay2 = Output.Relay('Fertilizer-B', device_id=1, pin=17, activeLOW=True)
    relay3 = Output.Relay('PH-Down-Agent', device_id=2, pin=18, activeLOW=True)
    relay4 = Output.Relay('LED-1', device_id=3, pin=22, activeLOW=True)
    relay5 = Output.Relay('LED-2', device_id=4, pin=5, activeLOW=True)
    relay6 = Output.Relay('FAN-1', device_id=5, pin=6, activeLOW=True)
    relay7 = Output.Relay('Pump-Add-Water', device_id=6, pin=13, activeLOW=True)
    relay8 = Output.Relay('Pump-Cycle', device_id=7, pin=26, activeLOW=True)

    devices['relays'] = [relay1, relay2, relay3,
                         relay4, relay5, relay6, relay7, relay8]
    devices['sensor']['switchs'] = Sensor.Switch(
        "Water-LMSW", device_id=0, pin=18)

    # Create i2c device (ADS1115 and SHT31)
    try:
        devices['sensor']['adc'] = Sensor.ADS1115(
            "ADC", device_id=0)  # i2c pin, default address
    except ValueError:
        print("SENSOR ERROR: ADC is not connected.")
    try:
        devices['sensor']['sht31'] = Sensor.SHT31("air-indoor", 0)
    except ValueError:
        print("SENSOR ERROR: SHT31 is not connected.")

    # Create Analog device if adc is connected
    if 'adc' in devices['sensor']:
        devices['sensor']['ph'] = Sensor.PHSensor(
            "ph", 0, devices['sensor']['adc'], 0)
        devices['sensor']['water-temp'] = Sensor.TempSensor(
            "water-temp", 0, devices['sensor']['adc'], 1)
        devices['sensor']['tds'] = Sensor.TempSensor(
            "tds", 0, devices['sensor']['adc'], 2)

    saveResult = FileManager.SaveObjAsJson("devices.json", devices)
    print(f"Save result: {saveResult}")

else:
    for relay in devices['relays']:
        relay.Setup()

    if 'adc' in devices['sensor']:
        devices['sensor']['adc'].Setup()
    if 'sht31' in devices['sensor']:
        devices['sensor']['sht31'].Setup()
    if 'switchs' in devices['sensor']:
        devices['sensor']['switchs'].Setup()

# do background save sensor data to DB

def Background_DBAutoSave():
    dbThread = DBManager.SqlLite("Sensor_history")

    # init scheduler
    scheduler = sched.scheduler(time.time, time.sleep)
    if 'switchs' in devices['sensor']:
        devices['sensor']['switchs'].AutoSaveToDB(30, scheduler, (dbThread,))
    if 'sht31' in devices['sensor']:
        devices['sensor']['sht31'].AutoSaveToDB(30, scheduler, (dbThread,))
    if 'ph' in devices['sensor']:
        devices['sensor']['ph'].AutoSaveToDB(30, scheduler, (dbThread,))
    if 'water-temp' in devices['sensor']:
        devices['sensor']['water-temp'].AutoSaveToDB(
            30, scheduler, (dbThread,))
    if 'tds' in devices['sensor']:
        devices['sensor']['tds'].AutoSaveToDB(
            30, scheduler, (dbThread, devices['sensor']['water-temp']))

    for relay in devices['relays']:
        relay.AutoSaveToDB(30, scheduler, (dbThread,))

    scheduler.run()

# Start a thread to run the events
t1 = threading.Thread(target=Background_DBAutoSave)
t1.setDaemon(True)
t1.start()

db = DBManager.SqlLite("Sensor_history")

# init Fastapi
app = FastAPI()

origins = [
    "http://pi-zero.local:8080",
    "http://pi-Project.local:8080",
    "http://raspberrypi.local:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=[f"http://{HOST_HOSTNAME}.local:8080"],
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


@app.get("/relay")
async def get_relays():
    return{"Relays": devices['relays']}


@app.get("/relay/{number}")
async def pump_state(number: int):
    try:
        return {devices['relays'][number]}
    except IndexError:
        return {"status": "Error", "detail": "Device not found."}


@app.put("/relay/{number}")
async def edit_relay(number: int, new_relay: Output.RelayModel):
    if len(devices['relays']) >= number:
        new_relay = Output.Relay(new_relay, devices['relays'][number].device_id, devices['relays'][number].pin)

        devices['relays'][number] = new_relay
        FileManager.SaveObjAsJson("devices.json", devices)
        return {"status": "ok", "detail": new_relay}
    else:
        return {"status": "Error", "detail": f"Relay ID {number} does not exist."}


@app.get("/relay/{number}/{power}")
async def relay_control(number: int, power: bool):
    try:
        # Pumps code
        if power:
            devices['relays'][number].ON()
        else:
            devices['relays'][number].OFF()
        return {devices['relays'][number].name: power}
    except IndexError:
        return {"status": "Error", "detail": "Device not found."}


@app.get("/switch")
async def switch_state():
    try:
        return {"name": devices['sensor']['switchs'].name, "value": devices['sensor']['switchs'].getState() == 0}
    except IndexError:
        return {"status": "Error", "detail": "Device not found."}

    except KeyError:
        return {"status": "Error", "detail": "Device not setup."}

@app.get("/sensor/temp")
async def get_temp():
    try:
        temp = devices['sensor']['sht31'].Get_temp()
        humid = devices['sensor']['sht31'].Get_Humid()
        return {"temp": temp, "humid": humid}
    except IndexError:
        return {"status": "Error", "detail": "Device is not connected."}
    
    except KeyError:
        return {"status": "Error", "detail": "Device is not setup."}


@app.websocket("/sensor/temp")
async def websocket_get_ph(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            temp = devices['sensor']['sht31'].Get_temp()
            humid = devices['sensor']['sht31'].Get_Humid()
            await websocket.send_json({"temp": temp, "humid": humid})
            await asyncio.sleep(1)
    except IndexError:
        await websocket.send_json({"status": "Error", "detail": "Device is not connected."})


@app.get("/sensor/water_temp")
async def get_water_temp():
    return {"temp": round(random.uniform(25, 26), 1)}


@app.get("/sensor/ph")
async def get_ph():
    try:
        if 'ph' in devices['sensor']:
            return {"ph": devices['sensor']['ph'].GetPH()}
        else:
            return {"ph": round(random.uniform(6.0, 7.0), 2), "Testmode": True}
    except ValueError as e:
        return {"status": "Error", "detail": str(e)}


@app.websocket("/sensor/ph")
async def websocket_get_ph(websocket: WebSocket):
    await websocket.accept()
    try:
        if 'ph' in devices['sensor']:
            while True:
                await websocket.send_json({"ph": devices['sensor']['ph'].GetPH()})
                await asyncio.sleep(1)
        else:
            while True:
                await websocket.send_json({"ph": round(random.uniform(6.0, 7.0), 2), "Testmode": True})
                await asyncio.sleep(1)
    except ValueError as e:
        await websocket.send_json({"status": "Error", "detail": str(e)})


@app.get("/sensor/ec")
async def get_ec():
    return {"ec": round(random.uniform(1.6, 1.9), 2), "unit": "(dS/m)"}  # dS/m


@app.get("/cam")
async def get_image():
    live_img = CamHandler.GetImage(180)
    if live_img is None:
        return {"status": "Error", "detail": "Device not found."}
    return StreamingResponse(io.BytesIO(live_img.tobytes()), media_type="image/jpg")


@app.get("/data")
async def get_record_tables():
    return db.GetRecords()


@app.get("/data/{dataTableName}")
async def get_records(dataTableName: str):
    try:
        return db.GetRecords(dataTableName)
    except OperationalError as e:
        return {"status": "Error", "detail": str(e)}


# Websocket test

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"Message text was: {data}")
