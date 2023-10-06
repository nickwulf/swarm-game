import os, sys, math, random, time, pygame
from pygame.locals import *
import pygame.gfxdraw

# Import global variables
from . import globals as glob
from . import utilities as util

# Import user classes
from .player import *
from .planet import *
from .caravan import *
from .particle import *

dir_path = os.path.dirname(os.path.realpath(__file__))
baseColorSurf = pygame.image.load(os.path.join(dir_path, 'images', 'LaserColor.bmp'))
baseCoverSurf = pygame.image.load(os.path.join(dir_path, 'images', 'LaserCover.bmp'))

class Laser:

   def __init__(self, planet, power, range, speed):
      self.planet = planet
      self.range = range
      self.angle = random.uniform(0,360)
      self.maxSpeed = speed
      self.power = power
      self.idleSpeed = 0
      self.makeIdleSpeed()
      self.drawSurf = baseColorSurf.copy()
      self.drawSurf.fill(self.planet.player.color, special_flags=BLEND_MULT)
      self.drawSurf.blit(baseCoverSurf, (0,0))
      self.targetCaravan = None
      self.shooting = False
      self.thickness = random.uniform(0,2)
      self.gunPos = (0, 0)
      self.gunDrawPos = self.gunPos[0]-glob.winPos[0], self.gunPos[1]-glob.winPos[1]

   def update(self):
      maxDistSq = (self.range + self.planet.size)**2
      minDistSq = (self.planet.size+20)**2
      anglePerDist = math.degrees(1.0/self.planet.size)
      speedAlpha = glob.gameTimeStep * anglePerDist

      # Find caravan that requires the least turning
      self.targetCaravan = None
      self.shooting = False
      bestDeltaAngle = 200
      bestDistSq = 0
      noTurnNeeded = False
      for c in glob.caravanList:
         if c.player is self.planet.player:
            continue
         cDelta = c.pos[0]-self.planet.pos[0], c.pos[1]-self.planet.pos[1]
         cDistSq = cDelta[0]**2 + cDelta[1]**2
         if cDistSq < minDistSq or cDistSq > maxDistSq:
            continue
         cAngle = math.degrees(math.atan2(cDelta[1],cDelta[0]))%360
         deltaAngle = self.getDeltaAngle(cAngle)
         if noTurnNeeded: # If already pointed at a target, then choose closest target
            if math.fabs(deltaAngle) < self.maxSpeed * speedAlpha and cDistSq < bestDistSq:
               bestDeltaAngle = deltaAngle
               self.targetCaravan = c
               bestDistSq = cDistSq
         else:
            if math.fabs(deltaAngle) < math.fabs(bestDeltaAngle):
               bestDeltaAngle = deltaAngle
               self.targetCaravan = c
               if math.fabs(bestDeltaAngle) < self.maxSpeed * speedAlpha:
                  bestDistSq = cDistSq
                  noTurnNeeded = True

      if self.targetCaravan is not None:
         self.makeIdleSpeed()
         if math.fabs(bestDeltaAngle) < self.maxSpeed * speedAlpha:
            self.angle += bestDeltaAngle
            self.shooting = True
            self.targetCaravan.takeDamage(self.power * glob.gameTimeStep)
         else:
            self.angle += math.copysign(self.maxSpeed * speedAlpha, bestDeltaAngle)
      else:
         self.angle += self.idleSpeed * speedAlpha
      self.angle = self.angle % 360

      # Determine gun position and make sparks
      offset2 = self.planet.pos[0] + (7+self.planet.size)*math.cos(math.radians(self.angle)), self.planet.pos[1] + (7+self.planet.size)*math.sin(math.radians(self.angle))
      offset3 = 0,0
      if self.angle < 135 or self.angle > 315:
         offset3 = 0,1
      if self.angle < 45 or self.angle > 225:
         offset3 = 1, offset3[1]
      self.gunPos = offset2[0]+offset3[0], offset2[1]+offset3[1]
      if self.shooting:
         sparkCount = util.getPoissonCount(6.0*glob.gameTimeStep)
         for i in range(sparkCount):
            glob.particleList.append(LaserSpark(self.gunPos,self.angle, random.uniform(-180,180),random.uniform(60,180),self.planet.player.color, 0.5, 0.1))

      self.gunDrawPos = self.gunPos[0]-glob.winPos[0], self.gunPos[1]-glob.winPos[1]

   def draw(self):
      # Draw beam
      if self.shooting:
         if glob.gameTimeStep != 0:
            self.thickness = random.uniform(0,2)
         laserColor = util.changeLuminosity(self.planet.player.color, 50)
         beamColor = util.combineColors((255,255,255), laserColor, 1.0 -self.thickness/2.0)
         targetDist = math.hypot(self.gunPos[0]-self.targetCaravan.pos[0], self.gunPos[1]-self.targetCaravan.pos[1])
         points = [(0,self.thickness), (targetDist,self.thickness), (targetDist,-self.thickness), (0,-self.thickness)]
         angleCos = math.cos(math.radians(self.angle))
         angleSin = math.sin(math.radians(self.angle))
         for i in range(len(points)):
            points[i] = self.gunDrawPos[0]+points[i][0]*angleCos - points[i][1]*angleSin, self.gunDrawPos[1]+points[i][0]*angleSin + points[i][1]*angleCos
         pygame.gfxdraw.filled_polygon(glob.windowSurface, points, beamColor)
         pygame.gfxdraw.aapolygon(glob.windowSurface, points, beamColor)

      # Draw gun
      tempDrawSurf = pygame.transform.rotozoom(self.drawSurf, -self.angle, 1)
      offset1 = -tempDrawSurf.get_width()/2, -tempDrawSurf.get_height()/2
      glob.windowSurface.blit(tempDrawSurf, (offset1[0]+self.gunDrawPos[0], offset1[1]+self.gunDrawPos[1]))

   def getDeltaAngle(self, targetAngle):
      # Returns difference between self.angle and targetAngle between -180 and 180 degrees
      deltaAngle = targetAngle - self.angle
      deltaAngle = deltaAngle % 360
      if deltaAngle > 180:
         deltaAngle -= 360
      return deltaAngle

   def makeIdleSpeed(self):
      self.idleSpeed = random.uniform(self.maxSpeed/6.0, self.maxSpeed/2.0)
      if random.random() < .5:
         self.idleSpeed *= -1

   def updateChanges(self):
      self.drawSurf = baseColorSurf.copy()
      self.drawSurf.fill(self.planet.player.color, special_flags=BLEND_MULT)
      self.drawSurf.blit(baseCoverSurf, (0,0))
