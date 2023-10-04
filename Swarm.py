import os, sys, math, random, time, pygame
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


####### Initialization ###################################

os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (300,100)

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



level = util.Level.TUTORIAL
singleLevel = False
player1 = Human((64,64,191))
player2 = AiGood((191,64,64))

isAiBattle = True
for p in [player1, player2]:
   if isinstance(p, Human):
      isAiBattle = False

while not singleLevel:
   if level not in iter(util.Level):
      print('End of Game')
      pygame.quit()
      glob.safeExit = True
      sys.exit()
      
   result = {'winner':None, 'time':0}
   if isAiBattle:
      aiTest = AiTest(player1, player2)
      aiTest.runTest(level, 10)
   else:
      result = util.runBattle(level, player1, player2)

   if isAiBattle or isinstance(result['winner'], Human):
      level += 1

pygame.quit()
glob.safeExit = True
sys.exit()



