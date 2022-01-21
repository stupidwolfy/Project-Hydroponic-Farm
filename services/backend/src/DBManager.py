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

    def Create(self, tableName, tableHeaders):
        cur =  self.con.cursor()
        cur.execute("create table if not exists "+ tableName +"(" +','.join(tableHeaders)+")")
        
        self.Refresh()

    def Append(self, tableName, recordList, autoCommit=True):
        cur =  self.con.cursor()
        cur.execute("insert into "+ tableName +" values (? " + ", ?"*(len(recordList)-1) + ")", recordList)

        if autoCommit:
            self.Commit()
