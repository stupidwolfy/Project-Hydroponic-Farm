import json

def LoadObjFromJson(filename):
    try:
        with open(filename, 'r') as file_object:  
            data = json.load(file_object)  
        return data
    
    except FileNotFoundError:
         return None

def SaveObjAsJson(targetObj, filename):
    try:
        with open(filename, 'w') as file_object:
            json.dump(targetObj, file_object)
        return True 

    except:
         return False