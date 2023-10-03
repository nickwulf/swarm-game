import os, sys, math, random, time, pygame
from pygame.locals import *
import pygame.gfxdraw

# Import global variables and utilities
import globals as glob
import utilities as util

# Import user classes
from player import *
from planet import *
from caravan import *
from particle import *

# Electric arcs randomly appear such that the chance of such an event increases linearly as the time since the last event increases. This gives the effect of a buildup and then random release of charge. It was discovered that this produces a Rayleigh distribution. If U is a uniformly random variable from 0 to 1, then the formula (sigma) * sqrt(-2 * ln(U)) generates a random variable corresponding to the Rayleigh distribution

baseColorSurf = pygame.image.load(os.path.join("images", "WallColor.bmp"))
baseCoverSurf = pygame.image.load(os.path.join("images", "WallCover.bmp"))
arcMaxLifeRange = (0.1, 1.0)
dischargePowerRange = (0.01, 0.4)

class Wall:

   def __init__(self, pos1, pos2, player, strength):
      self.player = player
      self.pos1 = pos1
      self.pos2 = pos2
      self.strength = strength
      self.dist = math.hypot(self.pos1[0]-self.pos2[0], self.pos1[1]-self.pos2[1])
      self.vectorPar = (self.pos2[0]-self.pos1[0])/self.dist, (self.pos2[1]-self.pos1[1])/self.dist
      self.vectorPerp = -self.vectorPar[1], self.vectorPar[0]
      self.angle = math.degrees(math.atan2(self.vectorPar[1], self.vectorPar[0]))
      if self.angle == 0 or self.angle == 180:
         self.angle += 0.1
      self.arcs = []
      self.arcLives = []
      self.maxArcLives = []
      self.charge = 0
      self.drawSurf = baseColorSurf.copy()
      if self.player is None:
         self.drawSurf.fill((0,0,0), special_flags=BLEND_MULT)
      else:
         self.drawSurf.fill(self.player.color, special_flags=BLEND_MULT)
      self.drawSurf.blit(baseCoverSurf, (0,0))


   def update(self):
      if self.player is None:
         sparkColor = (0,0,0)
      else:
         sparkColor = util.changeLuminosity(self.player.color, 50)

      # Detect and react to caravan collisions
      for c in glob.caravanList:
         if c.player is self.player:
            continue
         intersect = util.findIntersection(self.pos1, self.pos2, c.pos, c.oldPos)
         if intersect is not None:
            damage = c.population
            if self.strength is not None and self.strength < damage:
               damage = self.strength
            c.takeDamage(damage, intersect)
            sparkCount = int(random.gauss(damage, damage/5.0) + 5)
            if sparkCount < 5:
               sparkCount = 5
            speedAlpha = sparkCount**(1.0/3)
            for i in range(sparkCount):
               speed = 35*speedAlpha*math.sqrt(-2*math.log(random.random()))
               glob.particleList.append(LaserSpark(intersect, random.uniform(-180,180), 0, speed, sparkColor, 0.5, 0.1))
            if self.strength is not None:
               self.strength -= damage
      if self.strength is not None and self.strength <= 0:
         glob.wallList.remove(self)
         return

      # Update old arcs
      index = 0
      while index < len(self.arcLives):
         self.arcLives[index] -= glob.gameTimeStep
         if self.arcLives[index] <= 0:
            self.arcLives.pop(index)
            self.maxArcLives.pop(index)
            self.arcs.pop(index)
         else:
            index += 1

      # strengthScale is a value from 0 to 1 with 1 being dead and 0 being infinite strength
      if self.strength is None:
         strengthScale = 0.0
      else:
         strengthScale = math.exp(-self.strength*0.00693147)

      # Make new arcs
      arcMaxLife = strengthScale * (arcMaxLifeRange[1]-arcMaxLifeRange[0]) + arcMaxLifeRange[0]
      dischargePower = math.pow(strengthScale,2.0) * (dischargePowerRange[1]-dischargePowerRange[0]) + dischargePowerRange[0]
      self.charge += glob.gameTimeStep
      while self.charge >= 0:
         if self.charge < arcMaxLife:
            self.arcs.insert(0, self.generatePoints())
            self.maxArcLives.insert(0, arcMaxLife)
            if self.charge < 0:
               self.arcLives.insert(0, arcMaxLife)
            else:
               self.arcLives.insert(0, arcMaxLife-self.charge)
         self.charge -= dischargePower*math.sqrt(-2*math.log(random.random()))

      # Make sparks
      sparkCount = util.getPoissonCount((50.0-strengthScale*47.0)*glob.gameTimeStep)
      for i in range(sparkCount):
         divergence = random.gauss(self.angle,10)
         speed = 100*math.sqrt(-2*math.log(random.random()))
         glob.particleList.append(LaserSpark(self.pos1, divergence, 0, speed, sparkColor, 0.5, 0.1))
      sparkCount = util.getPoissonCount((50.0-strengthScale*47.0)*glob.gameTimeStep)
      for i in range(sparkCount):
         divergence = random.gauss(self.angle+180,10)
         speed = 100*math.sqrt(-2*math.log(random.random()))
         glob.particleList.append(LaserSpark(self.pos2, divergence, 0, speed, sparkColor, 0.5, 0.1))

   def draw(self):
      if self.player is None:
         arcColor = (0,0,0)
      else:
         arcColor = util.changeLuminosity(self.player.color, 50)
      for i in range(len(self.arcs)):
         for j in range(len(self.arcs[i])-1):
            pygame.gfxdraw.line(glob.windowSurface, self.arcs[i][j][0]-glob.winPos[0], self.arcs[i][j][1]-glob.winPos[1], self.arcs[i][j+1][0]-glob.winPos[0], self.arcs[i][j+1][1]-glob.winPos[1], (arcColor[0],arcColor[1],arcColor[2],int(255*self.arcLives[i]/self.maxArcLives[i])))
      drawAngle = self.angle
      if drawAngle == 0 or drawAngle == 180:
         drawAngle += 0.1
      tempDrawSurf = pygame.transform.rotozoom(self.drawSurf, -drawAngle, 1)
      offset = tempDrawSurf.get_width()/2
      glob.windowSurface.blit(tempDrawSurf, (self.pos1[0]-offset-glob.winPos[0], self.pos1[1]-offset-glob.winPos[1]))
      tempDrawSurf = pygame.transform.rotozoom(self.drawSurf, 180-drawAngle, 1)
      glob.windowSurface.blit(tempDrawSurf, (self.pos2[0]-offset-glob.winPos[0], self.pos2[1]-offset-glob.winPos[1]))

   def generatePoints(self):
      distances = [0]
      totalDist = 0
      while totalDist < self.dist:
         newDist = random.expovariate(1.0/20)
         totalDist += newDist
         distances.append(totalDist)
      distances.pop()
      distances.append(self.dist)
      divergences = [0]
      for i in range(1,len(distances)-1):
         divergences.append(random.expovariate(1.0/2))
         if random.random() < .5:
            divergences[i] *= -1
      divergences.append(0)
      points = []
      for i in range(len(distances)):
         points.append((int(round(self.pos1[0]+distances[i]*self.vectorPar[0]+divergences[i]*self.vectorPerp[0])), int(round(self.pos1[1]+distances[i]*self.vectorPar[1]+divergences[i]*self.vectorPerp[1]))))
      return points
