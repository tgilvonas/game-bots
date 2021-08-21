This is a set of python scripts which read views from screen zones and try to play old Nintendo NES/Famicom games. I hope they will outsmart some primitive classic Nintendo games one day :)

These scripts are adjusted to FCEUX Nintendo emulator: http://fceux.com/web/download.html . Please note that they are adjusted to 256x224 pixels resolution of FCEUX emulator. This is done so because speed and quick reaction are very important in videogames meanwhile image reading and detection are very expensive functions in time. So, the smaller region of screen script needs to read, the faster it works.

To make scripts working:
1. Install Python on your PC, if you don't have Python installed;
2. Place FCEUX emulator window on very left-top corner of your screen, with approximate coordinates x=0 and y=0 (tolerance is around 20 pixels in both x and y screen coordinates);
3. Launch the script;
4. Press 'q' key;
5. Set focus on emulator window and start the game;
6. Enjoy the action and laugh from dummy game bots :)
