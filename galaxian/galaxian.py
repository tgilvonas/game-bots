from pynput.keyboard import Key, Listener, Controller
import pyautogui, os, time

# path info of files:
print(os.path.dirname(__file__))

print('Hello, I am Python bot and I will try to play old Galaxian game on NES emulator :)')
print('Press q to start, set focus on the emulator window, and start the game :)')

scriptPath = os.path.dirname(__file__)

spritesDir = scriptPath + '/sprites/'

def playGame():
	print('initialized....')
	keyboard = Controller()
	while 1==1 :
		try:
			# next line should be deleted, and the code of game bot should be written:
			print('It works')
		except Exception as e:
			print(e)

def on_press(key):
    if str(key)=="'q'":
        playGame()
    if key == Key.esc:
        return False

with Listener(on_press=on_press) as listener:
    listener.join()
