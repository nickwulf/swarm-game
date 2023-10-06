import sys, math, random, time, pygame

# Import utilities
from . import utilities as util


safeExit = None
windowSurface = winPosRaw = winPos = fpsClock = fontObj = frameRate = backgroundSurface = None
mouseDrawPos = mousePos = mouseLeftButtonClicked = mouseLeftButtonUnclicked = mouseLeftButtonHeld = mouseRightButtonClicked = mouseRightButtonUnclicked = mouseRightButtonHeld = None
spacePressed = qPressed = ePressed = shiftHeld = aHeld = dHeld = wHeld = sHeld = None
mousedPlanet = None
playerList = planetList = caravanList = particleList = wallList = None
speedList = speedListInd = gameTimeStep = userToGameInteractionDisabled = None
userPlayer = None

def init():
   global safeExit
   global windowSurface, winPosRaw, winPos, fpsClock, fontObj, frameRate, backgroundSurface
   global mouseDrawPos, mousePos, mouseLeftButtonClicked, mouseLeftButtonUnclicked, mouseLeftButtonHeld, mouseRightButtonClicked, mouseRightButtonUnclicked, mouseRightButtonHeld
   global spacePressed, qPressed, ePressed, shiftHeld, aHeld, dHeld, wHeld, sHeld
   global mousedPlanet
   global playerList, planetList, caravanList, particleList, wallList
   global speedList, speedListInd, gameTimeStep, userToGameInteractionDisabled
   global userPlayer
   
   safeExit = False

   windowSurface = pygame.display.set_mode((1600,1000))
   winPosRaw = 0,0
   winPos = int(winPosRaw[0]), int(winPosRaw[1])
   fpsClock = pygame.time.Clock()
   fontObj = pygame.font.SysFont("comic sans ms", 32, True, False)
   frameRate = 60
   backScale = 10
   backWidth = math.ceil(windowSurface.get_width() / backScale)
   backHeight = math.ceil(windowSurface.get_height() / backScale)
   backgroundSurface = util.createBackground(backWidth, backHeight, backScale)

   mouseDrawPos = 0,0
   mousePos = mouseDrawPos[0]+winPos[0], mouseDrawPos[1]+winPos[1]
   mouseLeftButtonClicked = False
   mouseLeftButtonUnclicked = False
   mouseLeftButtonHeld = False
   mouseRightButtonClicked = False
   mouseRightButtonUnclicked = False
   mouseRightButtonHeld = False

   spacePressed = False
   qPressed = False
   ePressed = False
   shiftHeld = False
   aHeld = False
   dHeld = False
   wHeld = False
   sHeld = False

   mousedPlanet = None

   playerList = []
   planetList = []
   caravanList = []
   particleList = []
   wallList = []

   speedList = [1/30, 1/10, 1/3, 1, 3, 10, 30]
   speedListInd = 3
   gameTimeStep = speedList[speedListInd] / frameRate
   
   userToGameInteractionDisabled = False

   userPlayer = None
