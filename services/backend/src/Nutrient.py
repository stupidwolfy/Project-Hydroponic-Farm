from src import DBManager, FileManager
from src.devices import Output, Sensor
from typing import List, Tuple, Callable
from pydantic import BaseModel
from datetime import date
import sched


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
    nutrientRows: List[NutrientRow]


class NutrientManager(Repeatable):
    def __init__(self, activeTableID: int, startDate: date = None, adjustNutrientInterval=5):
        if startDate is None:
            self.startDate = date.today()
        else:
            self.startDate = startDate

        self.activeTableID = activeTableID
        self.adjustNutrientInterval = adjustNutrientInterval

        self.Setup()

    def Setup(self):
        nutrientTables = FileManager.LoadObjFromJson("nutrientTables.json")

        # create nutrientTable if no json file
        if nutrientTables is None:
            nutrientTables = []
            exampleRow = NutrientRow(minEC=2, maxPH=8)
            exampleTable = NutrientTable(
                id=len(nutrientTables), name="standard", nutrientRows=[exampleRow, exampleRow])
            nutrientTables.append(exampleTable)
            exampleTable2 = NutrientTable(
                id=len(nutrientTables), name="standard2", nutrientRows=[exampleRow, exampleRow])
            nutrientTables.append(exampleTable2)
            saveResult = FileManager.SaveObjAsJson(
                "nutrientTables.json", nutrientTables)
            print(f"NutrientTables created: {saveResult}")

        self.nutrientTables = nutrientTables

    def ChangeActiveTable(self, activeTableID: int):
        self.activeTableID = activeTableID
        self.Setup()

    def AddTableRow(self, tableID: int, newRow: NutrientRow):
        if tableID >= 0 and tableID <= len(self.nutrientTables):
            self.nutrientTables[tableID].append(newRow)
            saveResult = FileManager.SaveObjAsJson(
                "nutrientTables.json", self.nutrientTables)
            return saveResult

        return False

    def EditTableRow(self, tableID: int, tableRow: int, newRow: NutrientRow):
        if tableID >= 0 and tableID <= len(self.nutrientTables):
            if tableRow >= 0 and tableRow <= len(self.nutrientTables[tableID]):
                self.nutrientTables[tableID][tableRow] = newRow
                saveResult = FileManager.SaveObjAsJson(
                    "nutrientTables.json", self.nutrientTables)
                return saveResult

        return False

    def RemoveTableRow(self, tableID: int, tableRow: int):
        if tableID >= 0 and tableID <= len(self.nutrientTables):
            if tableRow >= 0 and tableRow <= len(self.nutrientTables[tableID]):
                del self.nutrientTables[tableID][tableRow]
                saveResult = FileManager.SaveObjAsJson(
                    "nutrientTables.json", self.nutrientTables)
                return saveResult
        
        return False

    def AdjustNutrient(self, nutrientARelay: Output.Relay, nutrientBRelay: Output.Relay, PHDownRelay: Output.Relay, phSensor: Sensor.PHSensor, tdsSensor: Sensor.TDSSensor):
        activeTable = self.nutrientTables[0]
        currentDate = date.today() - self.startDate
        ph = phSensor.GetPH()
        ec = tdsSensor.GetPPM()

        if ph is -1 or ec is None:
            return

        #if ph > activeTable 

    def AutoAdjustNutrient(self, scheduler: sched.scheduler, args: Tuple):
        return super().PeriodicTask(self.AdjustNutrient, self.adjustNutrientInterval, scheduler, args)
