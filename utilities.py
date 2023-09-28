import sys, math, random, time, pygame
from pygame.locals import *
import numpy as np

# Import global variables
import globals as glob

# Import user classes
from player import *
from planet import *
from caravan import *
from wall import *

# Displays message msg at the position pos on the screen.
def drawText(msg, pos, font=None, surf=None, color=(0,0,0)):
  if font is None:
    font = glob.fontObj
  if surf is None:
    surf = glob.windowSurface
  text = font.render(str(msg), True, color)
  textRect = text.get_rect()
  textRect.center = pos
  surf.blit(text,textRect)

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
      if event.key == K_LSHIFT:
        glob.shiftHeld = True
    elif event.type == KEYUP:
      if event.key == K_LSHIFT:
        glob.shiftHeld = False
  
def drawHud():
  ########## Draw Select Box ############################
  if isinstance(glob.userPlayer, Human):
    if glob.userPlayer.selectRect is not None:
      if glob.userPlayer.selectRect.width > 0 and glob.userPlayer.selectRect.height > 0:
        pygame.gfxdraw.box(glob.windowSurface, glob.userPlayer.selectRect, colorFade(glob.userPlayer.color,0.1))
        pygame.gfxdraw.rectangle(glob.windowSurface, glob.userPlayer.selectRect.inflate(-2,2), (64,64,64,128))
        pygame.gfxdraw.rectangle(glob.windowSurface, glob.userPlayer.selectRect.inflate(2,-2), (64,64,64,128))
        pygame.gfxdraw.rectangle(glob.windowSurface, glob.userPlayer.selectRect, (64,64,64,255))
        
  ########## Draw Side Display ##########################
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
  glob.particleList = []
  glob.wallList = []
  if level == 1:
    glob.planetList.append(Planet((100,100), 35.36, 10, glob.playerList[0]))
    glob.planetList.append(Planet((350,150), 25, 5, glob.playerList[1]))
    glob.planetList.append(Planet((200,300), 50, 5, glob.playerList[1]))
    glob.planetList.append(Planet((1000,800), 35.36, 10, glob.playerList[2]))
    glob.planetList.append(Planet((750,750), 25, 5, glob.playerList[1]))
    glob.planetList.append(Planet((900,600), 50, 5, glob.playerList[1]))
  elif level == 2:
    glob.planetList.append(Planet((100,450), 25, 10, glob.playerList[0]))
    glob.planetList.append(Planet((250,350), 25, 5, glob.playerList[1]))
    glob.planetList.append(Planet((250,550), 25, 5, glob.playerList[1]))
    glob.planetList.append(Planet((400,250), 35.36, 10, glob.playerList[1]))
    glob.planetList.append(Planet((400,450), 35.36, 10, glob.playerList[1]))
    glob.planetList.append(Planet((400,650), 35.36, 10, glob.playerList[1]))
    glob.planetList.append(Planet((550,150), 50, 15, glob.playerList[1]))
    glob.planetList.append(Planet((550,350), 50, 15, glob.playerList[1]))
    glob.planetList.append(Planet((550,550), 50, 15, glob.playerList[1]))
    glob.planetList.append(Planet((550,750), 50, 15, glob.playerList[1]))
    glob.planetList.append(Planet((700,250), 35.36, 10, glob.playerList[1]))
    glob.planetList.append(Planet((700,450), 35.36, 10, glob.playerList[1]))
    glob.planetList.append(Planet((700,650), 35.36, 10, glob.playerList[1]))
    glob.planetList.append(Planet((850,350), 25, 5, glob.playerList[1]))
    glob.planetList.append(Planet((850,550), 25, 5, glob.playerList[1]))
    glob.planetList.append(Planet((1000,450), 25, 10, glob.playerList[2]))
    glob.planetList[7].addLaser(1, 250, 50)
    glob.planetList[8].addLaser(1, 250, 50)
  elif level == 3:
    glob.planetList.append(Planet((100,120), 40, 15, glob.playerList[1]))
    glob.planetList.append(Planet((100,240), 35, 10, glob.playerList[1]))
    glob.planetList.append(Planet((100,350), 30, 7, glob.playerList[1]))
    glob.planetList.append(Planet((100,450), 25, 5, glob.playerList[0]))
    glob.planetList.append(Planet((100,550), 30, 7, glob.playerList[1]))
    glob.planetList.append(Planet((100,660), 35, 10, glob.playerList[1]))
    glob.planetList.append(Planet((100,780), 40, 15, glob.playerList[1]))
    glob.planetList.append(Planet((1000,450), 75, 5, glob.playerList[2]))
    glob.planetList.append(Planet((1000,200), 35, 150, glob.playerList[1]))
    glob.planetList.append(Planet((1000,700), 35, 150, glob.playerList[1]))
    glob.planetList[8].addLaser(5, 800, 100)
    glob.planetList[9].addLaser(5, 800, 100)
    glob.wallList.append(Wall((400,200), (600,700), glob.playerList[1], 100))
  
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
    
def drawPie(surface, centerPos, r, start, end, color):
  # Warning: Can't draw black pies
  if start >= end:
    return
  maskSurface = pygame.Surface((2*r+1,2*r+1))
  maskSurface.set_colorkey((255,255,255))
  pygame.gfxdraw.filled_circle(maskSurface, r, r, int(r), (255,255,255))
  tempSurface = pygame.Surface((2*r+1,2*r+1))
  tempSurface.set_colorkey((0,0,0))
  if end-start < 360:
    tempSurface.fill((0,0,0))
    corners = [(2*r+2,0), (0,0), (0,2*r+2), (2*r+2,2*r+2), (2*r+2,0), (0,0), (0,2*r+2), (2*r+2,2*r+2)]
    start = start % 360
    end = end % 360
    if start > end:
      end += 360
    startIndex = int((start+45)/90)
    endIndex = int((end+45)/90)
    startPos = 1.5*r*math.cos(math.radians(start))+r, -1.5*r*math.sin(math.radians(start))+r
    endPos = 1.5*r*math.cos(math.radians(end))+r, -1.5*r*math.sin(math.radians(end))+r
    points = [(r,r), startPos] + corners[startIndex:endIndex] + [endPos]
    pygame.gfxdraw.filled_polygon(tempSurface, points, color)
  else:
    tempSurface.fill(color)
  tempSurface.blit(maskSurface, (0,0))
  surface.blit(tempSurface, (centerPos[0]-r, centerPos[1]-r))

def combineColors(color1,color2,strengthOf1):
  if strengthOf1 <= 0:
    return color1
  elif strengthOf1 >= 1:
    return color2
  else:
    strengthOf2 = 1 - strengthOf1
    return int(color1[0]*strengthOf1+color2[0]*strengthOf2),int(color1[1]*strengthOf1+color2[1]*strengthOf2),int(color1[2]*strengthOf1+color2[2]*strengthOf2)
    
def changeLuminosity(color, lum):
  colorObj = pygame.Color(color[0],color[1],color[2],255)
  hslaValues = colorObj.hsla
  hslaValues = hslaValues[0], hslaValues[1], lum, hslaValues[3]
  colorObj.hsla = hslaValues
  return colorObj.r, colorObj.g, colorObj.b
  
def getPoissonCount(expectedVal):
  # Donald Knuth algorithm
  L = math.exp(-expectedVal)
  k = 0
  p = 1.0
  while True:
    k += 1
    p *= random.random()
    if p <= L:
      return k-1
      
def findIntersection(p,a,q,b): # p and a are endpoints of line1, q and b are endpoints of line 2
  # From http://stackoverflow.com/questions/563198/how-do-you-detect-where-two-line-segments-intersect
  r = a[0]-p[0], a[1]-p[1]  # r = vector from p to a
  s = b[0]-q[0], b[1]-q[1]  # s = vector from q to b
  denominator = r[0]*s[1] - r[1]*s[0]  # This is equivalent to (r x s)
  numeratorT = (q[0]-p[0])*s[1] - (q[1]-p[1])*s[0]  # This is equivalent to (q - p) x s
  numeratorU = (q[0]-p[0])*r[1] - (q[1]-p[1])*r[0]  # This is equivalent to (q - p) x r
  if denominator != 0:  # True if the lines are not parallel
    t = 1.0*numeratorT/denominator
    u = 1.0*numeratorU/denominator
    if 0 <= u and u <= 1 and 0 <= t and t<= 1:  # True if the intersection occures on the line segments
      return q[0]+u*s[0], q[1]+u*s[1]  # This is equivalent to q + us
    else:
      return None
  else:
    if r[0] == 0 and r[1] == 0:  # True if line1 is a point, which will always produce 0 for num and denom
      if s[0] == 0 and s[1] == 0:  # True if line2 is also a point
        if p[0] == q[0] and p[1] == q[1]:  # True if line1 and line2 are the same point
          return p
        else:
          return None
      else:  # If line1 is a point, we need to fix numerator for collinearity test
        numeratorU = numeratorT
    if numeratorU != 0:  # True if the lines are not collinear
      return None
    else:
      if r[0] == 0:  # True if both lines are completely vertical
        if (p[1]-q[1])*(p[1]-b[1]) <= 0:  # True if p is between q and b
          return p
        elif (a[1]-q[1])*(a[1]-b[1]) <= 0:  # True if a is between q and b
          return a
        elif (q[1]-p[1])*(q[1]-a[1]) <= 0:  # True if q (and b) is between p and a
          return q
        else:  # True if lines are collinear but not overlapping
          return None
      else:
        if (p[0]-q[0])*(p[0]-b[0]) <= 0:  # True if p is between q and b
          return p
        elif (a[0]-q[0])*(a[0]-b[0]) <= 0:  # True if a is between q and b
          return a
        elif (q[0]-p[0])*(q[0]-a[0]) <= 0:  # True if q (and b) is between p and a
          return q
        else:  # True if lines are collinear but not overlapping
          return None
    
      
  
    