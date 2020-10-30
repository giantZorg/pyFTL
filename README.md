# pyFTL
Rebuild of FTL in python for better modding accessability. It will require the base game to be installed locally, which can be bought here:

- https://store.steampowered.com/app/212680/FTL_Faster_Than_Light/
- https://www.epicgames.com/store/de/product/faster-than-light/home
- https://www.humblebundle.com/store/ftl-faster-than-light
- https://www.gog.com/game/faster_than_light

Buy the game, it's definitely money well spent.

## Get started
Clone the project or download the project to your local computer.

Then use the slipstream mod manager to unpack the ftl.dat into a folder called ftldata in the root folder of this project. The splistream mod manager is included here, or can be downloaded here: https://subsetgames.com/forum/viewtopic.php?t=17102

Select your ftl.dat (when installed via Steam, it will probably be found in "C:\Program Files (x86)\Steam\steamapps\common\FTL Faster Than Light", unless you changed your Steam folder).

In a future version, you will only have to specify the path to your FTL installation, but right now it has to be done manually.
It should also be possible to load the data directly into python, but this is something I would take care of toward the end of this project. A python2 template is found here: https://github.com/bwesterb/ftldat 

**Please DO NOT include the ftl.dat or ftldata folder in any distribution in any way. This is not intended as a standalone game, including these files would be a breach of the FTL copyright!**

The necessary python packages are numpy, pandas and pygame.

After that, run (for now) the file *testPlayerShip.py* either by double clicking it, starting it in the console or anaconda spyder.

## Current status
Since I have little spare time available at the moment, progress will be slow.

The plan for future development is as follows: Enemy ship, weapons, crew, drones, hacking, GUI.
At this point, a single shipfight should be possible (spawn player and enemy ship and fight it out).

Afterwards, the whole gameplay will be implemented.

## Background images
The current two background images are taken from https://www.deviantart.com/sanmonku/gallery/24908419 as I didn't want just a black background.

