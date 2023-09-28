import sys, math, random, time, pygame
from pygame.locals import *
import numpy as np

# Import global variables
import globals as glob

# Import user classes
from player import *
from planet import *
from caravan import *

# Displays message msg at the position pos on the screen.
def drawText(msg, pos, font=None):
  if font is None:
    font = glob.fontObj
  text = font.render(str(msg), True, (0,0,0))
  textRect = text.get_rect()
  textRect.center = pos
  glob.windowSurface.blit(text,textRect)
  

def colorFade(color, ratio):
  return color + (ratio*255,)
  
def decide(scoreList, fudge):
  for i in xrange(len(scoreList)):
    scoreList[i] += fudge * random.random()
  return scoreList.index(max(scoreList))
  
def handleInputEvents():
  glob.mouseLeftButtonClicked = False
  glob.mouseLeftButtonUnclicked = False
  glob.mouseRightButtonClicked = False
  glob.mouseRightButtonUnclicked = False
  glob.spacePressed = False
  
  for event in pygame.event.get():
    if event.type == QUIT:
      pygame.quit()
      glob.safeExit = True
      sys.exit()
    elif event.type == MOUSEMOTION:
      glob.mousePos = event.pos
    elif event.type == MOUSEBUTTONDOWN:
      glob.mousePos = event.pos
      if event.button == 1:
        glob.mouseLeftButtonClicked = True
        glob.mouseLeftButtonHeld = True
      elif event.button == 3:
        glob.mouseRightButtonClicked = True
        glob.mouseRightButtonHeld = True
    elif event.type == MOUSEBUTTONUP:
      glob.mousePos = event.pos
      if event.button == 1:
        glob.mouseLeftButtonUnclicked = True
        glob.mouseLeftButtonHeld = False
      elif event.button == 3:
        glob.mouseRightButtonUnclicked = True
        glob.mouseRightButtonHeld = False
    elif event.type == KEYDOWN:
      if event.key == K_SPACE:
        glob.spacePressed = True
  
def drawHUD():
  # Draw base image
  pygame.gfxdraw.box(glob.windowSurface, (1100,0,100,900), (128,128,128))
  pygame.gfxdraw.rectangle(glob.windowSurface, (1119,49,22,802), (0,0,0))
  pygame.gfxdraw.rectangle(glob.windowSurface, (1159,49,22,802), (0,0,0))
  
  # Calculate population and growth bars
  AccumPlayerPops = [0]
  totalPop = 0
  AccumPlayerGrowths = [0]
  totalGrowth = 0
  for player in glob.playerList:
    for p in glob.planetList:
      if p.player is player:
        totalPop += p.population
        totalGrowth += p.growthRate
    for c in glob.caravanList:
      if c.player is player:
        totalPop += c.population
    AccumPlayerPops.append(totalPop)
    AccumPlayerGrowths.append(totalGrowth)
  
  # Draw population bar
  for i in xrange(len(AccumPlayerPops)-1):
    if AccumPlayerPops[i] == AccumPlayerPops[i+1]:
      continue
    barTop = round(800.0*AccumPlayerPops[i]/totalPop)
    barBottom = round(800.0*AccumPlayerPops[i+1]/totalPop)
    pygame.gfxdraw.box(glob.windowSurface, (1120,50+barTop,20,barBottom-barTop), glob.playerList[i].color)
    
  # Draw growth bar
  for i in xrange(len(AccumPlayerGrowths)-1):
    if AccumPlayerGrowths[i] == AccumPlayerGrowths[i+1]:
      continue
    barTop = round(800.0*AccumPlayerGrowths[i]/totalGrowth)
    barBottom = round(800.0*AccumPlayerGrowths[i+1]/totalGrowth)
    pygame.gfxdraw.box(glob.windowSurface, (1160,50+barTop,20,barBottom-barTop), glob.playerList[i].color)
    
def createBackground(width, height, scale):
  for color in xrange(3):
    polyDegree = 4 # 2D polynomial goes up to x^4*y^4
    polyDegree += 1
    polyMatrix = np.zeros((polyDegree,polyDegree), np.float32)
    for a in xrange(polyDegree):
      for b in xrange(polyDegree):
        polyMatrix[a,b] = (random.gauss(0,1))/(1+a*b)
        
    valArray = np.zeros((width,height), np.float32)
    xRes = 2.0/width
    yRes = 2.0/height
    xVal = -1
    yValMatrixList = []
    for x in xrange(width):
      yVal = -1
      xValMatrix = np.power(xVal, np.arange(polyDegree, dtype=np.float32)).reshape(polyDegree,1)
      for y in xrange(height):
        if x == 0:
          yValMatrixList.append(np.power(yVal, np.arange(polyDegree,dtype=np.float32)).reshape(1,polyDegree))
        newPolyMatrix = np.array(polyMatrix)
        newPolyMatrix = np.multiply(newPolyMatrix, xValMatrix)
        newPolyMatrix = np.multiply(newPolyMatrix, yValMatrixList[y])
        valArray[x,y] = np.sum(newPolyMatrix)
        yVal += yRes
      xVal += xRes
    minVal = np.amin(valArray)
    valArray = np.subtract(valArray,minVal)
    scaleFactor = -25.0/np.amax(valArray)
    if color == 0:
      valArrayR = np.multiply(valArray,scaleFactor)
      valArrayR = np.add(valArrayR,255)
    if color == 1:
      valArrayG = np.multiply(valArray,scaleFactor)
      valArrayG = np.add(valArrayG,255)
    if color == 2:
      valArrayB = np.multiply(valArray,scaleFactor)
      valArrayB = np.add(valArrayB,255)
  
  bg = pygame.Surface((width,height))
  bgArray = pygame.PixelArray(bg)
  for x in xrange(width):
    for y in xrange(height):
      bgArray[x,y]=valArrayR[x,y],valArrayG[x,y],valArrayB[x,y]
  
  return pygame.transform.smoothscale(bg, (width*scale, height*scale))

def makeLevel(level):
  glob.planetList = []
  glob.caravanList = []
  if level == 1:
    glob.planetList.append(Planet((100,100), 35, 10, glob.playerList[0]))
    glob.planetList.append(Planet((350,150), 25, 5, glob.playerList[1]))
    glob.planetList.append(Planet((200,300), 50, 5, glob.playerList[1]))
    glob.planetList.append(Planet((1000,800), 35, 10, glob.playerList[2]))
    glob.planetList.append(Planet((750,750), 25, 5, glob.playerList[1]))
    glob.planetList.append(Planet((900,600), 50, 5, glob.playerList[1]))
  elif level == 2:
    glob.planetList.append(Planet((100,450), 25, 20, glob.playerList[0]))
    glob.planetList.append(Planet((250,350), 25, 5, glob.playerList[1]))
    glob.planetList.append(Planet((250,550), 25, 5, glob.playerList[1]))
    glob.planetList.append(Planet((400,250), 35, 10, glob.playerList[1]))
    glob.planetList.append(Planet((400,450), 35, 10, glob.playerList[1]))
    glob.planetList.append(Planet((400,650), 35, 10, glob.playerList[1]))
    glob.planetList.append(Planet((550,150), 50, 15, glob.playerList[1]))
    glob.planetList.append(Planet((550,350), 50, 15, glob.playerList[1]))
    glob.planetList.append(Planet((550,550), 50, 15, glob.playerList[1]))
    glob.planetList.append(Planet((550,750), 50, 15, glob.playerList[1]))
    glob.planetList.append(Planet((700,250), 35, 10, glob.playerList[1]))
    glob.planetList.append(Planet((700,450), 35, 10, glob.playerList[1]))
    glob.planetList.append(Planet((700,650), 35, 10, glob.playerList[1]))
    glob.planetList.append(Planet((850,350), 25, 5, glob.playerList[1]))
    glob.planetList.append(Planet((850,550), 25, 5, glob.playerList[1]))
    glob.planetList.append(Planet((1000,450), 25, 20, glob.playerList[2]))

def countLivePlayers(countNeutral=False):
  aliveList = []
  for p in glob.playerList:
    aliveList.append(False)
  for p in glob.planetList:
    aliveList[glob.playerList.index(p.player)] = True
  for c in glob.caravanList:
    aliveList[glob.playerList.index(c.player)] = True
  if not countNeutral:
    for pId in xrange(len(glob.playerList)):
      if isinstance(glob.playerList[pId], Neutral):
        aliveList[pId] = False
  return aliveList.count(True)
  
def getWinner(countNeutral=False):
  aliveList = []
  for p in glob.playerList:
    aliveList.append(False)
  for p in glob.planetList:
    aliveList[glob.playerList.index(p.player)] = True
  for c in glob.caravanList:
    aliveList[glob.playerList.index(c.player)] = True
  if not countNeutral:
    for pId in xrange(len(glob.playerList)):
      if isinstance(glob.playerList[pId], Neutral):
        aliveList[pId] = False
  if aliveList.count(True) == 1:
    return glob.playerList[aliveList.index(True)]
  else:
    return None

def testAiBattle(ai1, ai2, level):
  glob.playerList = []
  glob.playerList.append(ai1)
  glob.playerList.append(Neutral((191,191,191)))
  glob.playerList.append(ai2)
  makeLevel(level)
  gameTimer = 0
  fpsClock = pygame.time.Clock()
  while getWinner() is None:
    gameTimer += glob.gameTimeStep
    # Handle player inputs
    for p in glob.playerList:
      p.update()
    # Handle game action
    for p in glob.planetList:
      p.update()
    for c in glob.caravanList:
      c.update()
  if getWinner() is ai1:
    return 1, gameTimer
  else:
    return 2, gameTimer

def graphAis(ai1, ai2, level, iterations):
  graphFont = pygame.font.SysFont("arial", 20, True, False)
  graphDim = 500,300
  graphOrigin = 300,600
  maxTime = 20*60
  binWidth = 1.0*maxTime/graphDim[0]
  
  # Set parameters of Gaussian filter
  stdDev = 15
  variance = stdDev**2
  gaussScale = 1.0/stdDev/math.sqrt(2.0*math.pi)
  
  # Gather results
  gameList1 = []
  gameList2 = []
  for i in xrange(iterations):
    results = testAiBattle(ai1, ai2, level)
    if results[0] == 1:
      gameList1.append(results[1])
    else:
      gameList2.append(results[1])
  
  # Calculate graph data
  valueBins1 = []
  valueBins2 = []
  for x in xrange(graphDim[0]+1):
    valueBins1.append(0)
    valueBins2.append(0)
    xVal = 1.0*x/graphDim[0]*maxTime
    for time in gameList1:
      #if math.fabs(time-xVal) <= 30:
      #  valueBins1[x] += 1.0/iterations
      valueBins1[x] += 60.0/iterations*gaussScale*math.exp((-(xVal-time)**2.0)/(2.0*variance))
    for time in gameList2:
      #if math.fabs(time-xVal) <= 30:
      #  valueBins1[x] += 1.0/iterations
      valueBins2[x] += 60.0/iterations*gaussScale*math.exp((-(xVal-time)**2.0)/(2.0*variance))
  print (sum(valueBins1) + sum(valueBins2)) * maxTime/graphDim[0]/60
  
  # Find maximum y dimension
  maxWins = int(math.ceil(4*max(max(valueBins1),max(valueBins2))))/4.0
  
  # Adjust graph data vertically to match graphDim
  for x in xrange(len(valueBins1)):
    valueBins1[x] = 1.0*valueBins1[x]/maxWins*graphDim[1]
    valueBins2[x] = 1.0*valueBins2[x]/maxWins*graphDim[1]
  
  # Clear draw screen
  glob.windowSurface.fill((255,255,255))
  
  # Draw the data
  for x in xrange(graphDim[0]):
    pygame.draw.aaline(glob.windowSurface, (0,0,255), (graphOrigin[0]+x, graphOrigin[1]-valueBins1[x]), (graphOrigin[0]+x+1, graphOrigin[1]-valueBins1[x+1]))
    pygame.draw.aaline(glob.windowSurface, (255,0,0), (graphOrigin[0]+x, graphOrigin[1]-valueBins2[x]), (graphOrigin[0]+x+1, graphOrigin[1]-valueBins2[x+1]))
    
  # Draw the base graph
  pygame.draw.line(glob.windowSurface, (0,0,0), graphOrigin, (graphOrigin[0], graphOrigin[1]-graphDim[1]))
  pygame.draw.line(glob.windowSurface, (0,0,0), graphOrigin, (graphOrigin[0]+graphDim[0], graphOrigin[1]))
  for x in xrange(maxTime/120 + 1):
    offset = x*120.0/maxTime*graphDim[0]
    offset = int(round(offset))
    pygame.draw.line(glob.windowSurface, (0,0,0), (graphOrigin[0]+offset, graphOrigin[1]), (graphOrigin[0]+offset, graphOrigin[1]+5))
    drawText(x*2, (graphOrigin[0]+offset, graphOrigin[1]+15), graphFont)
  for y in xrange(6):
    offset = y/5.0*graphDim[1]
    offset = int(round(offset))
    pygame.draw.line(glob.windowSurface, (0,0,0), (graphOrigin[0], graphOrigin[1]-offset), (graphOrigin[0]-5, graphOrigin[1]-offset))
    drawText(round(y/5.0*maxWins,2), (graphOrigin[0]-25, graphOrigin[1]-offset), graphFont)
  
  # Flip screen and wait
  pygame.display.update()
  raw_input("Press Enter to continue...")


