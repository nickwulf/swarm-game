import sys, math, random, time, pygame

# Import utilities
import utilities as util

def init():
  global safeExit
  global windowSurface, fpsClock, fontObj, frameRate, backgroundSurface
  global mousePos, mouseLeftButtonClicked, mouseLeftButtonUnclicked, mouseLeftButtonHeld, mouseRightButtonClicked, mouseRightButtonUnclicked, mouseRightButtonHeld
  global spacePressed
  global mousedPlanet
  global playerList, planetList, caravanList
  global gameTimeStep
  
  safeExit = False
  
  windowSurface = pygame.display.set_mode((1200,900))
  fpsClock = pygame.time.Clock()
  fontObj = pygame.font.SysFont("comic sans ms", 32, True, False)
  frameRate = 60
  backgroundSurface = util.createBackground(120,90,10)
  
  mousePos = 0,0
  mouseLeftButtonClicked = False
  mouseLeftButtonUnclicked = False
  mouseLeftButtonHeld = False
  mouseRightButtonClicked = False
  mouseRightButtonUnclicked = False
  mouseRightButtonHeld = False
  
  spacePressed = False
  
  mousedPlanet = None
  
  playerList = []
  planetList = []
  caravanList = []
  
  gameTimeStep = 1.0 / frameRate