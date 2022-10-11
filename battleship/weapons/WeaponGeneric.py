from pynput.keyboard import Key, Listener, Controller
import pyautogui, os, time, random

class WeaponGeneric:
	
	weaponsSpritesPath = ''

	scannableScreenRegion = (0, 40, 300, 280)

	keyLeft='n'
	keyRight='m'
	keyDown='j'
	keyUp='h'
	keySelect='b'

	keyboard = Controller()

	def __init__(self):
		print('Weapon initiated')
		appPath = os.path.dirname(__file__)
		appPath.replace("\\weapons", "")
		appPath.replace("/weapons", "")
		print('App path:')
		print(appPath)
		self.weaponsSpritesPath = appPath + 'sprites' + os.sep + 'weapons' + os.sep
