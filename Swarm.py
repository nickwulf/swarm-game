import os
import sys
import math
import random
import time
import pygame
import getopt
from pygame.locals import *
import pygame.gfxdraw
import atexit

# Import global variables and utilities
import globals as glob
import utilities as util

# Import user classes
from aiTest import *
from player import *
from planet import *
from caravan import *
from particle import *
from pointer import *
from wall import *


def launchGame(player1='Human', player2='AiGood', level=1, doSingleLevel=False):
    # Launches a game window and plays through the levels

    # You can specify if each player is Human or an AI, and what level of AI. Levels are set up for player 1 to be human, but either player or neither can actually be human (2 human play is not supported). If neither player is human, both AIs play against each other 100 times using over 100X time acceleration. Once a human player wins (or AIs are done with last battle), the next level starts until all levels are completed. If the human loses, the current level resets. If doSingleLevel is True, the game ends at the end of the level, win or lose.

    # Inputs ################################################
    # player1, player2  ->  object, str
    # Can be actual objects of player classes from player.py or case-insensitive text descriptions of those classes (e.g. "human" or "AIBASIC")
    # level             ->  int, object, str
    # Determines the intial level to start play at. Each level has a name and number, which are defined by the enumerated Level class (found in utilities.py). You can specify a level with an object of saide enumerated class, its associated integer, or its associated name (case-insensitive, underscores equal to spaces)
    # doSingleLevel     -> boolean
    # If true, game closes after completion of initial level. Continues to subsequent levels otherwise

    ####### Initialization ###################################

    os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (300, 100)

    random.seed()
    pygame.init()
    glob.init()

    # Allows for debugging when error causes crash
    def press_any_key():
        if not glob.safeExit:
            input("Error: Press Enter to continue...")
    atexit.register(press_any_key)

    pygame.display.set_caption("Swarm")
    pygame.mouse.set_visible(False)

    if isinstance(level, str):
        if level.isnumeric():
            level = int(level)
        else:
            for lev in util.Level:
                if lev.name.lower() == level.lower().replace(' ', '_'):
                    level = lev

    players = [player1, player2]
    playerDefaultColors = [(64, 64, 191), (191, 64, 64)]
    playerClassMap = {'human': Human, 'aistupid': AiStupid, 'aidumb': AiDumb,
                      'aibasic': AiBasic, 'aigood': AiGood, 'neutral': Neutral}
    for p in range(len(players)):
        if isinstance(players[p], str):
            playerClass = playerClassMap[players[p].lower()]
            players[p] = playerClass(playerDefaultColors[p])

    isAiBattle = True
    for p in players:
        if isinstance(p, Human):
            isAiBattle = False

    while True:
        if level not in iter(util.Level):
            print('End of Game')
            pygame.quit()
            glob.safeExit = True
            sys.exit()

        result = {'winner': None, 'time': 0}
        if isAiBattle:
            aiTest = AiTest(*players)
            aiTest.runTest(level, 100)
        else:
            result = util.runBattle(level, *players)

        if isAiBattle or isinstance(result['winner'], Human):
            level += 1

        if doSingleLevel:
            break

    pygame.quit()
    glob.safeExit = True
    sys.exit()


def main(argv):
    options = {}

    try:
        opts, args = getopt.getopt(
            argv, 'hl:s', ['help', 'level=', 'single', 'player-1=', 'player-2='])
    except getopt.GetoptError:
        raise SystemExit(
            'Error: Incorrect option/s. Run with -h option for help')

    for opt, arg in opts:
        if opt in ('-h', '--help'):
            print(f'\
            \nOptions List:\
            \n   -h, --help               : Show this help screen\
            \n   -l, --level   <int/str>  : Select the level (default = 1). Can be the level number or the level\
            \n                                name (case insensitive, with underscores counting as spaces)\
            \n   -s, --single             : Only play a single level, and quit after completion, win or lose\
            \n   --player-1    <str>      : Name of the player class for player 1 (default = "Human") Valid names\
            \n                                 are "Human", "Neutral", "AiStupid", "AiDumb", "AiBasic", "AiGood"\
            \n                                 (case insensitive)\
            \n   --player-2    <str>      : Name of the player class for player 2 (default = "AiGood") Same valid\
            \n                                 names as with player 1\
            \n\
         ')
            exit()
        elif opt in ('-l', '--level'):
            options['level'] = arg
        elif opt in ('-s', '--single'):
            options['doSingleLevel'] = True
        elif opt == '--player-1':
            options['player1'] = arg
        elif opt == '--player-2':
            options['player2'] = arg
    launchGame(**options)


if __name__ == "__main__":
    main(sys.argv[1:])
