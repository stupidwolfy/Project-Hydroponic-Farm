import json
import jsonpickle

def LoadObjFromJson(filename, useJsonPickle= True):
    try:
        with open("./src/Config/" + filename, 'r') as file_object:
            if useJsonPickle:
                jsonStr = file_object.read()
                obj = jsonpickle.decode(jsonStr)
            else:
                obj = json.load(file_object) 
        return obj
    
    except FileNotFoundError:
        return None

def SaveObjAsJson(filename, targetObj, useJsonPickle= True):
    try:
        with open("./src/Config/" + filename, 'w') as file_object:
            if useJsonPickle:
                jsonObj = jsonpickle.encode(targetObj, indent=4)
                file_object.write(jsonObj)
            else:
                json.dump(targetObj, file_object, indent=4)
        return True 

    except:
        return False