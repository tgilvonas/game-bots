from pynput.keyboard import Key, Listener, Controller
import pyautogui, os, time

# path info of files:
print(os.path.dirname(__file__))

print('Hello, I am Python bot and I will try to play old RoadFighter game on NES emulator :)')
print('Press q to start, set focus on the emulator window, and start the game :)')

scriptPath = os.path.dirname(__file__)

spritesDir = scriptPath + '/sprites/'
roadsidesDir = spritesDir + 'roadsides/'

#keys:
keyAccelerate='z'
keyAccelerateMore='x'
keyLeft='n'
keyRight='m'

# dimesions of scannable screen region
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
	'car3.png'
]

spriteOfTargetCar = 'target.png'

def detectLeftRoadside():
	leftRoadSides = []
	leftRoadSideToReturn = 82;
	for roadside in spritesOfLeftRoadSides:
		leftRoadSides = leftRoadSides + list(pyautogui.locateAllOnScreen(roadsidesDir + roadside, region=scannableScreenRegion))
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

def detectRightRoadSide():
	rightRoadSides = []
	rightRoadSideToReturn = 290
	for roadside in spritesOfRightRoadSides:
		rightRoadSides = rightRoadSides + list(pyautogui.locateAllOnScreen(roadsidesDir + roadside, region=scannableScreenRegion))

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

def detectObject(sprite):
	coordinatesOfObject = pyautogui.locateOnScreen(spritesDir + sprite, region=scannableScreenRegion)
	print('Detected single object: ')
	print(sprite)
	print(coordinatesOfObject)
	return coordinatesOfObject

def detectAGroupOfObjects(arrayOfSprites):
	groupOfObjects = []
	for sprite in arrayOfSprites:
		groupOfObjects = groupOfObjects + list(pyautogui.locateAllOnScreen(spritesDir + sprite, region=scannableScreenRegion))
	print('Group of objects: ')
	print(groupOfObjects)
	return groupOfObjects

def detectOnWhichSideOfTheRoadIAm(coordinatesOfMe, leftRoadSide, rightRoadSide):
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

def checkIfObjectDoesNotIntersectWithOtherObjects(objectToCheck, arrayOfOtherObjects):
	if objectToCheck != None and len(objectToCheck) == 4  and arrayOfOtherObjects != None :
		objectLeft = objectToCheck[0];
		objectRight = objectToCheck[0] + objectToCheck[2]
		for obstacle in arrayOfOtherObjects:
			obstacleLeft = obstacle[0]
			obstacleRight = obstacle[0] + obstacle[2]
			if (objectLeft >= obstacleLeft and objectLeft <= obstacleRight) or (objectRight >= obstacleLeft and objectRight <= obstacleRight) :
				return True
	return False

def checkIfSpeedIsAbove220():
	coordinatesOfSpeedometerPart = pyautogui.locateOnScreen(spritesDir + 'speed-above-220.png', region=(190, 96, 27, 94))
	return (coordinatesOfSpeedometerPart != None and len(coordinatesOfSpeedometerPart) == 4)

def playGame():
	print('initialized....')

	keyboard = Controller()

	leftRoadSide = 82
	rightRoadSide = 290
	whichRoadside = 'left'
	slowOrPassiveObjects = []
	trickyCars = []

	while 1==1 :
		try:
			keyboard.press(keyAccelerate)

			leftRoadSide = detectLeftRoadside()
			rightRoadSide = detectRightRoadSide()

			coordinatesOfMe = detectObject(spriteOfMe)

			slowOrPassiveObjects = detectAGroupOfObjects(spritesOfSlowOrPassiveObjects)
			trickyCars = detectAGroupOfObjects(spritesOfTrickyCars)

			coordinatesOfTargetCar= detectObject(spriteOfTargetCar)

			if coordinatesOfMe == None:
				keyboard.release(keyAccelerateMore)

			myCarIntersectsWithSlowOrPassiveObjects = checkIfObjectDoesNotIntersectWithOtherObjects(coordinatesOfMe, slowOrPassiveObjects)
			if myCarIntersectsWithSlowOrPassiveObjects == True :
				keyboard.release(keyAccelerateMore)
				whichRoadside = detectOnWhichSideOfTheRoadIAm(coordinatesOfMe, leftRoadSide, rightRoadSide)
				while (checkIfObjectDoesNotIntersectWithOtherObjects(detectObject(spriteOfMe), detectAGroupOfObjects(spritesOfSlowOrPassiveObjects))) :
					if whichRoadside == 'left' :
						keyboard.press(keyRight)
					else :
						keyboard.press(keyLeft)
				keyboard.release(keyLeft)
				keyboard.release(keyRight)

			# still repeated code by reason: I don't know what strategy should be with "tricky" cars:
			myCarIntersectsWithTrickyCars = checkIfObjectDoesNotIntersectWithOtherObjects(coordinatesOfMe, trickyCars)
			if myCarIntersectsWithTrickyCars == True :
				keyboard.release(keyAccelerateMore)
				whichRoadside = detectOnWhichSideOfTheRoadIAm(coordinatesOfMe, leftRoadSide, rightRoadSide)
				while (checkIfObjectDoesNotIntersectWithOtherObjects(detectObject(spriteOfMe), detectAGroupOfObjects(spritesOfTrickyCars))) :
					if whichRoadside == 'left' :
						keyboard.press(keyRight)
					else :
						keyboard.press(keyLeft)
				keyboard.release(keyLeft)
				keyboard.release(keyRight)

			#if coordinatesOfTargetCar != None and (checkIfObjectDoesNotIntersectWithOtherObjects(coordinatesOfTargetCar, slowOrPassiveObjects + trickyCars) == False):
			#keyboard.release(keyAccelerateMore)

			if checkIfSpeedIsAbove220() and myCarIntersectsWithSlowOrPassiveObjects == False and myCarIntersectsWithTrickyCars == False :
				keyboard.press(keyAccelerateMore)

		except Exception as e:
			print(e)


def on_press(key):
    if str(key)=="'q'":
        playGame()
    if key == Key.esc:
        return False

with Listener(on_press=on_press) as listener:
    listener.join()
