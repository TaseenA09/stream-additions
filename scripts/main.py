import keyboard
import mouse
import soundcontroller

SoundToPlay = None

keysDown = []

def removeKey(event):
    if event in keysDown:
        #print(keysDown)
        keysDown.remove(event)
        soundcontroller.playSoundForKey(event=event,type=1)
    

def on_key_press(event):
    #print(f"Key {event.name} was pressed")

    if not(event in keysDown):
        keysDown.append(event)
        soundcontroller.playSoundForKey(event=event,type=0)

    keyboard.on_release_key(event.name,lambda x: removeKey(event))

def on_mouse_click(event):
    if isinstance(event,mouse.ButtonEvent):
        soundcontroller.playMouseSound(event)
        

keyboard.on_press(on_key_press)

mouse.hook(on_mouse_click)

keyboard.wait()