import json
import jsonpickle

def LoadObjFromJson(filename:str, useJsonPickle= True):
    try:
        with open("./Config/" + filename, 'r') as file_object:
            if useJsonPickle:
                jsonStr = file_object.read()
                obj = jsonpickle.decode(jsonStr)
            else:
                obj = json.load(file_object) 
        return obj
    
    except FileNotFoundError:
        return None

def SaveObjAsJson(filename:str, targetObj, useJsonPickle= True):
    try:
        with open("./Config/" + filename, 'w') as file_object:
            if useJsonPickle:
                jsonObj = jsonpickle.encode(targetObj, indent=4)
                file_object.write(jsonObj)
            else:
                json.dump(targetObj, file_object, indent=4)
        return True 
    except Exception as e:
        return str(e)