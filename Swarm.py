import os, sys, math, random, time, pygame
from pygame.locals import *
import pygame.gfxdraw
import atexit

# Import global variables and utilities
import globals as glob
import utilities as util

# Import user classes
from player import *
from planet import *
from caravan import *


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

#util.graphAis(AiTest(), AiDumb(), 2, 1)

glob.playerList = []
glob.playerList.append(Human((64,64,191)))
glob.playerList.append(Neutral((191,191,191)))
glob.playerList.append(AiStupid((191,64,64)))

level = 2
util.makeLevel(level)
gameTimer = 0

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
  for p in glob.planetList:
    p.update()
  for c in glob.caravanList:
    c.update()
  
  ####### Update Display #################################
  glob.windowSurface.blit(glob.backgroundSurface, (0,0))
  #glob.windowSurface.fill((232,232,232))

  for p in glob.planetList:
    p.drawBack()
  for p in glob.planetList:
    p.draw()
  for c in glob.caravanList:
    c.draw()
  util.drawHUD()
  util.drawText(int(gameTimer), (500,850))
  
  # Draw buffer and wait
  pygame.display.update()
  glob.fpsClock.tick_busy_loop(glob.frameRate)

