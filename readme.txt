This is a set of python scripts which read views from screen zones and try to play old Nintendo NES/Famicom games. I hope they will outsmart some primitive classic Nintendo games one day :)

These scripts are adjusted to FCEUX Nintendo emulator: http://fceux.com/web/download.html . Please note that they are adjusted to 256x224 pixels resolution of FCEUX emulator. This is done so because speed and quick reaction are very important in videogames meanwhile image reading and detection are very expensive functions in time. So, the smaller region of screen script needs to read, the faster it works.

To make scripts working:
1. Install Python on your PC, if you don't have Python installed;
2. Place FCEUX emulator window on very left-top corner of your screen, with approximate coordinates x=0 and y=0 (tolerance is around 20 pixels in both x and y screen coordinates); Please take notice that y=0 means "top of the screen" in computer screen coordinates.
3. Adjust your Windows screen resolution zoom settings to 100%
4. Set the equivalents of gamepad buttons for emulator, as listed in paragraph below.
5. Launch the script;
6. Press 'q' key;
7. Set focus on emulator window and start the game;
8. Enjoy the action and laugh at dummy game bots :)

Please keep in mind that it works only in your main monitor, not on additional monitor.

Equivalents of gamepad keys:
Button "B" - computer keyboard key 'z'
Button "B Turbo" - computer keyboard key 'a'
Button "A" - computer keyboard key 'x'
Button "A Turbo" - computer keyboard key 's'
Move left - computer keyboard key 'n'
Move right - computer keyboard key 'm'
Move down - computer keyboard key 'j'
Move up - computer keyboard key 'h'
Start/pause - computer keyboard key 'y'
Select - computer keyboard key 'b'
