from pynput.keyboard import Key, Listener, Controller
import pyautogui, os, time, random

from CommonProperties import CommonProperties

class CodeCracker(CommonProperties):

	def detectSelectedProperMenuItem(self):
		return pyautogui.locateOnScreen(self.dirOfGameplaySprites + 'code.png')

	def convertNumberToCode(self, i):
		print(i)

	def crackTheCodes(self):
		print('Code cracker initiated! Giving you time to set focus on emulator window!')
		time.sleep(5)
		while 1==1 :
			try:
				while self.detectSelectedProperMenuItem() == None:
					self.pressDown()
					print('Selecting menu item...')
				i=1
				while i<=9999:
					self.pressStart()
					self.convertNumberToCode(i)
					self.pressStart()
					i+=1
					
				return False
			except Exception as e:
				print(e)
