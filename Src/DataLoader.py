import json
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))

def LoadFiles(directory:str) -> list:
   return  [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]

def LoadAndUpdateJson(defaultValues,file) -> list:
    if os.path.exists(file):
        dataRead = {}
        with open(file,'r') as data:
            print("Data Loaded")
            dataRead = json.load(data)
    
        for key, default_value in defaultValues.items():
            if (key not in dataRead) or (type(default_value) != type(dataRead[key])):
                dataRead[key] = default_value
        
        defaultValues = dataRead

    with open(file,'w') as data:
         json.dump(defaultValues,data)
    return defaultValues