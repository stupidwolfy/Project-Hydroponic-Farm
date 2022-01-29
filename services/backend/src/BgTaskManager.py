import schedule
import time
import sched

from datetime import datetime, time2zone

#For feed AB Fertilizer on schedule
class FertilizerHandler:
    def __init__(self, name, datetime, autoStart=True):
        self.name = name
        self.sch = sched.scheduler()
        self.sch.enterabs(datetime.timestamp(), 1, self.__FeedSequence())
        if autoStart:
            self.run()
            
    def run(self):
        self.schself.run()

    def __FeedSequence(self):
        print("feeding Fertilizer A")
        time.sleep(10)
        print("feeding Fertilizer B")
        


#For repeatly read sensor status and save it to DB
class SensorUpdater:
    def __init__(self, name):
        self.name = name
