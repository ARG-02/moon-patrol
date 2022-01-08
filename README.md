# Moon Patrol
## A recreation of the hit Atari 2600 game, Moon Patrol

Moon Patrol is made with the PyGame library in Python and has the following features: 

- Endless Generation
  - Never Stops
  - Completely Random Generation
- Obstacles
  - White, Orange, and Purple aliens (all features included!)
  - Rocks
  - Holes
- Asthetic Choices
  - Scrolling background complete with stars and mountains
  - All Character and Death Animations
- Extra Additions
  - A max of 50 ammo which runs out as you shoot
  - Ammo crates spawn randomly
  - Lives can be earned by reaching 10000 points

* Tanks and mines are not added because objects are spawned randomly on the ground and would create too many enemies

## Requirements

 - A computer with python3.8 or higher installed
 - The pygame library (can be achieved by typing `pip install pygame` into terminal/cmd prompt)

## Install

To install, follow the instructions below.

 - Download this Github Repository.
 - Open a terminal/cmd prompt window and cd to the folder you put this game in
 - Open the `settings.toml` file and set the value to your screen size. For example, on 1080p displays, set it to `[1920, 1080]`
 - Values like whether or not you want to play in fullscreen can also be changed. 
 - Run the command `python main.py` to run the main script.

Note: if this running the main script fails, try reinstalling pygame with the requirements above or running `python3 main.py` instead.

## Controls

On the menu, press the down arrow to select the button below, or the up arrow to select the button above.
Then, press space to press the button.
To get out of a certain part of the menu or the game itself, press the escape key.  

Inside the game, press the left and right arrows to move forwards and backwards.
You can also press the up arrow to jump.
To shoot, press the space bar.

## Modifications

Want to change certain aspects this game? No problem!

If you want to change a constant (Like gravity, or how fast you move), this repository makes it incredibly easy to do so!

Instructions:
 - Open the code folder.
 - Then, open the modules folder and open the constants.py file with python idle or a different text editor.
 - You can then change the values next to variable names and these changes will show up in the game.
 
It is also possible to change an asset, like a texture, animation, sound, text, or even a font.

Instructions:
 - Open the content folder and then find an asset inside any of the folders contained in it.
 - Find the asset you want to replace or edit and place it in the folder you found it in with the same file name.
 
Note: Some texture changes may require changing the constants file accordingly depending on what it is.