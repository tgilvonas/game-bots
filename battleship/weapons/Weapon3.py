from pynput.keyboard import Key, Listener, Controller
import pyautogui, os, time, random

from weapons.WeaponGeneric import WeaponGeneric

class Weapon3(WeaponGeneric):
	
	def shoot(self):
		weaponSprite = self.weaponsSpritesPath + 'weapon3.png'
		while pyautogui.locateOnScreen(weaponSprite) == None:
			self.pressSelect()
			print('Selecting weapon...')
		self.moveCrosshairsDown()
		self.pressFire()
		print('Boom!')
