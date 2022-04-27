from src import DBManager
from typing import List


class Nutrient:
    def __init__(self, name: str, dataTableName: str):
        self.name = name
        self.dataTableName = dataTableName
        self.db = DBManager.SqlLite("Nutrient")
        self.currentDay = 0
        self.isActive

    def Setup(self):
        pass

    def ChangeTable(self, newdataTableName:str):
        self.dataTableName = newdataTableName
        self.Setup()

    def addRecord(self, db: DBManager.DBManager, recordList: List):
        db.CreateDataTable(self.name, ["ph", "ec", "ph-tolerance", "ec-tolerance", "nutrient-cycle-volume"], ["day"])
        db.Append(self.name, recordList)

    def updatePH(self, db: DBManager.DBManager, targetDay:int, newValue):
        db.Replace(self.dataTableName, "day", targetDay, "ph", newValue)

    def updateEC(self, db: DBManager.DBManager, targetDay:int, newValue):
        db.Replace(self.dataTableName, "day", targetDay, "ec", newValue)

