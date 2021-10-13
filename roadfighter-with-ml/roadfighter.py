import json, pyautogui, os, sqlite3, sys, time, traceback
from pynput.keyboard import Key, Listener, Controller
from time import sleep

# path info of files:
print(os.path.dirname(__file__))

print('Hello, I am Python bot and I will try to play old RoadFighter game on NES emulator :)')
print("Press 'q' to start, set focus on the emulator window, and start the game :)")

scriptPath = os.path.dirname(__file__)

spritesDir = scriptPath + '/sprites/'
roadsidesDir = spritesDir + 'roadsides/'

databaseFile = '/hypothesies.sqlite'

# keys:
keyAccelerate='z'
keyAccelerateMore='x'
keyLeft='n'
keyRight='m'
keyStartGame='y'

#for ML:
keysHistory={}
dataOfAllObjects={}
hypothesisEvaluation=0
logHypothesis = True
momentOfTime=0
keyNumber=0
parentHypothesisId=0
previousObjectsOnTrack=[]

# dimesions of scannable screen region
scannableScreenRegion = (32, 40, 160, 222)

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

# sprites to determine state of gameplay:
spriteOfGameLogo = 'game-logo.png'
spriteZeroFuel = 'zero-fuel.png'
spriteOfProgressIndicator = 'progress-indicator.png'

# global "keyboard controller" object:
keyboard = Controller()

def detectLeftRoadside():
	global scannableScreenRegion
	global roadsidesDir
	global spritesOfLeftRoadSides
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
	global scannableScreenRegion
	global roadsidesDir
	global spritesOfRightRoadSides
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
	global scannableScreenRegion
	global spritesDir
	coordinatesOfObject = pyautogui.locateOnScreen(spritesDir + sprite, region=scannableScreenRegion)
	print('Detected single object: ')
	print(sprite)
	print(coordinatesOfObject)
	return coordinatesOfObject

def detectAGroupOfObjects(arrayOfSprites):
	global scannableScreenRegion
	global spritesDir
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

def detectGameLogo():
	global spritesDir
	global spriteOfGameLogo
	coordinatesOfLogo = pyautogui.locateOnScreen(spritesDir + spriteOfGameLogo, region=(3, 68, 240, 140))
	return coordinatesOfLogo

def detectIfFuelLevelIsZero():
	global spritesDir
	global spriteZeroFuel
	coordinatesOfZeroFuelSprite = pyautogui.locateOnScreen(spritesDir + spriteZeroFuel, region=(200, 190, 60, 50))
	return coordinatesOfZeroFuelSprite

def resetInitialData():
	global leftRoadSide
	global rightRoadSide
	global whichRoadside
	global slowOrPassiveObjects
	global trickyCars
	global hypothesisEvaluation
	global logHypothesis
	leftRoadSide = 82
	rightRoadSide = 150
	whichRoadside = 'left'
	slowOrPassiveObjects = []
	trickyCars = []
	hypothesisEvaluation=0
	logHypothesis = True

def goThroughGameInterface():
	keyboard.press(keyStartGame)
	sleep(0.5)
	keyboard.release(keyStartGame)
	sleep(2)
	keyboard.press(keyStartGame)
	sleep(0.5)
	keyboard.release(keyStartGame)

def evaluateHypothesisByProgressIndicator():
	global hypothesisEvaluation
	positionOfProgressIndicator = pyautogui.locateOnScreen(spritesDir + spriteOfProgressIndicator, region=(10, 50, 25, 220))
	if (positionOfProgressIndicator != None) :
		hypothesisEvaluation = 300 - positionOfProgressIndicator[1]
	return hypothesisEvaluation

def writeHypothesisToDatabase():
	global hypothesisEvaluation
	global keysHistory
	global hypothesisEvaluation
	global dataOfAllObjects
	global parentHypothesisId
	global databaseFile
	dbConnection = sqlite3.connect(scriptPath + databaseFile)
	allEvaluationsOfHypothesies = {}
	allEvaluationsOfHypothesies['e1'] = hypothesisEvaluation
	dbConnectionCursor = dbConnection.cursor()
	dbConnectionCursor.execute("INSERT INTO hypothesies (parent_id, keys_history, hypothesis, evaluations, average_evaluation, passive_objects, passive_objects_processed) VALUES (?, ?, NULL, ?, ?, ?, NULL)", (parentHypothesisId, json.dumps(keysHistory), json.dumps(allEvaluationsOfHypothesies), hypothesisEvaluation, json.dumps(dataOfAllObjects)))
	dbConnection.commit()
	dbConnectionCursor.close()
	dbConnection.close()

def getBestHypothesisFromDatabase():
	global dataOfAllObjects
	global databaseFile
	hypothesis = {}
	dbConnection = sqlite3.connect(scriptPath + databaseFile)
	dbConnectionCursor = dbConnection.cursor()
	dbConnectionCursor.execute('SELECT * FROM hypothesies ORDER BY average_evaluation DESC LIMIT 1')
	hypothesis = dbConnectionCursor.fetchone()
	dbConnectionCursor.close()
	dbConnection.close()
	print('Hypothesis:')
	print(hypothesis)
	return hypothesis

def logKey(key, action):
	global momentOfTime
	global keysHistory
	global keyNumber
	keyHappened = {
        'action': '',
        'key': '',
        'wait': 0
    }
	keyHappened['action']=action
	keyHappened['key']=str(key)
	keyHappened['wait']=time.time_ns()-momentOfTime
	momentOfTime=time.time_ns()
	keysHistory['key'+str(keyNumber)]=keyHappened
	keyNumber+=1

def logObjectsOnTrack(groupOfObjects, tricky=False):
	global momentOfTime
	global dataOfAllObjects
	groupOfObjectsToLog = []
	if tricky:
		reserve=10
	else:
		reserve=30
	if (groupOfObjects != None and len(groupOfObjects)>0):
		for objectOfSomething in groupOfObjects:
			# giving a tolerance and reserve, making objects "wider":
			groupOfObjectsToLog.append([objectOfSomething[0] - reserve, objectOfSomething[1], objectOfSomething[2] + (2*reserve), objectOfSomething[3]])
		waitTime = time.time_ns()-momentOfTime
		groupOfObjectsAtTheMoment = {
			'wait': waitTime,
			'objects': groupOfObjectsToLog
		}
		dataOfAllObjects['t'+str(waitTime)] = groupOfObjectsAtTheMoment
		momentOfTime=time.time_ns()

def tryToPlayUnknownPartOfGame():
	global logHypothesis
	global spritesOfSlowOrPassiveObjects
	global spritesOfTrickyCars
	global spriteOfMe
	global keyLeft
	global keyRight
	while detectIfFuelLevelIsZero() == None:
		leftRoadSide = detectLeftRoadside()
		rightRoadSide = detectRightRoadSide()

		slowOrPassiveObjects = detectAGroupOfObjects(spritesOfSlowOrPassiveObjects)
		logObjectsOnTrack(slowOrPassiveObjects, False)
		trickyCars = detectAGroupOfObjects(spritesOfTrickyCars, True)
		logObjectsOnTrack(trickyCars)

		coordinatesOfTargetCar= detectObject(spriteOfTargetCar)

		coordinatesOfMe = detectObject(spriteOfMe)
		if (coordinatesOfMe == None and logHypothesis == True):
			print('CRASHED or collided with objects. Writing hypothesis to DB.')
			evaluateHypothesisByProgressIndicator()
			writeHypothesisToDatabase()
			logHypothesis = False
			#keyboard.release(keyAccelerateMore)

		myCarIntersectsWithSlowOrPassiveObjects = checkIfObjectDoesNotIntersectWithOtherObjects(coordinatesOfMe, slowOrPassiveObjects)
		if myCarIntersectsWithSlowOrPassiveObjects == True :
			keyboard.release(keyAccelerateMore)
			whichRoadside = detectOnWhichSideOfTheRoadIAm(coordinatesOfMe, leftRoadSide, rightRoadSide)
			while (checkIfObjectDoesNotIntersectWithOtherObjects(detectObject(spriteOfMe), detectAGroupOfObjects(spritesOfSlowOrPassiveObjects))) :
				if whichRoadside == 'left' :
					keyboard.press(keyRight)
					logKey(keyRight, 'pressed')
				else :
					keyboard.press(keyLeft)
					logKey(keyLeft, 'pressed')
			keyboard.release(keyLeft)
			logKey(keyLeft, 'released')
			keyboard.release(keyRight)
			logKey(keyRight, 'released')

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
			logKey(keyLeft, 'released')
			keyboard.release(keyRight)
			logKey(keyRight, 'released')

		#if checkIfSpeedIsAbove220() and myCarIntersectsWithSlowOrPassiveObjects == False and myCarIntersectsWithTrickyCars == False :
		#	keyboard.press(keyAccelerateMore)
	return None

def getListOfObjectsWithPreviousObjectsOnTrack(currentObjects):
	global previousObjectsOnTrack
	for currentObject in currentObjects:
		previousObjectsOnTrack.append(currentObject)
	if (len(previousObjectsOnTrack)>8):
		return previousObjectsOnTrack[-8:]
	return previousObjectsOnTrack

def decideToTurnLeftOrRight(coordinatesOfMe, leftRoadSide, rightRoadSide, objects):
	listOfEmptyPixels = [1] * 270
	for x in range(leftRoadSide, rightRoadSide):
  		listOfEmptyPixels[x] = 0
	for currentObject in objects:
		for x in range(currentObject[0], currentObject[0]+currentObject[2]):
			listOfEmptyPixels[x] = 1
	leftSideOfMe = coordinatesOfMe[0];
	rightSideOfMe = coordinatesOfMe[0] + coordinatesOfMe[2]
	distanceLeft=0
	distanceRight=0
	x = rightSideOfMe
	while x<rightRoadSide:
		while listOfEmptyPixels[x]==1:
			distanceRight+=1
		x+=1
	x = leftSideOfMe
	while x>leftRoadSide:
		while listOfEmptyPixels[x]==1:
			distanceLeft+=1
		x-=1
	if distanceLeft<distanceRight:
		return 'left'
	return 'right'

def tryToPlayByKeysHistory():
	# code has not been written yet
	return None

def tryToPlayByObjectsData():
	global dataOfAllObjects
	global keyLeft
	global keyRight
	global spriteOfMe
	global logHypothesis
	timeBeforeIteration = 0
	timeAfterIteration = 0
	hypothesis = getBestHypothesisFromDatabase()
	if (hypothesis != None and len(hypothesis)>=7):
		dataOfAllObjects = json.loads(hypothesis[6])
		for objectsHistoryIndex in dataOfAllObjects:
			timeBeforeIteration = time.time_ns()
			coordinatesOfMe = detectObject(spriteOfMe)
			if coordinatesOfMe == None:
				logHypothesis = False
				print('CRASHED')
				return None
			leftRoadSide = detectLeftRoadside()
			rightRoadSide = detectRightRoadSide()
			objectsOnTrack = getListOfObjectsWithPreviousObjectsOnTrack(dataOfAllObjects[objectsHistoryIndex]['objects'])
			whichRoadside = decideToTurnLeftOrRight(coordinatesOfMe, leftRoadSide, rightRoadSide, objectsOnTrack)
			while (checkIfObjectDoesNotIntersectWithOtherObjects(detectObject(spriteOfMe), objectsOnTrack)) :
				if whichRoadside == 'left' :
					keyboard.press(keyRight)
					logKey(keyRight, 'pressed')
				else :
					keyboard.press(keyLeft)
					logKey(keyLeft, 'pressed')
			keyboard.release(keyLeft)
			logKey(keyLeft, 'released')
			keyboard.release(keyRight)
			logKey(keyRight, 'released')
			coordinatesOfMe = detectObject(spriteOfMe)
			if coordinatesOfMe == None:
				logHypothesis = False
				print('CRASHED')
				return None
			timeAfterIteration = time.time_ns()
			sleep((dataOfAllObjects[objectsHistoryIndex]['wait'] - (timeAfterIteration - timeBeforeIteration)) / (1000 * 1000 * 1000))
	return None


def tryToPlayGameInfiniteLoop():
	
	global momentOfTime
	global keyAccelerate
	global logHypothesis

	print('initialized...')

	while 1==1 :

		try:
			while detectGameLogo() == None:
				print(detectGameLogo())
				print('Detecting logo in game intro...')
			print('Logo in game intro detected!')

			resetInitialData()
			#momentOfTime=time.time_ns()

			goThroughGameInterface()

			keyboard.press(keyAccelerate)
			sleep(9)

			momentOfTime=time.time_ns()

			tryToPlayByObjectsData()
			tryToPlayUnknownPartOfGame()
			logHypothesis = True

		except Exception as e:
			print(e)
			print(traceback.format_exc())


def on_press(key):
    if str(key)=="'q'":
        tryToPlayGameInfiniteLoop()
    if key == Key.esc:
        return False

with Listener(on_press=on_press) as listener:
    listener.join()
