from pynput.keyboard import Key, Listener, Controller
import pyautogui, os, time, random

class WeaponGeneric:
	def __init__(self):
		print('Weapon initiated')

	def shoot(self):
		print('Boom')
