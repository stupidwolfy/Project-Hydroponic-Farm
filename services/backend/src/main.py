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

from src import DBManager, FileManager, API, Nutrient
from src.devices import Output, Sensor, CamHandler

HOST_HOSTNAME = os.getenv('HOST_HOSTNAME')

devices = FileManager.LoadObjFromJson("devices.json")
apis = FileManager.LoadObjFromJson("apis.json")
nutrientManager = FileManager.LoadObjFromJson("nutrientManager.json")

GPIO.cleanup()


# create device if no json file
if devices is None:
    print("Device config file not found, createing...")
    devices = {'relays': [], 'sensor': {}}

    # Create Relay
    relay1 = Output.Relay('Fertilizer-A', device_id=0,
                          pin=24, ratePerSec=0.65, activeLOW=True)
    relay2 = Output.Relay('Fertilizer-B', device_id=1,
                          pin=17, ratePerSec=0.65, activeLOW=True)
    relay3 = Output.Relay('PH-Down-Agent', device_id=2,
                          pin=18, ratePerSec=0.65, activeLOW=True)
    relay4 = Output.Relay('LED-1', device_id=3, pin=22, activeLOW=True)
    relay5 = Output.Relay('LED-2', device_id=4, pin=5, activeLOW=True)
    relay6 = Output.Relay('FAN-1', device_id=5, pin=6, activeLOW=True)
    relay7 = Output.Relay('Pump-Add-Water', device_id=6,
                          pin=13, activeLOW=True)
    relay8 = Output.Relay('Pump-Cycle', device_id=7, pin=26, activeLOW=True)

    devices['relays'] = [relay1, relay2, relay3,
                         relay4, relay5, relay6, relay7, relay8]
    devices['sensor']['switchs'] = Sensor.Switch(
        "Water-LMSW", device_id=0, pin=18)

    devices['sensor']['water-temp'] = Sensor.TempSensor(
        "water-temp", 0, 4, "00-780000000000")

    # Create i2c device (ADS1115 and SHT31)
    devices['sensor']['adc'] = Sensor.ADS1115(
        "ADC", device_id=0)  # i2c pin, default address

    devices['sensor']['sht31'] = Sensor.SHT31("air-indoor", 0)

    # Create Analog device if adc is connected
    if 'adc' in devices['sensor']:
        devices['sensor']['ph'] = Sensor.PHSensor(
            "ph", 0, devices['sensor']['adc'], 0)
        devices['sensor']['tds'] = Sensor.TDSSensor(
            "tds", 0, devices['sensor']['adc'], 2)

    saveResult = FileManager.SaveObjAsJson("devices.json", devices)
    print(f"Devices created: {saveResult}")

else:
    for relay in devices['relays']:
        relay.Setup()

    if 'water-temp' in devices['sensor']:
        devices['sensor']['water-temp'].Setup()

    if 'adc' in devices['sensor']:
        devices['sensor']['adc'].Setup()
    if 'sht31' in devices['sensor']:
        devices['sensor']['sht31'].Setup()
    if 'switchs' in devices['sensor']:
        devices['sensor']['switchs'].Setup()

    print(f"Devices loaded")

# create api if no json file
if apis is None:
    apis = {}
    allowedDataName = ["switchs", "temp", "humid", "ph", "water-temp", "tds"]
    for i in range(8):
        allowedDataName.append(f"relay-{i}")
    apis['cloud'] = API.FirebaseHandler(allowedDataName)

    saveResult = FileManager.SaveObjAsJson("apis.json", apis)
    print(f"Apis created: {saveResult}")

else:
    apis['cloud'].Setup()
    print(f"Apis loaded")


if nutrientManager is None:
    nutrientManager = Nutrient.NutrientManager(0)

    saveResult = FileManager.SaveObjAsJson(
        "nutrientTables.json", nutrientManager)
    print(f"NutrientManager created: {saveResult}")

else:
    nutrientManager.Setup()
    print("nutrientManager loaded")

# do background save sensor data to DB
dbThread = DBManager.SqlLite("Sensor_history")
scheduler = sched.scheduler(time.time, time.sleep)


def Background_DBAutoSave():
    #dbThread = DBManager.SqlLite("Sensor_history")

    # init scheduler
    #scheduler = sched.scheduler(time.time, time.sleep)
    apis['cloud'].AutoRefreshToken(scheduler)

    if 'switchs' in devices['sensor']:
        devices['sensor']['switchs'].AutoSaveToDB(scheduler, (dbThread,))
        apis['cloud'].AutoSendToDB(
            scheduler, ("switchs", devices['sensor']['switchs'].getState()))
    if 'sht31' in devices['sensor']:
        devices['sensor']['sht31'].AutoSaveToDB(scheduler, (dbThread,))
        apis['cloud'].AutoSendToDB(
            scheduler, ("temp", devices['sensor']['sht31'].Get_temp()))
        apis['cloud'].AutoSendToDB(
            scheduler, ("humid", devices['sensor']['sht31'].Get_Humid()))
    if 'ph' in devices['sensor']:
        devices['sensor']['ph'].AutoSaveToDB(scheduler, (dbThread,))
        apis['cloud'].AutoSendToDB(
            scheduler, ("ph", devices['sensor']['ph'].GetPH()))
    if 'water-temp' in devices['sensor']:
        devices['sensor']['water-temp'].AutoSaveToDB(scheduler, (dbThread,))
        apis['cloud'].AutoSendToDB(
            scheduler, ("water-temp", devices['sensor']['water-temp'].GetTemp()))
    if 'tds' in devices['sensor']:
        devices['sensor']['tds'].AutoSaveToDB(
            scheduler, (dbThread, devices['sensor']['water-temp']))
        apis['cloud'].AutoSendToDB(
            scheduler, ("tds", devices['sensor']['tds'].GetPPM(devices['sensor']['water-temp'].GetTemp())))

    for i, relay in enumerate(devices['relays']):
        relay.AutoSaveToDB(scheduler, (dbThread,))
        apis['cloud'].AutoSendToDB(scheduler, (f"relay-{i}", relay.getState()))

    # scheduler.run()


# Start a thread to run the events
Background_DBAutoSave()
t1 = threading.Thread(target=scheduler.run)
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


# @app.get("/manager")
# async def device_manager():
#     return {"Hello": "ssss"}


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
        new_relay = Output.Relay(
            new_relay, devices['relays'][number].device_id, devices['relays'][number].pin)

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


@app.get("/relay/on_by_rate/{number}/{amount}")
async def relay_control(number: int, amount: int):
    try:
        await devices['relays'][number].OnRate(amount)
        return {devices['relays'][number].name: amount}
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


@app.get("/sensor/water_temp")
async def get_water_temp():
    return {"water_temp": devices['sensor']['water-temp'].GetTemp()}


@app.get("/sensor/ph")
async def get_ph(reset: bool = None, calibrate: bool = None, refPH: float = None):
    if calibrate is not None and refPH is not None:
        result = devices['sensor']['ph'].AddCalibratePoint(refPH)
        FileManager.SaveObjAsJson("devices.json", devices)
        if result:
            return {"status": "ok"}
        else:
            return {"status": "error"}
    elif reset is not None:
        devices['sensor']['ph'].ResetCalibratePoint()
        FileManager.SaveObjAsJson("devices.json", devices)
        return {"status": "ok"}
    else:
        return {"ph": devices['sensor']['ph'].GetPH()}


@app.get("/sensor/tds")
async def get_tds(getVoltage: bool = None):
    if getVoltage is None:
        tds = devices['sensor']['tds'].GetPPM(
            devices['sensor']['water-temp'].GetTemp())
        ec = (tds * 2)
        return {"tds": tds, "unit-tds": "ppm", "ec": ec, "unit-ec": "uS/cm"}
    else:
        return {"voltage": devices['sensor']['tds'].getVoltage()}


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
async def get_records(dataTableName: str, limit: int = -1):
    try:
        return db.GetRecords(dataTableName, limit)
    except OperationalError as e:
        return {"status": "Error", "detail": str(e)}


@app.get("/cloud/status")
async def cloud_status():
    return {"verified": apis['cloud'].isActivated}


@app.get("/cloud/setup")
async def cloud_setup(verified: bool = None) -> dict:
    if not verified:
        requestVerifyData = apis['cloud'].RequestVerifyDevice()
        return requestVerifyData

    else:
        verifyCompleated = apis['cloud'].VerifyDevice()
        if verifyCompleated:
            saveResult = FileManager.SaveObjAsJson("apis.json", apis)
        return {"result": verifyCompleated}

# Websocket test


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    data = await websocket.receive_text()
    await websocket.send_json({"got": data})
    if data == "temp":
        try:
            while True:
                await websocket.send_json({"temp": devices['sensor']['sht31'].Get_temp()})
                await asyncio.sleep(5)
        except IndexError:
            await websocket.send_json({"status": "Error", "detail": "Device is not connected."})

    elif data == "humid":
        try:
            while True:
                await websocket.send_json({"humid": devices['sensor']['sht31'].Get_Humid()})
                await asyncio.sleep(5)
        except IndexError:
            await websocket.send_json({"status": "Error", "detail": "Device is not connected."})

    elif data == "ph":
        try:
            while True:
                await websocket.send_json({"ph": devices['sensor']['ph'].GetPH()})
                await asyncio.sleep(1)
        except IndexError:
            await websocket.send_json({"status": "Error", "detail": "Device is not connected."})

    elif data == "tds":
        try:
            while True:
                tds = devices['sensor']['tds'].GetPPM(
                    devices['sensor']['water-temp'].GetTemp())
                ec = (tds * 2)
                await websocket.send_json({"tds": tds, "unit-tds": "ppm", "ec": ec, "unit-ec": "uS/cm"})
                await asyncio.sleep(1)
        except IndexError:
            await websocket.send_json({"status": "Error", "detail": "Device is not connected."})
    else:
        await websocket.send_json({"status": "Error", "detail": "No data."})
