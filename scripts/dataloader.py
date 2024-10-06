import json
import os
import mimetypes

os.chdir(os.path.dirname(os.path.abspath(__file__)))

SoundFile = "../Sound Profiles"

CONFIG_FILE = "SoundData.json" 
DEFAULT_CONFIG_DATA = {
    "PitchDown": 1.1,
    "PitchUp": 0.95,
    "PitchModifier":0.025
}

# Loads all files from a given directory
def LoadFiles(directory:str) -> list:
   return  [os.path.join(directory, f) for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]

def CheckFileTypes(files:list,type:str) -> list:
    return [f for f in files if (mime_type := mimetypes.guess_type(f)[0]) is not None and mime_type.startswith(type)]

def LoadDirectories(directory:str):
    return [os.path.join(directory, f) for f in os.listdir(directory) if os.path.isdir(os.path.join(directory, f))]

def GetFileName(directory:str):
    return os.path.basename(os.path.normpath(directory))

# Function to check a keyboard Sound Profile
def GetSoundProfileFolder(ProfileName:str) -> str:
    PossibleSoundFiles = LoadDirectories(SoundFile)
    possibleSoundFile = None

    #Used for logic to prefer metadata
    soundFileSource = 0

    for soundFile in PossibleSoundFiles:
        metaData = None

        for soundMetaData in LoadFiles(soundFile):
            try:
                if os.path.basename(soundMetaData) == "SoundProfile.json":
                    with open(soundMetaData, "r") as soundMetaDataRead:
                        metaData = json.load(soundMetaDataRead)
                    
                    break
            except:
                continue

        if metaData and ("ProfileName" in metaData) and (metaData["ProfileName"] == ProfileName):
            soundFileSource = 1
            possibleSoundFile = soundFile
        elif soundFileSource == 0 and os.path.basename(os.path.normpath(soundFile)) == ProfileName:
            possibleSoundFile = soundFile

    return possibleSoundFile

def getSoundsInDirectory(directory:str) -> list:
    filesLoaded = [None,None]
    upDownFiles = LoadDirectories(directory)

    for idir in upDownFiles:
        if GetFileName(idir) == "Up":
            filesLoaded[0] = CheckFileTypes(LoadFiles(idir),"audio")
        elif GetFileName(idir) == "Down":
            filesLoaded[1] = CheckFileTypes(LoadFiles(idir),"audio")

    if len(filesLoaded) == 1:
        if not filesLoaded[1]: 
            filesLoaded[1] = filesLoaded[0]
    elif len(filesLoaded) == 0:
        filesLoaded[0] = CheckFileTypes(LoadFiles(directory),"audio")

    return filesLoaded

def GetSoundFiles(ProfileName:str):
    soundFiles = {}
    soundProfileFolder = GetSoundProfileFolder(ProfileName)
    
    if not soundProfileFolder:
        return

    directoriesInSoundProfile = LoadDirectories(soundProfileFolder)

    soundFiles["Default"] = getSoundsInDirectory(soundProfileFolder)

    for sdir in directoriesInSoundProfile:
        if os.path.basename(os.path.normcase(sdir)) == "key":
           soundFiles["Key"] = getSoundsInDirectory(sdir)
           if soundFiles["Default"] == [None,None]:
               soundFiles["Default"] = soundFiles["Key"]
        elif os.path.basename(os.path.normcase(sdir)) == "special":
            soundFiles["Special"] = getSoundsInDirectory(sdir)
        elif os.path.basename(os.path.normcase(sdir)) == "enter":
            soundFiles["Enter"] = getSoundsInDirectory(sdir)
        elif os.path.basename(os.path.normcase(sdir)) == "space":
            soundFiles["Space"] = getSoundsInDirectory(sdir)
        elif os.path.basename(os.path.normcase(sdir)) == "modifier":
            soundFiles["Modifier"] = getSoundsInDirectory(sdir)
        elif os.path.basename(os.path.normcase(sdir)) == "click":
            soundFiles["Click"] = getSoundsInDirectory(sdir)
        elif os.path.basename(os.path.normcase(sdir)) == "middle":
            soundFiles["Middle"] = getSoundsInDirectory(sdir)
            if soundFiles["Default"] == [None,None]: 
                soundFiles["Middle"] = soundFiles["Click"]

    return soundFiles


# Loads or creates a json file depending on if it exists or not.
def LoadAndUpdateJson(defaultValues,file) -> list:
    dataRead = {}
    if os.path.exists(file):    
        with open(file,'r') as data:
            try:
                dataRead = json.load(data)    
            except:
                return defaultValues
    
        for key, default_value in defaultValues.items():
            if (key not in dataRead) or (type(default_value) != type(dataRead[key])):
                dataRead[key] = default_value
        
        defaultValues = dataRead

    else:
        with open(file,'w') as data:
             if (dataRead != data):
                 json.dump(defaultValues,data,indent=4)

    return defaultValues

def GetSoundsFromCurrentProfile() -> tuple[list,list]:
    loadedData = LoadAndUpdateJson(DEFAULT_CONFIG_DATA,CONFIG_FILE)
    
    if not "CurrentProfile" in loadedData or (isinstance(loadedData["CurrentProfile"],str)):
        loadedData["CurrentProfile"] = "default"
    
    return loadedData,GetSoundFiles(loadedData["CurrentProfile"])
