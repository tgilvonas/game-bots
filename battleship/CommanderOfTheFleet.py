from pynput.keyboard import Key, Listener, Controller
import pyautogui, os, time, random

from CommonProperties import CommonProperties

from weapons.Weapon1 import Weapon1
from weapons.Weapon2 import Weapon2
from weapons.Weapon3 import Weapon3
from weapons.Weapon4 import Weapon4

class CommanderOfTheFleet(CommonProperties):
	
	def __new__(cls, *args, **kwargs):
		return super().__new__(cls)

	def __init__(self):
		self.crosshairSprite = self.dirOfFieldsSprites + 'crosshair.png'
		self.untouchedFieldSprite = self.dirOfFieldsSprites + 'untouched.png'

	battlefieldCoordsGrid = []
	fieldsStates = []

	def detectMenu(self):
		return pyautogui.locateOnScreen(self.dirOfGameplaySprites + 'start.png')

	def detectFinalShipSetup(self):
		return pyautogui.locateOnScreen(self.dirOfGameplaySprites + 'accept-setup.png')

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

	def useSuperWeapons(self):
		weapon1 = Weapon1()
		weapon1.shoot()
		weapon2 = Weapon2()
		weapon2.shoot()
		weapon3 = Weapon3()
		weapon3.shoot()
		weapon4 = Weapon4()
		weapon4.shoot()

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
				print('Placing boats in battlefied...')
				while self.detectFinalShipSetup() == None:
					self.placeShipRandomly()
				self.pressKeyShoot()
				time.sleep(5)
				self.initBattlefieldCoordsGrid()
				self.useSuperWeapons()
				return False
			except Exception as e:
				print(e)
