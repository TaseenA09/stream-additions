import pygame
import numpy as np
import random
import dataloader
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))

pygame.mixer.init()

Settings, LoadedSounds = dataloader.GetSoundsFromCurrentProfile()

spaceKeys = ["space"]
specialKeys = ['enter']

def getSoundFromType(soundList:list,type):
    if soundList[type]:
        return soundList[type]
    else:
        return None

def change_pitch(sound, pitch_factor):
    # Get samples from the sound object
    samples = pygame.sndarray.array(sound)


    if samples.ndim == 2:
        #if np.array_equal(samples[:, 0], samples[:, 1]):
        #    print("MONO")
        samples = samples[:, 0] 


    # Resample to change pitch
    num_samples = int(len(samples) * pitch_factor)
    resampled = np.interp(
        np.linspace(0, len(samples), num_samples),
        np.arange(len(samples)),
        samples
    )

    # Convert back to 2D array (stereo)
    resampled = np.column_stack((resampled, resampled))  # Duplicate for stereo

    # Create a new sound object from the resampled array
    new_sound = pygame.sndarray.make_sound(resampled.astype(np.int16))  # Ensure type is correct

    return new_sound

def randomisePitchAndVolume(sound:pygame.mixer.Sound,eventName:str,seed:int):
    random.seed(seed)
    pitched_sound = change_pitch(sound, Settings["PitchUp"]+(random.random()*(Settings["PitchDown"]-Settings["PitchUp"]))+(len(eventName)*(Settings["PitchModifier"]/np.sqrt(len(eventName)))))
    pitched_sound.set_volume(0.4+(random.SystemRandom().random()*0.1))
    pitched_sound.fadeout(1)
    pitched_sound.play()

def tryToGetSounds(sound:str):
    if LoadedSounds[sound]:
        return LoadedSounds[sound]
    elif LoadedSounds["Default"]:
        return LoadedSounds["Default"]
    elif LoadedSounds["Key"]:
        return LoadedSounds["Key"]

def playSoundForKey(event,type:int):
    seed = sum(ord(char) for char in event.name)
    random.seed(seed)


    currentSoundList = None

    if event.name in specialKeys:
        currentSoundList = getSoundFromType(tryToGetSounds("Enter"),type)
    elif event.name in spaceKeys:

        currentSoundList = getSoundFromType(tryToGetSounds("Space"),type)
    else:

        currentSoundList = getSoundFromType(tryToGetSounds("Key"),type)

    key_sound_selected = currentSoundList[random.SystemRandom().randint(0,len(currentSoundList)-1)]

    currentSound = pygame.mixer.Sound(key_sound_selected)

    # print("Playing: ",key_sound_selected)

    randomisePitchAndVolume(sound=currentSound,eventName=event.name,seed=seed)

def playMouseSound(buttonEvent):
    seed = sum(ord(char) for char in buttonEvent.button)
    random.seed(seed)


    currentSoundList = None

    if buttonEvent.button == "middle":
        if buttonEvent.event_type == "down" or buttonEvent.event_type == "double":
            currentSoundList = getSoundFromType(tryToGetSounds("Middle"),0)
        elif  buttonEvent.event_type == "up":
            currentSoundList = getSoundFromType(tryToGetSounds("Middle"),1)
    else:
        if buttonEvent.event_type == "down" or buttonEvent.event_type == "double":
            currentSoundList = getSoundFromType(tryToGetSounds("Click"),0)
        elif  buttonEvent.event_type == "up":
            currentSoundList = getSoundFromType(tryToGetSounds("Click"),1)


    mouse_Sound_Selected = currentSoundList[random.SystemRandom().randint(0,len(currentSoundList)-1)]
    currentSound = pygame.mixer.Sound(mouse_Sound_Selected)
    randomisePitchAndVolume(sound=currentSound,eventName=buttonEvent.button,seed=seed)