from pynput.keyboard import Key, Listener, Controller
import pyautogui, os, time, random

from weapons.WeaponGeneric import WeaponGeneric

class Weapon1(WeaponGeneric):
	
	def shoot(self):
		print(self.weaponsSpritesPath)
		print('Weapon 1 shoots: Boom!')
