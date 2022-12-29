from pynput.keyboard import Controller, Key, Listener
import os, pyautogui, random, sys, time, traceback

from CommonProperties import CommonProperties

from weapons.Weapon1 import Weapon1
from weapons.Weapon2 import Weapon2
from weapons.Weapon3 import Weapon3
from weapons.Weapon4 import Weapon4

class CommanderOfTheFleet(CommonProperties):
	
	def __new__(cls, *args, **kwargs):
		return super().__new__(cls)

	def __init__(self):
		self.initialCrosshairSprite = self.dirOfFieldsSprites + 'crosshair-untouched.png'
		self.untouchedFieldSprite = self.dirOfFieldsSprites + 'untouched.png'

	battlefieldCoordsGrid = []
	fieldsStates = []

	spritesOfFields = {
		'hit': [
			'crosshair-hit.png',
			'hit.png'
		],
		'miss': [
			'crosshair-miss.png',
			'miss.png'
		],
		'untouched': [
			'crosshair-untouched.png',
			'untouched.png'
		],
		'sunk': [
			'sunk.png'
		]
	}
	spritesOfCrosshairs = [
		'crosshair-hit.png',
		'crosshair-miss.png',
		'crosshair-untouched.png'
	]

	scannableScreenRegionForBattlefield = (0, 40, 300, 180)

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
		coordsOfCrosshair = pyautogui.locateOnScreen(self.initialCrosshairSprite)
		self.battlefieldCoordsGrid = list(pyautogui.locateAllOnScreen(self.untouchedFieldSprite, region=self.scannableScreenRegionForBattlefield))
		self.battlefieldCoordsGrid.insert(0, coordsOfCrosshair)
		for listItem in self.battlefieldCoordsGrid:
			print(listItem)
		self.initFieldsStates()

	def initFieldsStates(self):
		self.fieldsStates = [['u']*12]*8
		for row in self.fieldsStates:
			print(row)

	def updateCurrentSituationInBattlefield(self):
		x=0
		y=0
		for field in self.battlefieldCoordsGrid:
			# y>7 is to prevent fatal error "index out of range", 
			# but it was also eliminated by defining new scannable screen region,
			# and fake empty field sprite from weapon indicator is no longer detected
			if y>7:
				break
			for fieldType in self.spritesOfFields.keys():
				for sprite in self.spritesOfFields[fieldType]:
					coordsOfDetectedField = pyautogui.locateOnScreen(self.dirOfFieldsSprites + sprite, region=(field[0], field[1], 16, 16))
					if coordsOfDetectedField != None:
						self.fieldsStates[y][x] = fieldType[0]
						print(fieldType[0]+': '+str(field[0])+', '+str(field[1]))
			if x>=11:
				x=0
				y+=1
			else:
				x+=1
		print('Fields states initialized')
		for row in self.fieldsStates:
			print(row)

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
				time.sleep(35)
				self.updateCurrentSituationInBattlefield()
				return False
			except Exception as e:
				print(e)
				raise
				#print(sys.exc_info()[2], 'Sorry I mean line...', traceback.tb_lineno(sys.exc_info()[2]))
				return False
