import keyboard
import SoundController

SoundToPlay = None

keysDown = []

def removeKey(event):
    if event in keysDown:
        print(keysDown)
        keysDown.remove(event)
        SoundController.playSoundForKey(event=event,type=1)
    

def on_key_press(event):
    #print(f"Key {event.name} was pressed")

    if not(event in keysDown):
        keysDown.append(event)
        SoundController.playSoundForKey(event=event,type=0)

    keyboard.on_release_key(event.name,lambda x: removeKey(event))

keyboard.on_press(on_key_press)

keyboard.wait()