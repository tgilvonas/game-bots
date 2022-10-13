from pynput.keyboard import Key, Listener, Controller
import pyautogui, os, time, random

from weapons.WeaponGeneric import WeaponGeneric

class Weapon4(WeaponGeneric):
	
	def shoot(self):
		weaponSprite = self.weaponsSpritesPath + 'weapon4.png'
		while pyautogui.locateOnScreen(weaponSprite) == None:
			self.pressSelect()
			print('Selecting weapon...')
		self.moveCrosshairsRight()
		time.sleep(self.delayAfterCrosshairMovement)
		self.moveCrosshairsDown()
		time.sleep(self.delayAfterCrosshairMovement)
		self.pressFire()
		print('Boom!')
