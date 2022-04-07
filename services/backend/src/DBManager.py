import sqlite3
from contextlib import closing
from datetime import datetime, timezone
from abc import ABC, abstractmethod
from typing import List

from numpy import empty

class DBManager(ABC):
    @abstractmethod
    def __init__(self, name:str):
        pass

    @abstractmethod
    def CreateDataTable(self, tableName:str, tableHeaders:List[str]):
        pass

    @abstractmethod
    def Append(self, tableName:str, recordList:List):
        pass

    @abstractmethod
    def GetRecords(self, tableName:str=None, firstID = -1, lastID = -1):
        pass

class SqlLite(DBManager):
    def __init__(self, name):
        self.name = name
        #self.con = sqlite3.connect('./DB/' +name+'.db')

    def CreateDataTable(self, tableName, tableHeaders):
        tableName = tableName.replace(" ", "_")
        tableName = tableName.replace("-", "_")
        #cur =  self.con.cursor()
        #cur.execute("create table if not exists "+ tableName +"(" + "Time_Stamp, " +','.join(tableHeaders)+")")
        
        #self.Refresh()

        db_name = './DB/' +self.name+'.db'
        with closing(sqlite3.connect(db_name)) as con, con, closing(con.cursor()) as cur:
          cur.execute("create table if not exists "+ tableName +"(" + "Time_Stamp, " +','.join(tableHeaders)+")")
          #return cur.fetchall()

    def Append(self, tableName, recordList):
        tableName = tableName.replace(" ", "_")
        recordList.insert(0, datetime.now()) #inject current datetime to list (utc time)
        #cur =  self.con.cursor()
        #cur.execute("insert into "+ tableName +" values (? " + ", ?"*(len(recordList)-1) + ")", recordList)

        #if autoCommit:
        #    self.Commit()

        db_name = './DB/' +self.name+'.db'
        with closing(sqlite3.connect(db_name)) as con, con, closing(con.cursor()) as cur:
          cur.execute("insert into "+ tableName +" values (? " + ", ?"*(len(recordList)-1) + ")", recordList)
          #return cur.fetchall()

    def GetRecords(self, tableName=None, firstID = -1, lastID = -1):
        #cur = self.con.cursor()
        db_name = './DB/' +self.name+'.db'
        with closing(sqlite3.connect(db_name)) as con, con, closing(con.cursor()) as cur:
          #Get all tables name
          if tableName is None:
              cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
              tables = [member[0] for member in cur.fetchall()]
              dataTable = {"tables" : tables}
          #Get table data
          else:
            #cur.row_factory = lambda cursor, row: row[0] #if prefer list instread of tuple
            sql = "SELECT * FROM " + tableName
  
            #Filter form x row to x row
            if firstID > -1 or lastID > -1:
                sql += " WHERE"
    
                if firstID > -1 and lastID == -1:
                    sql+= " rowid >=? "
                    cur.execute(sql, [firstID])
    
                elif firstID == -1 and lastID > -1:
                    sql+= " rowid <=? "
                    cur.execute(sql, [lastID])
                    
                elif firstID > -1 and lastID > -1:
                    sql+= " rowid BETWEEN ? AND ?"
                    cur.execute(sql, [firstID, lastID])
    
            else:
                cur.execute(sql)
  
            #Trim 'None' from get table name
            #from (('Tablename1', None, None,....),('Tablename2', None, None,....))
            #to   ('Tablename1', 'Tablename2')
            colNames = [member[0] for member in cur.description]
            rows = cur.fetchall()
    
            dataTable = {"column": colNames, "data": rows}
          return dataTable

        
