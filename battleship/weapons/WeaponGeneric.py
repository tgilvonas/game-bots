from pynput.keyboard import Key, Listener, Controller
import pyautogui, os, time, random

class WeaponGeneric:
	
	weaponsSpritesPath = ''

	scannableScreenRegion = (0, 40, 300, 280)

	keyLeft='n'
	keyRight='m'
	keyDown='j'
	keyUp='h'
	keySelect='b'
	keyShoot='x'

	pressReleaseDelay = 5

	keyboard = Controller()

	def __init__(self):
		appPath = os.path.dirname(__file__)
		appPathArray = appPath.split(os.sep)
		appPathArray.pop()
		appPath = os.sep.join(appPathArray)
		self.weaponsSpritesPath = appPath + os.sep + 'sprites' + os.sep + 'weapons' + os.sep

	def pressSelect(self):
		self.keyboard.press(self.keySelect)
		time.sleep(0.1)
		self.keyboard.release(self.keySelect)

	def moveCrosshairsRight(self):
		self.keyboard.press(self.keyRight)
		time.sleep(self.pressReleaseDelay)
		self.keyboard.release(self.keyRight)

	def moveCrosshairsDown(self):
		self.keyboard.press(self.keyDown)
		time.sleep(self.pressReleaseDelay)
		self.keyboard.release(self.keyDown)

	def pressFire(self):
		self.keyboard.press(self.keyShoot)
		time.sleep(1)
		self.keyboard.release(self.keyShoot)
