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
from swarmgame.utilities import launchGame


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
            \n                                 name (case insensitive, with underscores counting as spaces)\
            \n   -s, --single             : Only play a single level, and quit after completion, win or lose\
            \n   --player-1   <str>       : Name of the player class for player 1 (default = "Human") Valid names\
            \n                                 are "Human", "Neutral", "AiStupid", "AiDumb", "AiBasic", "AiGood"\
            \n                                 (case insensitive)\
            \n   --player-2   <str>       : Name of the player class for player 2 (default = "AiGood") Same valid\
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
