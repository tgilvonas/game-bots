from pynput.keyboard import Key, Listener, Controller
import pyautogui, os, time, random

print('Hello, I am Python bot and I will try to play Battleship game on NES emulator :)')
print('Press q to start, set focus on the emulator window, and start the game :)')

scriptPath = os.path.dirname(__file__)

spritesDir = scriptPath + '/sprites/'

keyLeft='n'
keyRight='m'

keyboard = Controller()

def playGame():
	print('initialized....')
	while 1==1 :
		try:
			keyboard.press(keyShoot)
			keyboard.release(keyShoot)
		except Exception as e:
			print(e)

def on_press(key):
    if str(key)=="'q'":
        playGame()
    if key == Key.esc:
        return False

with Listener(on_press=on_press) as listener:
    listener.join()
