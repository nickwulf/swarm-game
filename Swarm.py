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


level = 2
player1 = AiBasic((64,64,191))
player2 = AiGood((191,64,64))

isAiBattle = True
for p in [player1, player2]:
   if isinstance(p, Human):
      isAiBattle = False
      
if isAiBattle:
   aiTest = AiTest(player1, player2)
   aiTest.runTest(level, 10)
else:
   util.runBattle(level, player1, player2)

pygame.quit()
glob.safeExit = True
sys.exit()


# util.makeLevel(level)
# gameTimer = 0
# pointer = Pointer()

# while True:

#    ####### Handle Input Events ##################################
#    util.handleInputEvents()

#    ####### Perform Game Logic #############################

#    gameTimer += glob.gameTimeStep

#    # Determine if mouse is on a planet
#    glob.mousedPlanet = None
#    for p in glob.planetList:
#       if p.isMouseOver():
#          glob.mousedPlanet = p

#    # Handle player inputs
#    for p in glob.playerList:
#       p.update()

#    # Handle game action
#    for c in glob.caravanList:
#       c.update()
#    for w in glob.wallList:
#       w.update()
#    for p in glob.planetList:
#       p.update()
#    for p in glob.planetList:
#       for w in p.weapons:
#          w.update()
#    for p in glob.particleList:
#       p.update()
#    for c in glob.caravanList:
#       c.update2()


#    ####### Update Display #################################
#    glob.windowSurface.blit(glob.backgroundSurface, (0,0))

#    for p in glob.planetList:
#       p.drawBack()
#    for p in glob.planetList:
#       p.draw()
#    for p in glob.particleList:
#       p.draw()
#    for w in glob.wallList:
#       w.draw()
#    for c in glob.caravanList:
#       c.draw()
#    util.drawHud()
#    util.drawText(f'Time: {round(gameTimer, 1)}s', (20,25), align_h='left')
#    util.drawText(f'FPS: {round(glob.fpsClock.get_fps())}', (20,60), align_h='left')
#    pointer.draw()

#    # Draw buffer and wait
#    pygame.display.update()
#    glob.fpsClock.tick(glob.frameRate)
