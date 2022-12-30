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
	normalizedBattlefieldCoordsGrid = []
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
		possibleKeys = [self.keyLeft, self.keyRight, self.keyDown, self.keyUp, self.keyRotate, self.keyRight, self.keyDown]
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

	def updateCurrentSituationInBattlefield(self):
		print('Updating current situation in battlefied')
		x=0
		self.fieldsStates = []
		rowOfFields = []
		rowOfBattlefieldCoordsGrid = []
		for field in self.battlefieldCoordsGrid:
			for fieldType in self.spritesOfFields.keys():
				for sprite in self.spritesOfFields[fieldType]:
					coordsOfDetectedField = pyautogui.locateOnScreen(self.dirOfFieldsSprites + sprite, region=(field[0], field[1], 16, 16))
					if coordsOfDetectedField != None:
						rowOfFields.append(fieldType[0])
						rowOfBattlefieldCoordsGrid.append(coordsOfDetectedField)
			if x>=11:
				x=0
				self.fieldsStates.append(rowOfFields)
				self.normalizedBattlefieldCoordsGrid.append(rowOfBattlefieldCoordsGrid)
				rowOfFields = []
				rowOfBattlefieldCoordsGrid = []
			else:
				x+=1
		print('Fields states updated')
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

	def aimAndShoot(self):
		hitCoords = self.detectFirstHit()
		print(hitCoords)
		if hitCoords != False:
			targetCoords = self.decideTargetCoords(hitCoords)
		else:
			targetCoords = self.selectFieldForNewTarget()
		print(targetCoords)
		self.adjustCrosshair(targetCoords)
		self.pressFire()

	def adjustCrosshair(self, targetCoords):
		print('Adjusting crosshair')
		crosshairCords = self.detectCrosshair()
		while targetCoords[0]!=crosshairCords[0] and targetCoords[1]!=crosshairCords[1]:
			while targetCoords[0]>crosshairCords[0]:
				self.pressRight()
				crosshairCords[0]+=1
			while targetCoords[0]<crosshairCords[0]:
				self.pressLeft()
				crosshairCords[0]-=1
			while targetCoords[1]>crosshairCords[1]:
				self.pressDown()
				crosshairCords[1]+=1
			while targetCoords[1]<crosshairCords[1]:
				self.pressUp()
				crosshairCords[1]-=1
			crosshairCoords = self.detectCrosshair()
		return False

	def detectCrosshair(self):
		print('Detecting crosshair')
		for crosshairSprite in self.spritesOfCrosshairs:
			crosshairCoords = pyautogui.locateOnScreen(self.dirOfFieldsSprites+crosshairSprite)
			if crosshairCoords != None:
				break
		print('Finding crosshair in normalized battlefield coords grid')
		x=0
		y=0
		for fieldsRow in self.normalizedBattlefieldCoordsGrid:
			for field in fieldsRow:
				if crosshairCoords[0]==field[0] and crosshairCoords[1]==field[1]:
					return [x, y]
				x+=1
			x=0
			y+=1
		return False

	def decideTargetCoords(self, hitCoords):
		print('Deciding target coords')
		if hitCoords[1]>0 and self.fieldsStates[hitCoords[1]-1][hitCoords[0]]=='u':
			targetCoords = [hitCoords[0], hitCoords[1]-1]
		if hitCoords[1]<7 and self.fieldsStates[hitCoords[1]+1][hitCoords[0]]=='u':
			targetCoords = [hitCoords[0], hitCoords[1]+1]
		if hitCoords[0]>0 and self.fieldsStates[hitCoords[1]][hitCoords[0]-1]=='u':
			targetCoords = [hitCoords[0]-1, hitCoords[1]]
		if hitCoords[0]<11 and self.fieldsStates[hitCoords[1]][hitCoords[0]+1]=='u':
			targetCoords = [hitCoords[0]+1, hitCoords[1]]
		return targetCoords

	def selectFieldForNewTarget(self):
		print('Selecting field for new target')
		x=0
		y=0
		fs = self.fiedsStates
		for fieldsRow in self.fieldsStates:
			for field in fieldsRow:
				if x>0 and y>0 and x<11 and y<7 and fs[y][x]=='u':
					if fs[y-1][x] in ['u', 'h', 'm'] and fs[y+1][x] in ['u', 'h', 'm'] and fs[y][x-1] in ['u', 'h', 'm'] and fs[y][x-1] in ['u', 'h', 'm']:
						return [x, y]
				x+=1
			x=0
			y+=1
		return False

	def detectFirstHit(self):
		print('Detecting first hit')
		x=0
		y=0
		for fieldsRow in self.fieldsStates:
			for field in fieldsRow:
				if field=='h':
					print('Hit detected')
					return [x, y]
				x+=1
			x=0
			y+=1
		print('Hit not detected')
		return False

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
				while 1==1:
					self.aimAndShoot()
					time.sleep(35)
					self.updateCurrentSituationInBattlefield()
					self.aimAndShoot()
				return False
			except Exception as e:
				print(e)
				return False
