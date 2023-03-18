from pynput.keyboard import Key, Listener

from CommanderOfTheFleet import CommanderOfTheFleet
from CodeCracker import CodeCracker

print('Hello, I am Python bot and I will try to play Battleship game on NES emulator :)')
print('Press q to start me, set focus on the emulator window, and start the game :)')

def on_press(key):
	if str(key)=="'q'":
		commanderOfTheFleet = CommanderOfTheFleet()
		commanderOfTheFleet.playGame()
	if str(key)=="'w'":
		codeCracker = CodeCracker()
		codeCracker.crackTheCodes()
	if key == Key.esc:
		return False

with Listener(on_press=on_press) as listener:
	listener.join()
