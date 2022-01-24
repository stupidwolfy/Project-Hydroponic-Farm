import sqlite3
from datetime import datetime, timezone

from numpy import empty

class SqlLite:
    def __init__(self, name, isMem=False):
        self.name = name
        self.isMem = isMem
        if isMem:
            self.con = sqlite3.connect(":memory:")
        else:
            self.con = sqlite3.connect('./src/DB/' +name+'.db')

    def Close(self):
        cur =  self.con.cursor()
        cur.close()
        self.con.close()

    def Refresh(self):
        self.Close()

        self.con = sqlite3.connect(":memory:" if self.isMem else './src/DB/' +self.name+'.db')
    
    def Exe(self, exeStr):
        cur =  self.con.cursor()
        cur.execute(exeStr)

        #cur.close()

    def Commit(self):
        self.con.commit()
        self.con.cursor().close()

    def Fetch(self, exeStr):
        cur = self.con.cursor()
        self.Exe(exeStr)

        rows = cur.fetchall()
        cur.close()

        return rows

    def CreateDataTable(self, tableName, tableHeaders):
        cur =  self.con.cursor()
        cur.execute("create table if not exists "+ tableName +"(" + "Time_Stamp, " +','.join(tableHeaders)+")")
        
        self.Refresh()

    def Append(self, tableName, recordList, autoCommit=True):
        recordList.insert(0, datetime.now()) #inject current datetime to list (utc time)
        cur =  self.con.cursor()
        cur.execute("insert into "+ tableName +" values (? " + ", ?"*(len(recordList)-1) + ")", recordList)

        if autoCommit:
            self.Commit()

    def GetRecords(self, tableName=None, firstID = -1, lastID = -1):
        cur = self.con.cursor()
        if tableName is None:
            cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = [member[0] for member in cur.fetchall()]
            dataTable = {"tables" : tables}
        else:
          #cur.row_factory = lambda cursor, row: row[0] #Prefer list instread of tuple
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
          cur.close()
  
          dataTable = {"column": colNames, "data": rows}

        return dataTable

        
