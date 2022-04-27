import sqlite3
from contextlib import closing
from datetime import datetime, timezone
from abc import ABC, abstractmethod
from typing import List, Optional

from numpy import empty


class DBManager(ABC):
    @abstractmethod
    def __init__(self, name: str):
        pass

    @abstractmethod
    def CreateDataTable(self, tableName: str, tableHeaders: List[str], uniqueHeaders: Optional[List[str]] = None):
        pass

    @abstractmethod
    def Append(self, tableName: str, recordList: List, addTimeStamp = True):
        pass

    @abstractmethod
    def GetRecords(self, tableName: str = None, firstID=-1, lastID=-1):
        pass


class SqlLite(DBManager):
    def __init__(self, name):
        self.name = name
        #self.con = sqlite3.connect('./DB/' +name+'.db')

    def CreateDataTable(self, tableName: str, tableHeaders: List[str], uniqueHeaders: Optional[List[str]] = None):
        tableName = tableName.replace(" ", "_")
        tableName = tableName.replace("-", "_")
        #cur =  self.con.cursor()
        #cur.execute("create table if not exists "+ tableName +"(" + "Time_Stamp, " +','.join(tableHeaders)+")")

        # self.Refresh()

        db_name = './DB/' + self.name+'.db'
        with closing(sqlite3.connect(db_name)) as con, con, closing(con.cursor()) as cur:
            #if no unique column
            if uniqueHeaders is None:
                 cur.execute("create table if not exists " + tableName +
                             "(" + "Time_Stamp, " + ','.join(tableHeaders)+")")
            else:
                cur.execute("create table if not exists " + tableName +
                             "(" + "Time_Stamp, " + ','.join(tableHeaders)+ ", UNIQUE("+ ','.join(uniqueHeaders) +") )")
            # return cur.fetchall()

    def Append(self, tableName, recordList, addTimeStamp = True):
        tableName = tableName.replace(" ", "_")
        tableName = tableName.replace("-", "_")
        # inject current datetime to list (utc time)
        if addTimeStamp:
            recordList.insert(0, datetime.now())

        db_name = './DB/' + self.name+'.db'
        with closing(sqlite3.connect(db_name)) as con, con, closing(con.cursor()) as cur:
            cur.execute("insert into " + tableName + " values (? " +
                        ", ?"*(len(recordList)-1) + ")", recordList)
            # return cur.fetchall()


    def Replace(self, tableName, columIdname, columValue, targetColumnName, newValue):
        tableName = tableName.replace(" ", "_")
        tableName = tableName.replace("-", "_")

        db_name = './DB/' + self.name+'.db'

        with closing(sqlite3.connect(db_name)) as con, con, closing(con.cursor()) as cur:
            cur.execute("UPDATE " + tableName + " SET ? = ? WHERE ? = ?", [targetColumnName, newValue, columIdname, columValue])

    def GetRecords(self, tableName=None, limit=-1):
        db_name = './DB/' + self.name+'.db'
        with closing(sqlite3.connect(db_name)) as con, con, closing(con.cursor()) as cur:
            # Get all tables name
            if tableName is None:
                cur.execute(
                    "SELECT name FROM sqlite_master WHERE type='table';")
                tables = [member[0] for member in cur.fetchall()]
                dataTable = {"tables": tables}
            # Get table data
            else:
                # cur.row_factory = lambda cursor, row: row[0] #if prefer list instread of tuple
                sql = "SELECT * FROM " + tableName
                sql += " ORDER BY Time_Stamp DESC"

                if limit > -1:
                    sql += " LIMIT " + str(limit)
                cur.execute(sql)

                # Trim 'None' from get table name
                # from (('Tablename1', None, None,....),('Tablename2', None, None,....))
                #to   ('Tablename1', 'Tablename2')
                colNames = [member[0] for member in cur.description]
                rows = cur.fetchall()

                dataTable = {"column": colNames, "data": rows}
            return dataTable
