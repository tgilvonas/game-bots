from pynput.keyboard import Key, Listener, Controller
import pyautogui, os, time, random

from weapons.WeaponGeneric import WeaponGeneric

class Weapon1(WeaponGeneric):
	
	def shoot(self):
		weaponSprite = self.weaponsSpritesPath + 'weapon1.png'
		while pyautogui.locateOnScreen(weaponSprite) == None:
			self.pressSelect()
			print('Selecting weapon...')
		self.pressFire()
		print('Boom!')
