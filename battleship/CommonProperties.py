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

	#we must solve problem of key down durations: they vary from context
	durationOfKeyDown = 0.5

	keyboard = Controller()

	def pressStart(self):
		self.keyboard.press(self.keyStartGame)
		time.sleep(self.durationOfKeyDown)
		self.keyboard.release(self.keyStartGame)

	def pressUp(self):
		self.keyboard.press(self.keyUp)
		time.sleep(self.durationOfKeyDown)
		self.keyboard.release(self.keyUp)

	def pressDown(self):
		self.keyboard.press(self.keyDown)
		time.sleep(self.durationOfKeyDown)
		self.keyboard.release(self.keyDown)

	def pressLeft(self):
		self.keyboard.press(self.keyLeft)
		time.sleep(self.durationOfKeyDown)
		self.keyboard.release(self.keyLeft)

	def pressRight(self):
		self.keyboard.press(self.keyRight)
		time.sleep(self.durationOfKeyDown)
		self.keyboard.release(self.keyRight)

	def pressFire(self):
		self.keyboard.press(self.keyShoot)
		time.sleep(self.durationOfKeyDown)
		self.keyboard.release(self.keyShoot)
