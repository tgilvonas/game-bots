from pynput.keyboard import Key, Listener, Controller
import pyautogui, os, time, random

print('Hello, I am Python bot and I will try to play old Galaxian game on NES emulator :)')
print('Press q to start, set focus on the emulator window, and start the game :)')

scriptPath = os.path.dirname(__file__)

spritesDir = scriptPath + '/sprites/'

pixelsOfInsects = [
	'insect-0.png',
	'insect-1.png',
	'insect-2.png'
]
pixelsOfEnemyGunfire = 'enemy-gunfire.png'

spriteOfMySpaceship = 'me-smaller.png';

scannableRegionForEnemiesAndGunfire = (2, 156, 276, 140)
scannableRegionOfMySpaceship = (10, 240, 270, 60)

keyShoot='z'
keyLeft='n'
keyRight='m'

keyboard = Controller()

def decideToGoLeftOrRight(coordinatesOfMySpaceship, coordinatesOfEnemyGunfires, coordinatesOfAttackingBugs):
	minMaxCoordinatesOfAttackingBugs = getMinMaxCoordinatesOfAttackingBugs(coordinatesOfAttackingBugs)
	whichSideIAm = detectOnWhichSideIsMySpaceship(coordinatesOfMySpaceship)
	if minMaxCoordinatesOfAttackingBugs != None and whichSideIAm != None:
		print('I AM ON: ')
		print(whichSideIAm)
		print('ENEMIES: ')
		print(minMaxCoordinatesOfAttackingBugs)
		if minMaxCoordinatesOfAttackingBugs[0] > 128 and minMaxCoordinatesOfAttackingBugs[1] > 128 and whichSideIAm == 'left' :
			print('GOING LEFT')
			goLeft()
		if minMaxCoordinatesOfAttackingBugs[0] < 128 and minMaxCoordinatesOfAttackingBugs[1] < 128 and whichSideIAm == 'right' :
			print('GOING RIGHT')
			goRight()
		print('GOING ANYWHERE')
		randomSide = random.randint(0,1)
		if randomSide == 0 :
			goLeft()
		else:
			goRight()
	return None

def goLeft():
	keyboard.release(keyRight)
	keyboard.press(keyLeft)

def goRight():
	keyboard.release(keyLeft)
	keyboard.press(keyRight)

# not accurate:
def detectOnWhichSideIsMySpaceship(coordinatesOfMySpaceship):
	arrayOfSides = ['left', 'right']
	if coordinatesOfMySpaceship == None:
		return None
	if coordinatesOfMySpaceship[0] < 127:
		return 'left'
	if coordinatesOfMySpaceship[0] + coordinatesOfMySpaceship[2] > 128:
		return 'right'
	return arrayOfSides[random.randint(0,1)]

def getMinMaxCoordinatesOfAttackingBugs(coordinatesOfAttackingBugs):
	if coordinatesOfAttackingBugs == None:
		return None
	arrayOfMinX = [301, 300]
	arrayOfMaxX = [0, 1]
	for coordinatesList in coordinatesOfAttackingBugs:
		arrayOfMinX.append(coordinatesList[0])
		arrayOfMaxX.append(coordinatesList[0] + coordinatesList[2])
	return [min(arrayOfMinX), max(arrayOfMaxX)]

# to do:
def detectIfEnemyGunfireIsGoingToHitMySpaceship(coordinatesOfMySpaceship, coordinatesOfEnemyGunfires):
	return ''

# to do: move this repeated function to library:
def detectAGroupOfObjects(arrayOfSprites, scannableScreenRegion):
	groupOfObjects = []
	for sprite in arrayOfSprites:
		groupOfObjects = groupOfObjects + list(pyautogui.locateAllOnScreen(spritesDir + sprite, region=scannableScreenRegion))
	return groupOfObjects

def playGame():

	print('initialized....')

	coordinatesOfMySpaceship = pyautogui.locateOnScreen(spritesDir + spriteOfMySpaceship, region=scannableRegionOfMySpaceship)

	while 1==1 :
		try:

			keyboard.press(keyShoot)

			coordinatesOfMySpaceship = pyautogui.locateOnScreen(spritesDir + spriteOfMySpaceship, region=scannableRegionOfMySpaceship)
			print('Coordinates of my spaceship:')
			print(coordinatesOfMySpaceship)

			coordinatesOfEnemyGunfires = list(pyautogui.locateAllOnScreen(spritesDir + pixelsOfEnemyGunfire, region=scannableRegionForEnemiesAndGunfire))

			coordinatesOfAttackingBugs = detectAGroupOfObjects(pixelsOfInsects, scannableRegionForEnemiesAndGunfire)

			keyboard.release(keyShoot)

			decideToGoLeftOrRight(coordinatesOfMySpaceship, coordinatesOfEnemyGunfires, coordinatesOfAttackingBugs)

		except Exception as e:
			print(e)

def on_press(key):
    if str(key)=="'q'":
        playGame()
    if key == Key.esc:
        return False

with Listener(on_press=on_press) as listener:
    listener.join()
