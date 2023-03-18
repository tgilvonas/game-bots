from pynput.keyboard import Key, Listener, Controller
from Racer import Racer
import os

# path info of files:
print(os.path.dirname(__file__))

print('Hello, I am Python bot and I will try to play old RoadFighter game on NES emulator :)')
print('Press q to start, set focus on the emulator window, and start the game :)')

def on_press(key):
    if str(key)=="'q'":
        racer = Racer()
        racer.playGame()
    if key == Key.esc:
        return False

with Listener(on_press=on_press) as listener:
    listener.join()
