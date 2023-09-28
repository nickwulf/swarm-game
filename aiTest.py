import sys, math, random, time, pygame
import pygame.gfxdraw

# Import global variables
import globals as glob
import utilities as util

# Import user classes
from player import *
from planet import *
from caravan import *

class AiTest:
  
  def __init__(self, ai1, ai2):
    self.ai1 = ai1
    self.ai2 = ai2
    self.ai1.color = (64,64,191)
    self.ai2.color = (191,64,64)
    self.level = 0
    self.battleNum = 0
    self.stepsPerFrame = 100
    self.gameList1 = []
    self.gameList2 = []
  
  def runTest(self, level, battleNum):
    self.level = level
    self.battleNum = battleNum
    
    # Gather results
    self.gameList1 = []
    self.gameList2 = []
    for i in xrange(self.battleNum):
      results = self.runBattle()
    graphPic = self.makeGraphPic()
    
    # Pause until user clicks
    util.handleInputEvents()  # flush input events
    done = False
    while not done:
      util.handleInputEvents()
      if glob.mouseLeftButtonClicked:
        done = True
      glob.windowSurface.blit(graphPic, (0,0))
      pygame.display.update()
      glob.fpsClock.tick(glob.frameRate)
    
  def runBattle(self):
    oldInteractionValue = glob.userToGameInteractionDisabled
    glob.userToGameInteractionDisabled = True
    glob.playerList = []
    glob.playerList.append(self.ai1)
    glob.playerList.append(Neutral((191,191,191)))
    glob.playerList.append(self.ai2)
    util.makeLevel(self.level)
    framePeriodLimit = 0.9*1000/glob.frameRate
    gameOver = False
    gameTimer = 0
    while not gameOver:
      util.handleInputEvents()
      for i in xrange(self.stepsPerFrame):
        if util.getWinner() is None:
          gameTimer += glob.gameTimeStep
        else:
          gameOver = True
        # Handle player inputs
        for p in glob.playerList:
          p.update()
        # Handle game action
        for p in glob.planetList:
          p.update()
        for c in glob.caravanList:
          c.update()
          
      # Draw intermediate results to the screen
      glob.windowSurface.fill((232,232,232))
      for p in glob.planetList:
        p.draw()
      for c in glob.caravanList:
        c.draw()
      util.drawHud()
      self.drawProgressBar()
      pygame.display.update()
      glob.fpsClock.tick(glob.frameRate)
      if glob.fpsClock.get_rawtime() < framePeriodLimit:
        self.stepsPerFrame += 1
      else:
        self.stepsPerFrame -= 1
      
    glob.userToGameInteractionDisabled = oldInteractionValue
    if util.getWinner() is self.ai1:
      self.gameList1.append(gameTimer)
    else:
      self.gameList2.append(gameTimer)
  
  def drawProgressBar(self):
    pygame.gfxdraw.rectangle(glob.windowSurface, (19,19,1062,32), (0,0,0))
    limit1 = round(1060.0 * len(self.gameList1) / self.battleNum)
    limit2 = round(1060.0 * (len(self.gameList1)+len(self.gameList2)) / self.battleNum)
    limit3 = round(1060.0)
    if len(self.gameList1) > 0:
      pygame.gfxdraw.box(glob.windowSurface, (20,20,limit1,30), self.ai1.color)
    if len(self.gameList2) > 0:
      pygame.gfxdraw.box(glob.windowSurface, (20+limit1,20,limit2-limit1,30), self.ai2.color)
    pygame.gfxdraw.box(glob.windowSurface, (20+limit2,20,limit3-limit2,30), (191,191,191))

  
  def makeGraphPic(self):
    surf = glob.windowSurface.copy()
    
    # Set graph parameters
    graphDim = 500,250
    graphOrigin = 350,400
    maxTime = 20*60
    binWidth = 1.0*maxTime/graphDim[0]
    
    # Set parameters of Gaussian filter
    stdDev = 15
    variance = stdDev**2
    gaussScale = 1.0/stdDev/math.sqrt(2.0*math.pi)
    
    # Calculate graph data
    valueBins1 = []
    valueBins2 = []
    for x in xrange(graphDim[0]+1):
      valueBins1.append(0)
      valueBins2.append(0)
      xVal = 1.0*x/graphDim[0]*maxTime
      for time in self.gameList1:
        #if math.fabs(time-xVal) <= 30:
        #  valueBins1[x] += 1.0/self.battleNum
        valueBins1[x] += 60.0/self.battleNum*gaussScale*math.exp((-(xVal-time)**2.0)/(2.0*variance))
      for time in self.gameList2:
        #if math.fabs(time-xVal) <= 30:
        #  valueBins1[x] += 1.0/self.battleNum
        valueBins2[x] += 60.0/self.battleNum*gaussScale*math.exp((-(xVal-time)**2.0)/(2.0*variance))
    
    # Find maximum y dimension
    maxWins = int(math.ceil(4*max(max(valueBins1),max(valueBins2))))/4.0
    
    # Adjust graph data vertically to match graphDim
    for x in xrange(len(valueBins1)):
      valueBins1[x] = 1.0*valueBins1[x]/maxWins*graphDim[1]
      valueBins2[x] = 1.0*valueBins2[x]/maxWins*graphDim[1]
    
    # Clear draw surface
    surf.fill((232,232,232))
    
    # Draw the data
    for x in xrange(graphDim[0]):
      pygame.draw.aaline(surf, (0,0,255), (graphOrigin[0]+x, graphOrigin[1]-valueBins1[x]), (graphOrigin[0]+x+1, graphOrigin[1]-valueBins1[x+1]))
      pygame.draw.aaline(surf, (255,0,0), (graphOrigin[0]+x, graphOrigin[1]-valueBins2[x]), (graphOrigin[0]+x+1, graphOrigin[1]-valueBins2[x+1]))
      
    # Draw the base graph
    graphFont = pygame.font.SysFont("arial", 20, True, False)
    pygame.draw.line(surf, (0,0,0), graphOrigin, (graphOrigin[0], graphOrigin[1]-graphDim[1]))
    pygame.draw.line(surf, (0,0,0), graphOrigin, (graphOrigin[0]+graphDim[0], graphOrigin[1]))
    for x in xrange(maxTime/120 + 1):
      offset = x*120.0/maxTime*graphDim[0]
      offset = int(round(offset))
      pygame.draw.line(surf, (0,0,0), (graphOrigin[0]+offset, graphOrigin[1]), (graphOrigin[0]+offset, graphOrigin[1]+5))
      util.drawText(x*2, (graphOrigin[0]+offset, graphOrigin[1]+15), graphFont, surf)
    for y in xrange(6):
      offset = y/5.0*graphDim[1]
      offset = int(round(offset))
      pygame.draw.line(surf, (0,0,0), (graphOrigin[0], graphOrigin[1]-offset), (graphOrigin[0]-5, graphOrigin[1]-offset))
      util.drawText(round(y/5.0*maxWins,2), (graphOrigin[0]-25, graphOrigin[1]-offset), graphFont, surf)
    util.drawText("Time Until Victory PDF", (graphOrigin[0]+0.5*graphDim[0], graphOrigin[1]-graphDim[1]-40), pygame.font.SysFont("arial", 30, True, False), surf) 
    util.drawText("Game Time (minutes)", (graphOrigin[0]+0.5*graphDim[0], graphOrigin[1]+50), pygame.font.SysFont("arial", 25, True, False), surf)
    
    # Perform final analysis and draw table
    tableCenTop = graphOrigin[0]+0.5*graphDim[0], graphOrigin[1]+125
    winPercent1 = round(100.0 * len(self.gameList1) / self.battleNum, 1)
    winPercent2 = str(100 - winPercent1) + "%"
    winPercent1 = str(winPercent1) + "%"
    avgTime1 = "N/A"
    avgTime2 = "N/A"
    if len(self.gameList1) > 0:
      avgTime1 = int(round(sum(self.gameList1) / len(self.gameList1)))
      if avgTime1%60 < 10:
        avgTime1 = str(avgTime1/60) + ":0" + str(avgTime1%60)
      else:
        avgTime1 = str(avgTime1/60) + ":" + str(avgTime1%60)
    if len(self.gameList2) > 0:
      avgTime2 = int(round(sum(self.gameList2) / len(self.gameList2)))
      if avgTime2%60 < 10:
        avgTime2 = str(avgTime2/60) + ":0" + str(avgTime2%60)
      else:
        avgTime2 = str(avgTime2/60) + ":" + str(avgTime2%60)
    util.drawText("Results Summary", (tableCenTop[0], tableCenTop[1]), pygame.font.SysFont("arial", 30, True, False), surf)
    util.drawText("Wins", (tableCenTop[0]-40, tableCenTop[1]+50), pygame.font.SysFont("arial", 25, True, False), surf)
    util.drawText("Time", (tableCenTop[0]+40, tableCenTop[1]+50), pygame.font.SysFont("arial", 25, True, False), surf)
    pygame.draw.line(surf, (0,0,0), (tableCenTop[0], tableCenTop[1]+40), (tableCenTop[0], tableCenTop[1]+125))
    pygame.draw.line(surf, (0,0,0), (tableCenTop[0]-70, tableCenTop[1]+65), (tableCenTop[0]+70, tableCenTop[1]++65))
    util.drawText(winPercent1, (tableCenTop[0]-40, tableCenTop[1]+85), pygame.font.SysFont("arial", 25, True, False), surf, self.ai1.color)
    util.drawText(avgTime1, (tableCenTop[0]+40, tableCenTop[1]+85), pygame.font.SysFont("arial", 25, True, False), surf, self.ai1.color)
    util.drawText(winPercent2, (tableCenTop[0]-40, tableCenTop[1]+115), pygame.font.SysFont("arial", 25, True, False), surf, self.ai2.color)
    util.drawText(avgTime2, (tableCenTop[0]+40, tableCenTop[1]+115), pygame.font.SysFont("arial", 25, True, False), surf, self.ai2.color)
    
    # Return the draw surface
    return surf
