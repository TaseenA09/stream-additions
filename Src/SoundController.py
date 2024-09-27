import pygame
import numpy as np
import random
import os
import DataLoader

pygame.mixer.init()

ConfigData = DataLoader.LoadAndUpdateJson(defaultValues={
        "EnterSoundsDir": '../Sounds/Enter',
        "SpaceSoundsDirs": ['../Sounds/Space/Down','../Sounds/Space/Up'],
        "KeySoundsDir": ['../Sounds/Key/Down','../Sounds/Key/Up'],
        "PitchDown" : 1.1,
        "PitchUp" : 0.95,
        "PitchModifier" : 0.025,
}
,file= "SoundData.json"
)


EnterSounds = [f for f in os.listdir(ConfigData["EnterSoundsDir"]) if os.path.isfile(os.path.join(ConfigData["EnterSoundsDir"], f))]

SpaceSounds = [
    [f for f in os.listdir(ConfigData["SpaceSoundsDirs"][0]) if os.path.isfile(os.path.join(ConfigData["SpaceSoundsDirs"][0], f))],
    [f for f in os.listdir(ConfigData["SpaceSoundsDirs"][1]) if os.path.isfile(os.path.join(ConfigData["SpaceSoundsDirs"][1], f))]
]

KeySounds = [
    [f for f in os.listdir(ConfigData["KeySoundsDir"][0]) if os.path.isfile(os.path.join(ConfigData["KeySoundsDir"][0], f))],
    [f for f in os.listdir(ConfigData["KeySoundsDir"][1]) if os.path.isfile(os.path.join(ConfigData["KeySoundsDir"][1], f))]
]


spaceKeys = ["space"]
specialKeys = ['enter']


def change_pitch(sound, pitch_factor):
    # Get samples from the sound object
    samples = pygame.sndarray.array(sound)


    if samples.ndim == 2:
        if np.array_equal(samples[:, 0], samples[:, 1]):
            print("MONO")
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

def playSoundForKey(event,type:int):
    seed = sum(ord(char) for char in event.name)
    random.seed(seed)

    currentSoundDir = None
    currentSoundList = None

    if event.name in specialKeys:
        if type == 0:
            currentSoundDir = ConfigData["EnterSoundsDir"]
            currentSoundList = EnterSounds
        else:
            return
    elif event.name in spaceKeys:
        currentSoundDir = ConfigData["SpaceSoundsDirs"][type]
        currentSoundList = SpaceSounds[type]
    else:
        currentSoundDir = ConfigData["KeySoundsDir"][type]
        currentSoundList = KeySounds[type]

    key_sound_selected = currentSoundDir+"/"+currentSoundList[random.SystemRandom().randint(0,len(currentSoundList)-1)]

    currentSound = pygame.mixer.Sound(key_sound_selected)

    print("Playing: ",key_sound_selected)

    pitched_sound = change_pitch(currentSound, ConfigData["PitchUp"]+(random.random()*(ConfigData["PitchDown"]-ConfigData["PitchUp"]))+(len(event.name)*(ConfigData["PitchModifier"]/np.sqrt(len(event.name)))))
    pitched_sound.set_volume(0.4+(random.SystemRandom().random()*0.1))
    pitched_sound.fadeout(1)
    pitched_sound.play()