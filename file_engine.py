import json
import os
import os.path
import sys
import datetime
import filelock
import pathlib


class FileEngine:
    #if the user does not provide any file path then the application will use the current working directory
    def __init__(self, FilePath = str(pathlib.Path(__file__).parent.absolute())+"\data_store.json"):
        self.FilePath = FilePath
        # A FileLock is used to indicate another process of your application that a resource or
        # working directory is currently used. To do so, create a FileLock first.
        self.lockFile = str(FilePath) + ".lock"

        try:
            #checking if the file exists. if not, creating a new json file
            if(not os.path.exists(FilePath)):
                #locking the file for thread safety
                #writing dummy data to avoid I/O Exception
                with filelock.FileLock(self.lockFile):
                    with open(FilePath, 'w') as f:
                        json.dump({"": {}}, f)
            #checking the data store file size if it exceeds the total capacity(1GB)
            if (os.path.getsize(FilePath) > 1024):
                raise MemoryError("Data file reached maximum capacity(1GB)")

        #raise exception if something goes wrong in I/O operations
        except OSError:
            print("Caught OSError!")
        #raise Exception if the data store file size exceeds 1GB
        except MemoryError as exp:
            print(exp)

    def CreateDataEntry(self, key, value, TimeToLive = sys.maxsize):
        try:
            #cheching if the key is valid
            # 1.key shoud be a string type
            # 2.length of the key should be always less than 32 chars
            if ((isinstance(key, str)) and len(key) > 32) :
                raise KeyError("Key is too large")
            #cheching if the value is valid
            # 1.value shoud be a json object
            # 2.length of the value should be always less than 16KB
            if ((sys.getsizeof(value) / 1024) > 16):
                raise ValueError("Gson object should less than 16KB")

            #locking the file before accessing it for thread safety
            with filelock.FileLock(self.lockFile):
                with open(self.FilePath, 'r+') as file:
                    data = json.load(file)
                    #checking if the given key is present in the file. if not, raising an exception
                    if key in dict(data):
                        raise KeyError("Key already exists")
                    else:
                        #creating a new dictonary with given values
                        temp_dict = {key: {
                         "value": value,
                         "TimeToLive": TimeToLive,
                         "TimeStamp": self.getCurrentTime()}}
                         #updating the old dictonary with the new values and writing into the file
                        data.update(temp_dict)
                        file.seek(0)
                        json.dump(data, file)

        except ValueError as exp:
            print(exp)

    def getCurrentTime(self):
        #helper method to find the current time in string format
        curr_time = datetime.datetime.now().time()
        return str(curr_time.hour)+":"+str(curr_time.minute)+":"+str(curr_time.second)

    def checkTimeToLive(self, key):
        #geting the TimeStamp of the json object
        f = open(self.FilePath, "r")
        data = json.load(f)
        if key in data:
            a = dict(data[key])
        f.close()
        timeLimit = a["TimeToLive"]
        #calulating the time difference between the current time and the TimeStamp
        start_dt = datetime .datetime.strptime(a["TimeStamp"], '%H:%M:%S')
        end_dt = datetime .datetime.strptime(self.getCurrentTime(), '%H:%M:%S')
        diff = (end_dt - start_dt)
        #if the difference is less than timeLimit then return true(the key is still valid)
        if(int(diff.seconds) < timeLimit):
            return True
        else:
            return False;

    def read_file(self, key):
        try:
            #before reading a object, locking the file for thread safety
            with filelock.FileLock(self.lockFile):
                with open(self.FilePath, 'r') as readfile:
                    data = json.load(readfile)
                    #if the given key is not present in data store, raise ValueError
                    if not key in data:
                        raise KeyError("Key is not present")
                    #if the given invalid, raise ValueError
                    if(not self.checkTimeToLive(key)):
                        raise KeyError("Key has expired")

                    #returning the object corresponding to the given key
                    return data[key]

        except OSError as exp:
            print(exp)


    def delete_data_engine(self, key):
        #before deleting a object locking the file for thread safety
        with filelock.FileLock(self.lockFile):
            with open(self.FilePath, 'r') as f:
                data = json.load(f)
                #if the given key is not present in data store, raise ValueError
                if not key in dict(data):
                    raise KeyError("Key does not exists")
                #if the given invalid, raise ValueError
                if(not self.checkTimeToLive(key)):
                    raise KeyError("Key has expired")
                #deleting the object corresponding to the given key
                pop = data.pop(key, None)

        #updating the data store after deletion
        with filelock.FileLock(self.lockFile):
            with open(self.FilePath, 'w') as file:
                json.dump(data, file)

#sample test cases to test the program manually
#p = FileEngine()
#p.CreateDataEntry("key_expired", "test_object",10)
#p.CreateDataEntry("test1", "test_object", 2000)
#p.CreateDataEntry("test2", "test_object", 3000)
#print(p.read_file("test1"))
#print(p.delete_data_engine("test1"))
#print(p.read_all_data_engine())
