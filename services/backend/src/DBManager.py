import sqlite3
import datetime

class SqlLite:
    def __init__(self, name, isMem=False):
        self.name = name
        self.isMem = isMem
        if isMem:
            self.con = sqlite3.connect(":memory:")
        else:
            self.con = sqlite3.connect('./src/DB/' +name+'.db')

    def Refresh(self):
        cur =  self.con.cursor()
        cur.close()
        self.con.close()

        self.con = sqlite3.connect(":memory:" if self.isMem else './src/DB/' +self.name+'.db')
    
    def Exe(self, exeStr):
        cur =  self.con.cursor()
        cur.execute(exeStr)

    def Commit(self):
        self.con.commit()

    def Fetch(self, exeStr):
        cur = self.con.cursor()
        self.Exe(exeStr)
        return cur.fetchall()

    def CreateDataTable(self, tableName, tableHeaders):
        cur =  self.con.cursor()
        cur.execute("create table if not exists "+ tableName +"(" +','.join(tableHeaders)+")")
        
        self.Refresh()

    def Append(self, tableName, recordList, autoCommit=True):
        cur =  self.con.cursor()
        cur.execute("insert into "+ tableName +" values (? " + ", ?"*(len(recordList)-1) + ")", recordList)

        if autoCommit:
            self.Commit()

    def GetRecords(self, tableName, firstID = -1, lastID = -1):
        cur = self.con.cursor()
        #cur.row_factory = lambda cursor, row: row[0] #Prefer list instread of tuple

        sql = "SELECT * FROM " + tableName

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
        rows = cur.fetchall()

        return rows
        
        
