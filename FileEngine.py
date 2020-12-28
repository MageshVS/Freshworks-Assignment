import json
import os
import os.path
import sys
import datetime

class FileEngine:
    def __init__(self, FilePath = "M:\\python\\main.json"):
        self.FilePath = FilePath
        dictionary = {"": {}}
        try:
            if(not os.path.exists(FilePath)):
                with open("main.json", "w") as outfile:
                    json.dump(dictionary, outfile)
        except OSError:
            print("Caught OSError!")



    def CreateDataEntry(self, key, value, TimeToLive = sys.maxsize):
        try:
            if (len(key) > 32) :
                raise ValueError("Key is too large")
            if ((os.path.getsize(self.FilePath) / 1024) > 16):
                raise ValueError("Gson object should less than 16KB")
            with open('main.json','r+') as f:
                data = json.load(f)
                if key in dict(data):
                    raise ValueError("Key already exists")

            temp_dict = {key: {
             "value": value,
             "TimeToLive": TimeToLive,
             "CurrentTime": self.getCurrentTime()}}

            with open("main.json", "r+") as file:
                data = json.load(file)
                data.update(temp_dict)
                file.seek(0)
                json.dump(data, file)

        except ValueError as exp:
            print(exp)

    def getCurrentTime(self):
        curr_time = datetime.datetime.now().time()
        return str(curr_time.hour)+":"+str(curr_time.minute)+":"+str(curr_time.second)

    def readAllDataEngine(self):
        f = open('main.json', "r")
        data = json.load(f)
        print(data)
        f.close()

    def checkTimeToLive(self, key, timeLimit = 1000):
        f = open('main.json', "r")
        data = json.load(f)
        if key in data:
            a = dict(data[key])
        start = a["CurrentTime"]
        curr_time = datetime.datetime.now().time()
        end = self.getCurrentTime()
        start_dt = datetime .datetime.strptime(start, '%H:%M:%S')
        end_dt = datetime .datetime.strptime(end, '%H:%M:%S')
        diff = (end_dt - start_dt)
        if(int(diff.seconds/60) < timeLimit):
            return True
        else:
            return True;

    def readDataEngine(self, key):
        try:
            if self.checkTimeToLive(key):
                f = open('main.json', "r")
                data = json.load(f)
            else:
                raise ValueError("Key has expired")

            if key in data:
                print(data[key])
            else:
                raise ValueError("Key is not present")
        except ValueError as exp:
            print(exp)

        f.close()

    def DeleteDataEngine(self, key):
        with open("main.json", "r") as fi:
            data = json.load(fi)

        data.pop(key, None)

        with open("main.json", "w") as file:
            json.dump(data, file)


p = FileEngine()
#p.CreateDataEntry("oneonronronroneonronronroneonronronr", "1")
#p.CreateDataEntry("two", "2", 30)
'''p.CreateDataEntry("two", "2", 30)
p.CreateDataEntry("three", "3")
p.CreateDataEntry("four", "4")'''
#p.readDataEngine("one")
#p.DeleteDataEngine("two")
p.readDataEngine("two")
#p.readAllDataEngine()
#3p.CreateDataEntry("five", "5", 100)
