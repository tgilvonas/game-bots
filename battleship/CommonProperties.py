from pynput.keyboard import Key, Listener, Controller
import pyautogui, os, time, random

class CommonProperties:
	scriptPath = os.path.dirname(__file__)

	dirOfSprites = scriptPath + '/sprites/'
	dirOfFieldsSprites = dirOfSprites + 'fields/'
	dirOfGameplaySprites = dirOfSprites + 'gameplay/'
	dirOfWeaponsSprites = dirOfSprites + 'weapons/'
	dirOfNumbersSprites = dirOfSprites + 'numbers/'

	scannableScreenRegion = (0, 40, 300, 280)

	keyLeft='n'
	keyRight='m'
	keyDown='j'
	keyUp='h'
	keySelect='b'
	keyShoot='x'
	keyRotate='z'
	keyStartGame='y'

	durationOfKeyDown = 0.02

	keyboard = Controller()

	def pressStart(self):
		self.keyboard.press(self.keyStartGame)
		time.sleep(self.durationOfKeyDown)
		self.keyboard.release(self.keyStartGame)

	def pressDown(self):
		self.keyboard.press(self.keyDown)
		time.sleep(self.durationOfKeyDown)
		self.keyboard.release(self.keyDown)

	def pressRight(self):
		self.keyboard.press(self.keyRight)
		time.sleep(self.durationOfKeyDown)
		self.keyboard.release(self.keyRight)
