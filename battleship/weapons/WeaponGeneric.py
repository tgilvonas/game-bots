from pynput.keyboard import Key, Listener, Controller
import pyautogui, os, time, random

class WeaponGeneric:
	
	scannableScreenRegion = (0, 40, 300, 280)

	keyLeft='n'
	keyRight='m'
	keyDown='j'
	keyUp='h'
	keySelect='b'

	keyboard = Controller()

	def __init__(self):
		print('Weapon initiated')

	def shoot(self):
		print('Boom!')
