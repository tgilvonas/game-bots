from pynput.keyboard import Key, Controller
import pyautogui, os, time

class Racer():

	scriptPath = os.path.dirname(__file__)

	spritesDir = scriptPath + '/sprites-optimized/'
	roadsidesDir = spritesDir + 'roadsides/'

	#keys:
	keyAccelerate='z'
	keyAccelerateMore='x'
	keyLeft='n'
	keyRight='m'

	#dimesions of scannable screen region
	scannableScreenRegion = (32, 36, 160, 240)

	spriteOfMe = 'me.png'

	spritesOfLeftRoadSides = [
		'left1.png',
		'left2.png'
	]

	spritesOfRightRoadSides = [
		'right1.png',
		'right2.png'
	]

	spritesOfSlowOrPassiveObjects = [
		'car0.png',
		'oil.png',
		'truck.png'
	]

	spritesOfTrickyCars = [
		'car1.png',
		'car2.png',
		'car3.png',
		'car4.png'
	]

	spriteOfTargetCar = 'target.png'

	lengthOfRoadObjects = 32

	def detectLeftRoadside(self):
		leftRoadSides = []
		leftRoadSideToReturn = 82;
		for roadside in self.spritesOfLeftRoadSides:
			leftRoadSides = leftRoadSides + list(pyautogui.locateAllOnScreen(self.roadsidesDir + roadside, region=self.scannableScreenRegion))
		if len(leftRoadSides) > 0 :
			lastLeftRoadSide = leftRoadSides[-1]
			if len(lastLeftRoadSide) == 4:
				leftRoadSideToReturn = lastLeftRoadSide[0] + lastLeftRoadSide[2]
				print('Left roadside: ')
				print(leftRoadSideToReturn)
			else :
				print('No left roadsides')
		else :
			print('No left roadsides')
		return leftRoadSideToReturn

	def detectRightRoadSide(self):
		rightRoadSides = []
		rightRoadSideToReturn = 290
		for roadside in self.spritesOfRightRoadSides:
			rightRoadSides = rightRoadSides + list(pyautogui.locateAllOnScreen(self.roadsidesDir + roadside, region=self.scannableScreenRegion))

		if len(rightRoadSides) > 0 :
			lastRightRoadSide = rightRoadSides[-1]
			if len(lastRightRoadSide) == 4 :
				rightRoadSideToReturn = lastRightRoadSide[0]
				print('Right roadside: ')
				print(rightRoadSideToReturn)
			else :
				print('No right roadsides')
		else :
			print('No right roadsides')
		return rightRoadSideToReturn

	def detectObject(self, sprite):
		coordinatesOfObject = pyautogui.locateOnScreen(self.spritesDir + sprite, region=self.scannableScreenRegion)
		print('Detected single object: ')
		print(sprite)
		print(coordinatesOfObject)
		return coordinatesOfObject

	def detectAGroupOfObjects(self, arrayOfSprites):
		groupOfObjects = []
		for sprite in arrayOfSprites:
			groupOfObjects = groupOfObjects + list(pyautogui.locateAllOnScreen(self.spritesDir + sprite, region=self.scannableScreenRegion, grayscale=True))
		print('Group of objects: ')
		print(groupOfObjects)
		return groupOfObjects

	def detectOnWhichSideOfTheRoadIAm(self, coordinatesOfMe, leftRoadSide, rightRoadSide):
		if coordinatesOfMe != None and len(coordinatesOfMe) == 4 :
			leftTopCorner = coordinatesOfMe[0]
			rightTopCorner = coordinatesOfMe[0] + coordinatesOfMe[2]
			differenceLeft = leftTopCorner - leftRoadSide
			differenceRight = rightRoadSide - rightTopCorner
			if differenceLeft > differenceRight :
				print('Position: right')
				return 'right'
			else :
				print('Position: left')
				return 'left'
		else :
			print('Unknown position of my car. Maybe crashed, or course is finished.')
			return 'left'

	def checkIfObjectIntersectsWithOthers(self, objectToCheck, arrayOfOtherObjects):
		if objectToCheck != None and len(objectToCheck) == 4  and arrayOfOtherObjects != None :
			objectLeft = objectToCheck[0];
			objectRight = objectToCheck[0] + objectToCheck[2]
			for obstacle in arrayOfOtherObjects:
				obstacleLeft = obstacle[0]
				obstacleRight = obstacle[0] + obstacle[2]
				if (objectLeft >= obstacleLeft and objectLeft <= obstacleRight) or (objectRight >= obstacleLeft and objectRight <= obstacleRight) :
					return True
		return False

	def checkIfSpeedIsAbove220(self):
		coordinatesOfSpeedometerPart = pyautogui.locateOnScreen(self.spritesDir + 'speed-above-220.png', region=(190, 96, 27, 94))
		return (coordinatesOfSpeedometerPart != None and len(coordinatesOfSpeedometerPart) == 4)

	def playGame(self):
		print('initialized....')

		keyboard = Controller()

		leftRoadSide = 82
		rightRoadSide = 290
		whichRoadside = 'left'
		slowOrPassiveObjects = []
		trickyCars = []

		while 1==1 :
			try:
				keyboard.press(self.keyAccelerate)

				leftRoadSide = self.detectLeftRoadside()
				rightRoadSide = self.detectRightRoadSide()

				coordinatesOfMe = self.detectObject(self.spriteOfMe)

				slowOrPassiveObjects = self.detectAGroupOfObjects(self.spritesOfSlowOrPassiveObjects)
				trickyCars = self.detectAGroupOfObjects(self.spritesOfTrickyCars)

				coordinatesOfTargetCar = self.detectObject(self.spriteOfTargetCar)

				if coordinatesOfMe == None:
					keyboard.release(self.keyAccelerateMore)

				myCarIntersectsWithSlowOrPassiveObjects = self.checkIfObjectIntersectsWithOthers(coordinatesOfMe, slowOrPassiveObjects)
				if myCarIntersectsWithSlowOrPassiveObjects == True :
					keyboard.release(self.keyAccelerateMore)
					whichRoadside = self.detectOnWhichSideOfTheRoadIAm(coordinatesOfMe, leftRoadSide, rightRoadSide)
					while(self.checkIfObjectIntersectsWithOthers(self.detectObject(self.spriteOfMe), self.detectAGroupOfObjects(self.spritesOfSlowOrPassiveObjects))):
						if whichRoadside == 'left' :
							keyboard.press(self.keyRight)
						else :
							keyboard.press(self.keyLeft)
					keyboard.release(self.keyLeft)
					keyboard.release(self.keyRight)

				# still repeated code by reason: I don't know what strategy should be with "tricky" cars:
				myCarIntersectsWithTrickyCars = self.checkIfObjectIntersectsWithOthers(coordinatesOfMe, trickyCars)
				if myCarIntersectsWithTrickyCars == True :
					keyboard.release(self.keyAccelerateMore)
					whichRoadside = self.detectOnWhichSideOfTheRoadIAm(coordinatesOfMe, leftRoadSide, rightRoadSide)
					while (self.checkIfObjectIntersectsWithOthers(detectObject(self.spriteOfMe), detectAGroupOfObjects(self.spritesOfTrickyCars))) :
						if whichRoadside == 'left' :
							keyboard.press(self.keyRight)
						else :
							keyboard.press(self.keyLeft)
					keyboard.release(self.keyLeft)
					keyboard.release(self.keyRight)

				#if self.checkIfSpeedIsAbove220() and myCarIntersectsWithSlowOrPassiveObjects == False and myCarIntersectsWithTrickyCars == False :
				#	keyboard.press(self.keyAccelerateMore)

			except Exception as e:
				print(e)
