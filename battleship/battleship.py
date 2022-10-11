from pynput.keyboard import Key, Listener, Controller
import pyautogui, os, time, random

from weapons.WeaponGeneric import WeaponGeneric

print('Hello, I am Python bot and I will try to play Battleship game on NES emulator :)')
print('Press q to start, set focus on the emulator window, and start the game :)')

class BattleshipBot:
	scriptPath = os.path.dirname(__file__)

	dirOfSprites = scriptPath + '/sprites/'
	dirOfFieldsSprites = dirOfSprites + 'fields/'
	dirOfGameplaySprites = dirOfSprites + 'gameplay/'
	dirOfWeaponsSprites = dirOfSprites + 'weapons/'

	crosshairSprite = dirOfFieldsSprites + 'crosshair.png'
	untouchedFieldSprite = dirOfFieldsSprites + 'untouched.png'

	scannableScreenRegion = (0, 40, 300, 280)

	battlefieldCoordsGrid = []
	fieldsStates = []

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
		time.sleep(0.02)
		self.keyboard.release(self.keyStartGame)

	def pressKeyShoot(self):
		self.keyboard.press(self.keyShoot)
		time.sleep(0.02)
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
			self.keyboard.press(keyboardKey)
			time.sleep(0.02)
			self.keyboard.release(keyboardKey)
		self.pressKeyShoot()

	def initBattlefieldCoordsGrid(self):
		coordsOfCrosshair = pyautogui.locateOnScreen(self.crosshairSprite)
		coordsOfAllFields = list(pyautogui.locateAllOnScreen(self.untouchedFieldSprite, region=self.scannableScreenRegion))
		coordsOfAllFields.insert(0, coordsOfCrosshair)
		for i in range(0, 96, 12):
			x = i
			self.battlefieldCoordsGrid.append(coordsOfAllFields[x:x+12])
		for listItem in self.battlefieldCoordsGrid:
			print(listItem)
		self.initFieldsStates()

	def initFieldsStates(self):
		self.fieldsStates = [['u']*12]*8
		print(self.fieldsStates)

	def playGame(self):
		print('initialized....')
		while 1==1 :
			try:
				while self.detectMenu() == None:
					print('Detecting game menu...')
				print('Game menu was detected! Giving you time to set focus on emulator window!')
				time.sleep(5)
				self.pressStart()
				time.sleep(5)
				while self.detectFinalShipSetup() == None:
					self.placeShipRandomly()
				self.pressKeyShoot()
				time.sleep(5)
				self.initBattlefieldCoordsGrid()
				weaponGeneric = WeaponGeneric()
				weaponGeneric.shoot()
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
