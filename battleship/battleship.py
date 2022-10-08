from pynput.keyboard import Key, Listener, Controller
import pyautogui, os, time, random

print('Hello, I am Python bot and I will try to play Battleship game on NES emulator :)')
print('Press q to start, set focus on the emulator window, and start the game :)')

class BattleshipBot:
	scriptPath = os.path.dirname(__file__)

	dirOfSprites = scriptPath + '/sprites/'
	dirOfFieldsSprites = dirOfSprites + 'fields/'
	dirOfGameplaySprites = dirOfSprites + 'gameplay/'
	dirOfWeaponsSprites = dirOfSprites + 'weapons/'

	keyLeft='n'
	keyRight='m'
	keyDown='j'
	keyUp='h'
	keySelect='b'
	keyShoot='x'
	keyRotate='z'
	keyStartGame='y'

	keyboard = Controller()

	def detectMenu(self):
		return pyautogui.locateOnScreen(self.dirOfGameplaySprites + 'start.png')

	def detectFinalShipSetup(self):
		return pyautogui.locateOnScreen(self.dirOfGameplaySprites + 'accept-setup.png')

	def pressStart(self):
		self.keyboard.press(self.keyStartGame)
		time.sleep(0.5)
		self.keyboard.release(self.keyStartGame)

	def pressKeyShoot(self):
		self.keyboard.press(self.keyShoot)
		time.sleep(0.5)
		self.keyboard.release(self.keyShoot)

	def generateListOfKeysToPlaceShip(self):
		possibleKeys = [self.keyLeft, self.keyRight, self.keyDown, self.keyUp, self.keyRotate]
		listOfKeys = []
		i = 1
		while i <= 10:
			listOfKeys.append(possibleKeys[random.randint(0, 4)])
			i+=1
		return listOfKeys

	def placeShipRandomly(self):
		listOfKeys = self.generateListOfKeysToPlaceShip()
		for keyboardKey in listOfKeys:
			print(keyboardKey)
			self.keyboard.press(keyboardKey)
			time.sleep(0.5)
			self.keyboard.release(keyboardKey)
		self.pressKeyShoot()
		print('Placing ship randomly')

	def playGame(self):
		print('initialized....')
		while 1==1 :
			try:
				while self.detectMenu() == None:
					print('Detecting game menu...')
				print('Game menu was detected! Giving you time to set focus on emulator window!')
				time.sleep(10)
				self.pressStart()
				time.sleep(10)
				while self.detectFinalShipSetup() == None:
					self.placeShipRandomly()
				self.pressKeyShoot()
				return False
			except Exception as e:
				print(e)

def on_press(key):
	battleshipBot = BattleshipBot()
	if str(key)=="'q'":
		battleshipBot.playGame()
	if key == Key.esc:
		return False

with Listener(on_press=on_press) as listener:
	listener.join()
