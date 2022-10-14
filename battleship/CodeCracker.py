from pynput.keyboard import Key, Listener, Controller
import pyautogui, os, time, random

from CommonProperties import CommonProperties

class CodeCracker(CommonProperties):

	def detectSelectedProperMenuItem(self):
		return pyautogui.locateOnScreen(self.dirOfGameplaySprites + 'code.png')

	# beginning to crack the code from '1000', flipping the string of numbers:
	def convertNumberToCode(self, i):
		oldUnits = i % 10
		oldDozens = i % 100 // 10
		oldHundreds = i % 1000 // 100
		oldThousands = i // 1000
		newUnits = oldThousands
		newDozens = oldHundreds * 10
		newHundreds = oldDozens * 100
		newThousands = oldUnits * 1000
		code = newThousands + newHundreds + newDozens + newUnits
		print(code)
		return [newThousands, newHundreds, newDozens, newUnits]

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
					code = self.convertNumberToCode(i)
					
					self.pressStart()
					i+=1
				return False
			except Exception as e:
				print(e)
