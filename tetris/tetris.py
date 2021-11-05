from pynput.keyboard import Key, Listener, Controller
import pyautogui, os, time

# path info of files:
print(os.path.dirname(__file__))

print('Hello, I am Python bot and I will try to play old Tetris game on NES emulator :)')
print('Press q to start, set focus on the emulator window, and start the game :)')

scriptPath = os.path.dirname(__file__)

#keys:
keyRotate='z'
keyLeft='n'
keyRight='m'
keyPutDown='j'

keyboard = Controller()

widthOfWell = 80
heightOfWell = 161
wellLeft = 0
wellTop = 0

regionToTakeScreenshot = (0, 0, 81, 161)

def determineCoordinatesOfBricksWell():
	coordinatesOfBottomFrame = pyautogui.locateOnScreen(scriptPath + '/' + 'bottom-of-well.png', region=(0, 0, 250, 270))
	if coordinatesOfBottomFrame != None:
		print('Bottom of well detected')
		wellLeft = coordinatesOfBottomFrame[0] + 3;
		wellTop = coordinatesOfBottomFrame[1] - 4 - heightOfWell;
	return None

def playGame():
	print('initialized....')
	try:
		determineCoordinatesOfBricksWell()
		while 1==1 :
			return None
	except Exception as e:
		print(e)

def on_press(key):
    if str(key)=="'q'":
        playGame()
    if key == Key.esc:
        return False

with Listener(on_press=on_press) as listener:
    listener.join()
