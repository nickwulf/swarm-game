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
    raw_input("Error: Press Enter to continue...")
atexit.register(press_any_key)

pygame.display.set_caption("Swarm")
pygame.mouse.set_visible(False)

aiTest = AiTest(AiDumb(), AiDumb2())
#aiTest.runTest(2,100)

glob.playerList = []
glob.playerList.append(Human((64,64,191)))
glob.playerList.append(Neutral((191,191,191)))
glob.playerList.append(AiDumb2((191,64,64)))
glob.userPlayer = glob.playerList[0]

level = 3
util.makeLevel(level)
gameTimer = 0
pointer = Pointer()

while True:
  
  ####### Handle Input Events ##################################
  util.handleInputEvents()
        
  ####### Perform Game Logic #############################
  
  gameTimer += glob.gameTimeStep
  
  # Determine if mouse is on a planet
  glob.mousedPlanet = None
  for p in glob.planetList:
    if p.isMouseOver():
      glob.mousedPlanet = p
  
  # Handle player inputs
  for p in glob.playerList:
    p.update()
  
  # Handle game action
  for c in glob.caravanList:
    c.update()
  for w in glob.wallList:
    w.update()
  for p in glob.planetList:
    p.update()
  for p in glob.planetList:
    for w in p.weapons:
      w.update()
  for p in glob.particleList:
    p.update()
  for c in glob.caravanList:
    c.update2()

  
  ####### Update Display #################################
  glob.windowSurface.blit(glob.backgroundSurface, (0,0))

  for p in glob.planetList:
    p.drawBack()
  for p in glob.planetList:
    p.draw()
  for p in glob.particleList:
    p.draw()
  for w in glob.wallList:
    w.draw()
  for c in glob.caravanList:
    c.draw()
  util.drawHud()
  util.drawText(int(gameTimer), (50,25))
  util.drawText(int(glob.fpsClock.get_rawtime()), (50,50))
  pointer.draw()
  
  # Draw buffer and wait
  pygame.display.update()
  glob.fpsClock.tick(glob.frameRate)

