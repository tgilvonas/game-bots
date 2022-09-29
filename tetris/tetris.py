from pynput.keyboard import Key, Listener, Controller
from PIL import Image
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
heightOfWell = 160

screenshotImg = 'screenshot.png'

def determineCoordinatesOfBricksWell():
	coordinatesOfBottomFrame = pyautogui.locateOnScreen(scriptPath + '/' + 'bottom-of-well.png', region=(0, 0, 250, 270))
	if coordinatesOfBottomFrame != None:
		print('Bottom of well detected')
		wellLeft = coordinatesOfBottomFrame[0] + 3
		wellTop = coordinatesOfBottomFrame[1] - 3 - heightOfWell
	return (wellLeft, wellTop, widthOfWell, heightOfWell)

def takeScreenshot(screenshotRegion):
	image = pyautogui.screenshot(screenshotImg, region=screenshotRegion)

def getPixel(x, y):
	imageObject = Image.open(scriptPath + '/' + screenshotImg).convert('RGB')
	r, g, b = imageObject.getpixel((x, y))
	if r != 0 or g != 0 or b != 0:
		return 1
	else:
		return 0

def scanScreenshot():
	posX = 4
	posY = 4
	stepX = 8
	stepY = 8
	wellMatrix = [[0]*10]*20
	while posY < heightOfWell:
		while posX < widthOfWell:
			result = getPixel(posX, posY)
			print(result)
			posX+=stepX
		posY+=stepY
		posX=4

def playGame():
	print('initialized....')
	try:
		coordinatesOfBricksWell = determineCoordinatesOfBricksWell()
		takeScreenshot(coordinatesOfBricksWell)
		scanScreenshot()
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
