from pynput.keyboard import Key, Listener, Controller
import pyautogui, os, time, random

class CommonProperties:
	scriptPath = os.path.dirname(__file__)

	dirOfSprites = scriptPath + '/sprites/'
	dirOfFieldsSprites = dirOfSprites + 'fields/'
	dirOfGameplaySprites = dirOfSprites + 'gameplay/'
	dirOfWeaponsSprites = dirOfSprites + 'weapons/'

	scannableScreenRegion = (0, 40, 300, 280)

	keyLeft='n'
	keyRight='m'
	keyDown='j'
	keyUp='h'
	keySelect='b'
	keyShoot='x'
	keyRotate='z'
	keyStartGame='y'

	keyboard = Controller()

	def pressStart(self):
		self.keyboard.press(self.keyStartGame)
		time.sleep(0.02)
		self.keyboard.release(self.keyStartGame)
