import sys, math, random, time, pygame
import enum
from pygame.locals import *
import numpy as np
import atexit

# Import global variables
from . import globals as glob

# Import user classes
from .aiTest import *
from .player import *
from .planet import *
from .caravan import *
from .pointer import *
from .wall import *



def launchGame(player1='Human', player2='AiGood', level=1, doSingleLevel=False):
   # Launches a game window and plays through the levels

   # You can specify if each player is Human or an AI, and what level of AI. Levels are set up for player 1 to be human, but either player or neither can actually be human (2 human play is not supported). If neither player is human, both AIs play against each other 100 times using over 100X time acceleration. Once a human player wins (or AIs are done with last battle), the next level starts until all levels are completed. If the human loses, the current level resets. If doSingleLevel is True, the game ends at the end of the level, win or lose.

   # Inputs ################################################
   # player1, player2  ->  object, str
   # Can be actual objects of player classes from player.py or case-insensitive text descriptions of those classes (e.g. "human" or "AIBASIC")
   # level          ->  int, object, str
   # Determines the intial level to start play at. Each level has a name and number, which are defined by the enumerated Level class (found in utilities.py). You can specify a level with an object of saide enumerated class, its associated integer, or its associated name (case-insensitive, underscores equal to spaces)
   # doSingleLevel    -> boolean
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


# Displays message msg at the position pos on the screen.
def drawText(msg, pos, font=None, surf=None, color=(0,0,0), align_h='center'):
   if font is None:
      font = glob.fontObj
   if surf is None:
      surf = glob.windowSurface
   text = font.render(str(msg), True, color)
   textRect = text.get_rect()
   textRect.center = pos
   if align_h == 'left': textRect.left = pos[0]
   surf.blit(text,textRect)

def colorFade(color, ratio):
   return color + (ratio*255,)

def decide(scoreList, fudge):
   for i in range(len(scoreList)):
      scoreList[i] += fudge * random.random()
   return scoreList.index(max(scoreList))

def handleInputEvents():
   glob.mouseLeftButtonClicked = False
   glob.mouseLeftButtonUnclicked = False
   glob.mouseRightButtonClicked = False
   glob.mouseRightButtonUnclicked = False
   glob.spacePressed = False
   glob.qPressed = False
   glob.ePressed = False

   for event in pygame.event.get():
      if event.type == QUIT:
         pygame.quit()
         glob.safeExit = True
         sys.exit()
      elif event.type == MOUSEMOTION:
         glob.mouseDrawPos = event.pos
      elif event.type == MOUSEBUTTONDOWN:
         glob.mouseDrawPos = event.pos
         if event.button == 1:
            glob.mouseLeftButtonClicked = True
            glob.mouseLeftButtonHeld = True
         elif event.button == 3:
            glob.mouseRightButtonClicked = True
            glob.mouseRightButtonHeld = True
      elif event.type == MOUSEBUTTONUP:
         glob.mouseDrawPos = event.pos
         if event.button == 1:
            glob.mouseLeftButtonUnclicked = True
            glob.mouseLeftButtonHeld = False
         elif event.button == 3:
            glob.mouseRightButtonUnclicked = True
            glob.mouseRightButtonHeld = False
      elif event.type == KEYDOWN:
         if event.key == K_SPACE:
            glob.spacePressed = True
         if event.key == K_q:
            glob.qPressed = True
         if event.key == K_e:
            glob.ePressed = True
         if event.key == K_LSHIFT:
            glob.shiftHeld = True
         if event.key == K_a:
            glob.aHeld = True
         if event.key == K_d:
            glob.dHeld = True
         if event.key == K_w:
            glob.wHeld = True
         if event.key == K_s:
            glob.sHeld = True
      elif event.type == KEYUP:
         if event.key == K_LSHIFT:
            glob.shiftHeld = False
         if event.key == K_a:
            glob.aHeld = False
         if event.key == K_d:
            glob.dHeld = False
         if event.key == K_w:
            glob.wHeld = False
         if event.key == K_s:
            glob.sHeld = False

   glob.mousePos = glob.mouseDrawPos[0]+glob.winPos[0], glob.mouseDrawPos[1]+glob.winPos[1]

def drawHud():
   ########## Draw Select Box ############################
   if isinstance(glob.userPlayer, Human):
      if glob.userPlayer.selectRect is not None:
         if glob.userPlayer.selectRect.width > 0 and glob.userPlayer.selectRect.height > 0:
            drawRect = glob.userPlayer.selectRect.move(-glob.winPos[0], -glob.winPos[1])
            pygame.gfxdraw.box(glob.windowSurface, drawRect, colorFade(glob.userPlayer.color,0.1))
            pygame.gfxdraw.rectangle(glob.windowSurface, drawRect.inflate(-2,2), (64,64,64,128))
            pygame.gfxdraw.rectangle(glob.windowSurface, drawRect.inflate(2,-2), (64,64,64,128))
            pygame.gfxdraw.rectangle(glob.windowSurface, drawRect, (64,64,64,255))

   ########## Draw Side Display ##########################
   # Draw base image
   winDims = glob.windowSurface.get_size();
   barDims = 20, winDims[1] - 100
   barOffset1 = winDims[0] - 80, 50
   barOffset2 = winDims[0] - 40, 50
   pygame.gfxdraw.box(glob.windowSurface, (winDims[0]-100,0,100,winDims[1]), (128,128,128))
   pygame.gfxdraw.rectangle(glob.windowSurface, (barOffset1[0]-1, barOffset1[1]-1, barDims[0]+2, barDims[1]+2), (0,0,0))
   pygame.gfxdraw.rectangle(glob.windowSurface, (barOffset2[0]-1, barOffset2[1]-1, barDims[0]+2, barDims[1]+2), (0,0,0))

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
   for i in range(len(AccumPlayerPops)-1):
      if AccumPlayerPops[i] == AccumPlayerPops[i+1]:
         continue
      barTop = round(barDims[1]*AccumPlayerPops[i]/totalPop)
      barBottom = round(barDims[1]*AccumPlayerPops[i+1]/totalPop)
      pygame.gfxdraw.box(glob.windowSurface, (barOffset1[0], barOffset1[1]+barTop, barDims[0], barBottom-barTop), glob.playerList[i].color)

   # Draw growth bar
   for i in range(len(AccumPlayerGrowths)-1):
      if AccumPlayerGrowths[i] == AccumPlayerGrowths[i+1]:
         continue
      barTop = round(barDims[1]*AccumPlayerGrowths[i]/totalGrowth)
      barBottom = round(barDims[1]*AccumPlayerGrowths[i+1]/totalGrowth)
      pygame.gfxdraw.box(glob.windowSurface, (barOffset2[0], barOffset2[1]+barTop, barDims[0], barBottom-barTop), glob.playerList[i].color)

def createBackground(width, height, scale):
   for color in range(3):
      polyDegree = 4 # 2D polynomial goes up to x^4*y^4
      polyDegree += 1
      polyMatrix = np.zeros((polyDegree,polyDegree), np.float32)
      for a in range(polyDegree):
         for b in range(polyDegree):
            polyMatrix[a,b] = (random.gauss(0,1))/(1+a*b)

      valArray = np.zeros((width,height), np.float32)
      xRes = 2.0/width
      yRes = 2.0/height
      xVal = -1
      yValMatrixList = []
      for x in range(width):
         yVal = -1
         xValMatrix = np.power(xVal, np.arange(polyDegree, dtype=np.float32)).reshape(polyDegree,1)
         for y in range(height):
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
   for x in range(width):
      for y in range(height):
         bgArray[x,y]=valArrayR[x,y],valArrayG[x,y],valArrayB[x,y]

   return pygame.transform.smoothscale(bg, (width*scale, height*scale))

class Level(enum.IntEnum):
   TUTORIAL = enum.auto()
   FAR_SIDE = enum.auto()
   KING_OF_THE_HILL = enum.auto()
   MAZE = enum.auto()
   BORROWED_TIME = enum.auto()
   PROTECTED = enum.auto()
   DOUBLE_DUTCH = enum.auto()
   ISLAND_HOPPING = enum.auto()

def makeLevel(level, player1, player2, playerN):
   glob.planetList = []
   glob.caravanList = []
   glob.particleList = []
   glob.wallList = []
   if level == Level.TUTORIAL:
      glob.planetList.append(Planet((0,0), 50, 10, player1))
      glob.planetList.append(Planet((30,100), 30, 5, player1))
      glob.planetList.append(Planet((100,50), 30, 5, playerN))
      glob.planetList.append(Planet((800,50), 30, 10, player2))
   elif level == Level.FAR_SIDE:
      glob.planetList.append(Planet((100,100), 35.36, 10, player1))
      glob.planetList.append(Planet((350,150), 30, 5, playerN))
      glob.planetList.append(Planet((200,300), 50, 5, playerN))
      glob.planetList.append(Planet((1000,800), 35.36, 10, player2))
      glob.planetList.append(Planet((750,750), 25, 5, playerN))
      glob.planetList.append(Planet((900,600), 50, 5, playerN))
   elif level == Level.MAZE:
      glob.planetList.append(Planet((0,-400), 30, 10, playerN))
      glob.planetList.append(Planet((0,-200), 30, 10, playerN))
      glob.planetList.append(Planet((0,0), 30, 10, playerN))
      glob.planetList.append(Planet((0,200), 30, 10, playerN))
      glob.planetList.append(Planet((0,400), 30, 10, player1))
      glob.planetList.append(Planet((200,-400), 30, 10, playerN))
      glob.planetList.append(Planet((200,-200), 30, 10, playerN))
      glob.planetList.append(Planet((200,0), 30, 10, playerN))
      glob.planetList.append(Planet((200,200), 30, 10, playerN))
      glob.planetList.append(Planet((200,400), 30, 10, playerN))
      glob.planetList.append(Planet((400,-400), 30, 10, playerN))
      glob.planetList.append(Planet((400,-200), 30, 10, playerN))
      glob.planetList.append(Planet((400,0), 30, 10, playerN))
      glob.planetList.append(Planet((400,200), 30, 10, playerN))
      glob.planetList.append(Planet((400,400), 30, 10, playerN))
      glob.planetList.append(Planet((600,-400), 30, 10, playerN))
      glob.planetList.append(Planet((600,-200), 30, 10, playerN))
      glob.planetList.append(Planet((600,0), 30, 10, playerN))
      glob.planetList.append(Planet((600,200), 30, 10, playerN))
      glob.planetList.append(Planet((600,400), 30, 10, playerN))
      glob.planetList.append(Planet((800,-400), 30, 10, playerN))
      glob.planetList.append(Planet((800,-200), 30, 10, playerN))
      glob.planetList.append(Planet((800,0), 30, 10, playerN))
      glob.planetList.append(Planet((800,200), 30, 10, playerN))
      glob.planetList.append(Planet((800,400), 30, 10, playerN))
      glob.planetList.append(Planet((1000,-400), 30, 10, playerN))
      glob.planetList.append(Planet((1000,-200), 30, 10, playerN))
      glob.planetList.append(Planet((1000,0), 30, 10, playerN))
      glob.planetList.append(Planet((1000,200), 30, 10, playerN))
      glob.planetList.append(Planet((1000,400), 30, 10, playerN))
      glob.planetList.append(Planet((1200,-400), 30, 10, player2))
      glob.planetList.append(Planet((1200,-200), 30, 10, playerN))
      glob.planetList.append(Planet((1200,0), 30, 10, playerN))
      glob.planetList.append(Planet((1200,200), 30, 10, playerN))
      glob.planetList.append(Planet((1200,400), 30, 10, playerN))
      glob.wallList.append(Wall((100,-350), (100,450), player2, 500))
      glob.wallList.append(Wall((300,-450), (300,-50), player2, 500))
      glob.wallList.append(Wall((300,450), (300,50), player2, 500))
      glob.wallList.append(Wall((500,-450), (500,350), player2, 500))
      glob.wallList.append(Wall((450,300), (850,300), player2, 500))
      glob.wallList.append(Wall((950,300), (1250,300), player2, 500))
   elif level == Level.KING_OF_THE_HILL:
      glob.planetList.append(Planet((100,450), 25, 10, player1))
      glob.planetList.append(Planet((250,350), 25, 5, playerN))
      glob.planetList.append(Planet((250,550), 25, 5, playerN))
      glob.planetList.append(Planet((400,250), 35.36, 10, playerN))
      glob.planetList.append(Planet((400,450), 35.36, 10, playerN))
      glob.planetList.append(Planet((400,650), 35.36, 10, playerN))
      glob.planetList.append(Planet((550,150), 50, 15, playerN))
      glob.planetList.append(Planet((550,350), 50, 15, playerN))
      glob.planetList.append(Planet((550,550), 50, 15, playerN))
      glob.planetList.append(Planet((550,750), 50, 15, playerN))
      glob.planetList.append(Planet((700,250), 35.36, 10, playerN))
      glob.planetList.append(Planet((700,450), 35.36, 10, playerN))
      glob.planetList.append(Planet((700,650), 35.36, 10, playerN))
      glob.planetList.append(Planet((850,350), 25, 5, playerN))
      glob.planetList.append(Planet((850,550), 25, 5, playerN))
      glob.planetList.append(Planet((1000,450), 25, 10, player2))
      glob.planetList[7].addLaser(3, 350, 100)
      glob.planetList[8].addLaser(3, 350, 100)
   elif level == Level.BORROWED_TIME:
      glob.planetList.append(Planet((0,0), 30, 10, player1))
      glob.wallList.append(Wall((-220,-200), (-180,200), player1, 250))
      glob.planetList.append(Planet((-400,0), 100, 10, player2))
      glob.planetList.append(Planet((270,-10), 20, 3, playerN))
      glob.planetList.append(Planet((350,-40), 30, 5, playerN))
      glob.planetList.append(Planet((320,60), 30, 20, playerN))
      glob.planetList.append(Planet((450,20), 50, 10, playerN))
      glob.planetList.append(Planet((400,130), 30, 10, playerN))
      glob.planetList.append(Planet((550,-150), 70, 50, playerN))
      glob.planetList.append(Planet((420,-120), 20, 3, playerN))
      glob.planetList.append(Planet((580,100), 60, 30, playerN))
      glob.planetList.append(Planet((700,0), 50, 35, playerN))
      glob.planetList.append(Planet((480,170), 40, 30, playerN))
      glob.planetList.append(Planet((350,-170), 25, 20, playerN))
      glob.planetList.append(Planet((550,0), 25, 5, playerN))
      glob.planetList.append(Planet((690,-130), 30, 15, playerN))
   elif level == Level.PROTECTED:
      glob.planetList.append(Planet((100,120), 40, 15, playerN))
      glob.planetList.append(Planet((100,240), 35, 10, playerN))
      glob.planetList.append(Planet((100,350), 30, 7, playerN))
      glob.planetList.append(Planet((100,450), 25, 5, player1))
      glob.planetList.append(Planet((100,550), 30, 7, playerN))
      glob.planetList.append(Planet((100,660), 35, 10, playerN))
      glob.planetList.append(Planet((100,780), 40, 15, playerN))
      glob.planetList.append(Planet((1000,450), 75, 5, player2))
      glob.planetList.append(Planet((1000,200), 35, 150, playerN))
      glob.planetList.append(Planet((1000,700), 35, 150, playerN))
      glob.planetList[8].addLaser(5, 800, 100)
      glob.planetList[9].addLaser(5, 800, 100)
      glob.wallList.append(Wall((400,200), (600,700), playerN, 100))
   elif level == Level.DOUBLE_DUTCH:
      glob.planetList.append(Planet((0,0), 30, 10, player2))
      planetDefend = Planet((-400,-200), 40, 900, playerN)
      glob.planetList.append(planetDefend)
      planetDefend.addLaser(20, 300, 25)
      planetDefend.addLaser(20, 300, 25)
      glob.wallList.append(Wall((-220,-200), (-180,200), player2, 250))
      glob.planetList.append(Planet((-600,0), 100, 10, player1))
      glob.planetList.append(Planet((-650,-130), 20, 5, player1))
      glob.planetList.append(Planet((270,-10), 20, 3, playerN))
      glob.planetList.append(Planet((350,-40), 30, 5, playerN))
      glob.planetList.append(Planet((320,60), 45, 10, playerN))
      glob.planetList.append(Planet((450,20), 60, 10, playerN))
      glob.planetList.append(Planet((400,130), 30, 10, playerN))
      glob.planetList.append(Planet((550,-150), 80, 15, playerN))
      glob.planetList.append(Planet((420,-120), 25, 3, playerN))
      glob.planetList.append(Planet((580,100), 60, 12, playerN))
      glob.planetList.append(Planet((700,0), 50, 10, playerN))
      glob.planetList.append(Planet((480,170), 45, 8, playerN))
      glob.planetList.append(Planet((350,-170), 25, 10, playerN))
      glob.planetList.append(Planet((550,0), 25, 5, playerN))
      glob.planetList.append(Planet((690,-130), 30, 10, playerN))
   elif level == Level.ISLAND_HOPPING:
      glob.planetList.append(Planet((0,0), 30, 10, player1))
      glob.planetList.append(Planet((1000,0), 30, 10, player2))
      planetCenter = Planet((500,0), 50, 250, playerN)
      glob.planetList.append(planetCenter)
      planetCenter.addLaser(20, 800, 150)
      glob.planetList.append(Planet((80,100), 30, 10, playerN))
      glob.planetList.append(Planet((80,-100), 30, 10, playerN))
      glob.planetList.append(Planet((205,170), 30, 10, playerN))
      glob.planetList.append(Planet((205,-170), 30, 10, playerN))
      glob.planetList.append(Planet((350,200), 30, 10, playerN))
      glob.planetList.append(Planet((350,-200), 30, 10, playerN))
      glob.planetList.append(Planet((500,210), 30, 10, playerN))
      glob.planetList.append(Planet((500,-210), 30, 10, playerN))
      glob.planetList.append(Planet((650,200), 30, 10, playerN))
      glob.planetList.append(Planet((650,-200), 30, 10, playerN))
      glob.planetList.append(Planet((795,170), 30, 10, playerN))
      glob.planetList.append(Planet((795,-170), 30, 10, playerN))
      glob.planetList.append(Planet((920,100), 30, 10, playerN))
      glob.planetList.append(Planet((920,-100), 30, 10, playerN))
     
      
   centerWinPos()
   

def getWinner(countNeutral=False):
   aliveList = []
   for p in glob.playerList:
      aliveList.append(False)
   for p in glob.planetList:
      aliveList[glob.playerList.index(p.player)] = True
   for c in glob.caravanList:
      aliveList[glob.playerList.index(c.player)] = True
   if not countNeutral:
      for pId in range(len(glob.playerList)):
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
   r = a[0]-p[0], a[1]-p[1]   # r = vector from p to a
   s = b[0]-q[0], b[1]-q[1]   # s = vector from q to b
   denominator = r[0]*s[1] - r[1]*s[0]   # This is equivalent to (r x s)
   numeratorT = (q[0]-p[0])*s[1] - (q[1]-p[1])*s[0]   # This is equivalent to (q - p) x s
   numeratorU = (q[0]-p[0])*r[1] - (q[1]-p[1])*r[0]   # This is equivalent to (q - p) x r
   if denominator != 0:   # True if the lines are not parallel
      t = 1.0*numeratorT/denominator
      u = 1.0*numeratorU/denominator
      if 0 <= u and u <= 1 and 0 <= t and t<= 1:   # True if the intersection occures on the line segments
         return q[0]+u*s[0], q[1]+u*s[1]   # This is equivalent to q + us
      else:
         return None
   else:
      if r[0] == 0 and r[1] == 0:   # True if line1 is a point, which will always produce 0 for num and denom
         if s[0] == 0 and s[1] == 0:   # True if line2 is also a point
            if p[0] == q[0] and p[1] == q[1]:   # True if line1 and line2 are the same point
               return p
            else:
               return None
         else:   # If line1 is a point, we need to fix numerator for collinearity test
            numeratorU = numeratorT
      if numeratorU != 0:   # True if the lines are not collinear
         return None
      else:
         if r[0] == 0:   # True if both lines are completely vertical
            if (p[1]-q[1])*(p[1]-b[1]) <= 0:   # True if p is between q and b
               return p
            elif (a[1]-q[1])*(a[1]-b[1]) <= 0:   # True if a is between q and b
               return a
            elif (q[1]-p[1])*(q[1]-a[1]) <= 0:   # True if q (and b) is between p and a
               return q
            else:   # True if lines are collinear but not overlapping
               return None
         else:
            if (p[0]-q[0])*(p[0]-b[0]) <= 0:   # True if p is between q and b
               return p
            elif (a[0]-q[0])*(a[0]-b[0]) <= 0:   # True if a is between q and b
               return a
            elif (q[0]-p[0])*(q[0]-a[0]) <= 0:   # True if q (and b) is between p and a
               return q
            else:   # True if lines are collinear but not overlapping
               return None

def centerWinPos():
   range = {'x':[math.inf, -math.inf], 'y':[math.inf, -math.inf]}
   for p in glob.planetList:
      range['x'][0] = min(range['x'][0], p.pos[0] - p.size)
      range['x'][1] = max(range['x'][1], p.pos[0] + p.size)
      range['y'][0] = min(range['y'][0], p.pos[1] - p.size)
      range['y'][1] = max(range['y'][1], p.pos[1] + p.size)
   glob.winPosRaw = (range['x'][0] + range['x'][1] - (glob.windowSurface.get_width()-100)) / 2, (range['y'][0] + range['y'][1] - glob.windowSurface.get_height()) / 2
   glob.winPos = int(glob.winPosRaw[0]), int(glob.winPosRaw[1])

def applySpeedInd(speedListInd):
   speedListInd = max(0, speedListInd)
   speedListInd = min(len(glob.speedList)-1, speedListInd)
   glob.speedListInd = speedListInd
   glob.gameTimeStep = glob.speedList[glob.speedListInd] / glob.frameRate

def runBattle(level, player1, player2, aiTest=None):
   isAiBattle = aiTest is not None
   glob.userPlayer = None
   glob.userToGameInteractionDisabled = True
   for p in [player1, player2]:
      if isinstance(p, Human):
         glob.userPlayer = p
         glob.userToGameInteractionDisabled = False
   
   glob.playerList = []
   playerN = Neutral((191,191,191))
   glob.playerList.append(player1)
   glob.playerList.append(playerN)
   glob.playerList.append(player2)
   applySpeedInd(3)

   result = {'winner':None, 'time':0}
   util.makeLevel(level, player1, player2, playerN)
   pointer = Pointer()
   winDelayMs = 3000
   
   # Set up logic specific to Ai testing or not
   framePeriodLimit = 0
   if isAiBattle:
      framePeriodLimit = 0.9*1000/glob.frameRate
      winDelayMs = 0
      
      
   while result['winner'] is None or winDelayMs > 0:
      ####### Handle Input Events ##################################
      util.handleInputEvents()
      
      ####### Perform Game Logic #############################
      stepsPerFrame = 1
      if isAiBattle: stepsPerFrame = aiTest.stepsPerFrame
      for i in range(stepsPerFrame):

         result['time'] += glob.gameTimeStep

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
      if isAiBattle: aiTest.drawProgressBar()
      
      statTexts = []
      statTexts.append(f"Level: {level}, {Level(level).name.replace('_',' ').title()}")
      statTexts.append(f'FPS: {round(glob.fpsClock.get_fps())}')
      statTexts.append(f"Time: {round(result['time'], 1)}s")
      speed = glob.speedList[glob.speedListInd]
      if isAiBattle: speed *= aiTest.stepsPerFrame
      speedText = f'{round(speed)}x'
      if speed < 1: speedText = f'x/{round(1/speed)}'
      statTexts.append(f'Speed: {speedText}')
      yVal = 25
      for t in statTexts:
         util.drawText(t, (20,yVal), align_h='left')
         yVal += 35
      
      if pointer is not None: pointer.draw()

      result['winner'] = util.getWinner()
      if result['winner'] is not None:
         winDelayMs -= glob.fpsClock.get_time()

      # Draw buffer and wait
      pygame.display.update()
      glob.fpsClock.tick(glob.frameRate)
      
      if isAiBattle:
         stepsPerFrameAdjust = 1 if glob.fpsClock.get_rawtime() < framePeriodLimit else -1
         aiTest.stepsPerFrame += stepsPerFrameAdjust
         
   return result

