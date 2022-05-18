from src import DBManager, FileManager
from src.devices import Output, Sensor
from typing import List, Tuple, Callable
from pydantic import BaseModel
from datetime import date
import sched
import asyncio

class Repeatable:
    # To make some methode run repeatly
    # For performance safety, change interval to 1min (X60sec) instead of 1sec
    def PeriodicTask(self, func: Callable, interval: int, scheduler: sched.scheduler, args: Tuple):
        func(*args)
        scheduler.enter(interval*60, 1, self.PeriodicTask,
                        (func, interval, scheduler, args))


class NutrientRow(BaseModel):
    #day: int
    minEC: float
    maxPH: float


class NutrientTable(BaseModel):
    id: int
    name: str
    nutrientFeedAmount: int
    nutrientABGapTime: int
    phDownFeedAmount: int
    nutrientRows: List[NutrientRow]


class NutrientManager(Repeatable):
    def __init__(self, activeTableID: int, startDate: date = None, adjustNutrientInterval=5):
        if startDate is None:
            self.startDate = date.today()
        else:
            self.startDate = startDate

        self.activeTableID = activeTableID
        self.adjustNutrientInterval = adjustNutrientInterval
        self.activate = False

        self.Setup()

    def Setup(self):
        nutrientTables = FileManager.LoadObjFromJson("nutrientTables.json")

        # create nutrientTable if no json file
        if nutrientTables is None:
            nutrientTables = []
            exampleRow = NutrientRow(minEC=2, maxPH=8)
            exampleTable = NutrientTable(
                id=len(nutrientTables), name="standard",nutrientFeedAmount=5, nutrientABGapTime=15, phDownFeedAmount=5, nutrientRows=[exampleRow, exampleRow])
            nutrientTables.append(exampleTable)
            exampleTable2 = NutrientTable(
                id=len(nutrientTables), name="standard2",nutrientFeedAmount=5, nutrientABGapTime=15, phDownFeedAmount=5, nutrientRows=[exampleRow, exampleRow])
            nutrientTables.append(exampleTable2)
            saveResult = FileManager.SaveObjAsJson(
                "nutrientTables.json", nutrientTables)
            print(f"NutrientTables created: {saveResult}")

        self.nutrientTables = nutrientTables

    def getActiveTableID(self):
        return self.activeTableID

    def ChangeActiveTable(self, activeTableID: int):
        if activeTableID >= 0 and activeTableID <= len(self.nutrientTables): 
            self.activeTableID = activeTableID
            self.Setup()
            return True
        return False

    def CreateTable(self, tableName: str, nutrientFeedAmount:int, nutrientABGapTime:int, phDownFeedAmount:int):
        newNutrientTable = NutrientTable(id=len(self.nutrientTables), name=tableName, nutrientFeedAmount=nutrientFeedAmount, nutrientABGapTime=nutrientABGapTime, phDownFeedAmount=phDownFeedAmount, nutrientRows=[])
        self.nutrientTables.append(newNutrientTable)
        saveResult = FileManager.SaveObjAsJson(
                "nutrientTables.json", self.nutrientTables)
        return saveResult

    def RemoveTable(self, tableID: int):
        if tableID >= 0 and tableID < len(self.nutrientTables):
            del self.nutrientTables[tableID]
            return True
        return False

    def GetTable(self, tableID: int = None) -> NutrientTable:
        if tableID is None:
            return ({"id": i.id, "name":i.name} for i in self.nutrientTables)
        if tableID >= 0 and tableID < len(self.nutrientTables):
            return self.nutrientTables[tableID]

    def AddTableRow(self, tableID: int, newRow: NutrientRow):
        if tableID >= 0 and tableID < len(self.nutrientTables):
            self.nutrientTables[tableID].nutrientRows.append(newRow)
            saveResult = FileManager.SaveObjAsJson(
                "nutrientTables.json", self.nutrientTables)
            return saveResult

        return False

    def EditTableRow(self, tableID: int, tableRow: int, newRow: NutrientRow):
        if tableID >= 0 and tableID < len(self.nutrientTables):
            if tableRow >= 0 and tableRow < len(self.nutrientTables[tableID].nutrientRows):
                self.nutrientTables[tableID].nutrientRows[tableRow] = newRow
                saveResult = FileManager.SaveObjAsJson(
                    "nutrientTables.json", self.nutrientTables)
                return saveResult

        return False

    def RemoveTableRow(self, tableID: int, tableRow: int):
        if tableID >= 0 and tableID < len(self.nutrientTables):
            if tableRow >= 0 and tableRow < len(self.nutrientTables[tableID].nutrientRows):
                del self.nutrientTables[tableID].nutrientRows[tableRow]
                saveResult = FileManager.SaveObjAsJson(
                    "nutrientTables.json", self.nutrientTables)
                return saveResult
        
        return False

    def Activate(self, activation : bool):
        self.activate = activation
        return True

    def GetActivation(self) -> bool:
        return self.activate 

    async def AdjustNutrient(self, nutrientARelay: Output.Relay, nutrientBRelay: Output.Relay, PHDownRelay: Output.Relay, phSensor: Sensor.PHSensor, tdsSensor: Sensor.TDSSensor):
        if self.activate:
            activeTable = self.nutrientTables[self.activeTableID]
            dayGap = date.today() - self.startDate
            #if current day still within day in table
            if dayGap.days <= len(activeTable.nutrientRows):
                ph = phSensor.GetPH()
                ec = tdsSensor.GetPPM()
                if ph is -1 or ec is None:
                    return
                
                #fix ph too high
                if ph > activeTable.nutrientRows[dayGap].maxPH:
                    PHDownRelay.OnRate(activeTable.phDownFeedAmount)
    
                #fix ec too low
                if ec < activeTable.nutrientRows[dayGap].minEC:
                    #add nutrientA
                    await nutrientARelay.OnRate(activeTable.nutrientFeedAmount)
                    #wait few hour
                    await asyncio.sleep(nutrientABGapTime)
                    #add nutrientB
                    await nutrientBRelay.OnRate(activeTable.nutrientFeedAmount)

    def AutoAdjustNutrient(self, scheduler: sched.scheduler, args: Tuple):
        return super().PeriodicTask(self.AdjustNutrient, self.adjustNutrientInterval, scheduler, args)
