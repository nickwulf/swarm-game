==========
Swarm-Game
==========

Swarm-Game is a game about swarming your enemies, taking over other planets, and expanding your empire.

It is still in development mode, so it's not a fully playable game. Currently you can select what Ais you want to fight, choose what level you want to start at, and then launch a game window to start playing.

How To Play
-----------
The goal of the game is to take over planets until you're the only one left. Every planet under your control generates fighters. You can send these fighters to enemy planets to fight and take them over, or send to your own planets for reinforcement. When starting a new level, you and your enemy will have small armies with only 1 or 2 planets. There will also be many other neutral planets just waiting to be conquered. Expand your empire rapidly by prioritizing larger, closer planets with fewer supporting fighters. The more you grow, the faster you can conquer new planets and grow even faster. But be careful, because your enemies will be doing the same!

The bigger a planet is, the more fighters it can support and the more quickly it produces them. The growing bars around a planet indicate how full it is. At 75% capacity, the bars start pulsing, indicating that fighter production is halved because the planet is so full. At 100%, production stops. If reinforcements arrive to push a planet beyond its capacity (indicated by the new white bar on top), they will quickly die off due to starvation.

When you tell a planet to send its fighters, half of the fighters will be sent, leaving the other half to stay behind and defend the planet. You can send multiple groups rapidly to send almost every fighter. Be careful though, as this may leave the planet undefended against a counterattack.

Sometimes planets will have lasers, which will destroy fighters if they get the chance. Lasers on neutral planets will target all fighters, but if you conquer the planet, then its lasers are your and will only attack your enemies! Lasers vary in their power, range, and speed, so you'll need different strategies to either avoid or attack them.

You'll also encounter walls out in space (somehow a thing), that destroy any fighters that cross their paths. The walls have a certain health though, so if you pull a Zap Brannigan and send enough of your fighters to their doom, you'll eventually defeat the wall. Whether that's an acceptable cost or not is up to you. You can tell how close you are to defeating a wall by observing how infrequent and weak its lighting arcs are.

Controls
________
A, W, S, D  -> Pan the view around
Q           -> Slow down time
E           -> Speed up time
Left Mouse  -> Click to select/deselect a planet. Drag to select a group of planets
Right Mouse -> Click to send fighters from the selected planet/s to another planet
Left Shift  -> Hold to keep the selected planets even while selecting or deselecting anther planet. Useful to grow or selectively shrink your selected group

Quick Start
-----------
The quickest way to get started is to download the GitHub project onto your machine, unzip, and go to the top-level directory. From here, launch the game using the command "python main.py". You can use other command line options to change certain settings such as switching players between human or other AIs or changing the starting level. Run the command "python main.py -h" to see the full list of options in the help menu.

Dependencies
____________
You'll also need to install these other python packages before you can run the game:
- pygame >= 2.4
- numpy >= 1.21.6

Python Install
--------------
This code was structured as a Python package with installation scripts so that it could be easily installed and integrated into your other Python projects for easier experimentation.

Download
________
1. Download directly from GitHub at https://github.com/nickwulf/swarm-game and unzip where you want, or
2. If you have git installed on Linux, run the command "git clone https://github.com/nickwulf/swarm-game.git <file_location>" to clone the project to you local area.

Build
_____
Build the Python package by navigating to the top-level project directory, and run the command "python setup.py sdist"

Install
_______
Find the new Python package in the new "dist" directory, and install it into your Python environment by running the command "python -m pip install ./dist/<dist_file>.tar.gz".

Integrate
_________
Integrate the package into any of your other Python projects the same way as with any other package. For example, import the Human player class with the line "from swarmgame.player import Human". Alternatively, you can straight up run the game by importing the launchGame function from the utilities module and executing the function as so: "from swarmgame.utilities import launchGame; launchGame()"
