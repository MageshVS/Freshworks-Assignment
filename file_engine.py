import json
import os
import os.path
import sys
import datetime

class FileEngine:
    def __init__(self, FilePath = "M:\Freshworks Assignment\main.json"):
        self.FilePath = FilePath

        try:
            if(not os.path.exists(FilePath)):
                with open(self.FilePath, "w") as outfile:
                    json.dump({"": {}}, outfile)
            if (os.path.getsize(self.FilePath) > 1024):
                raise MemoryError("Data file reached maximum capacity(1GB)")

        except OSError:
            print("Caught OSError!")
        except MemoryError as exp:
            print(exp)

    def CreateDataEntry(self, key, value, TimeToLive = sys.maxsize):
        try:
            if (len(key) > 32) :
                raise ValueError("Key is too large")
            if ((os.path.getsize(self.FilePath) / 1024) > 16):
                raise ValueError("Gson object should less than 16KB")
            with open(self.FilePath,'r+') as f:
                data = json.load(f)
                if key in dict(data):
                    raise KeyError("Key already exists")

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

        except KeyError as exp:
            print(exp)

    def getCurrentTime(self):
        curr_time = datetime.datetime.now().time()
        return str(curr_time.hour)+":"+str(curr_time.minute)+":"+str(curr_time.second)

    def read_all_data_engine(self):
        f = open(self.FilePath, "r")
        data = json.load(f)
        f.close()
        return data

    def checkTimeToLive(self, key):
        f = open(self.FilePath, "r")
        data = json.load(f)
        if key in data:
            a = dict(data[key])
        start = a["CurrentTime"]
        timeLimit = a["TimeToLive"]
        end = self.getCurrentTime()
        start_dt = datetime .datetime.strptime(start, '%H:%M:%S')
        end_dt = datetime .datetime.strptime(end, '%H:%M:%S')
        diff = (end_dt - start_dt)
        if(int(diff.seconds) < timeLimit):
            return True
        else:
            return True;

    def read_file(self, key):
        try:
            f = open(self.FilePath, "r")
            data = json.load(f)

            if not key in data:
                raise ValueError("Key is not present")

            if(not self.checkTimeToLive(key)):
                raise ValueError("Key has expired")

        except ValueError as exp:
            print(exp)

        finally:
            f.close()

        return data[key]

    def delete_data_engine(self, key):
        with open(self.FilePath, "r") as fi:
            data = json.load(fi)

        pop = data.pop(key, None)

        with open(self.FilePath, "w") as file:
            json.dump(data, file)

        return pop


'''p = FileEngine()
p.CreateDataEntry("very-large-key-to-make-the-exception", "1")
p.CreateDataEntry("test1", "test_object", 2000)
p.CreateDataEntry("test2", "test_object", 3000)'''
'''p.CreateDataEntry("two", "2", 30)
p.CreateDataEntry("three", "3")
p.CreateDataEntry("four", "4")'''
#p.readDataEngine("one")
#p.DeleteDataEngine("two")
#p.readDataEngine("two")
#print(p.read_all_data_engine())
#3p.CreateDataEntry("five", "5", 100)
