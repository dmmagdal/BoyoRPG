import pygame
import time
import random
import MapLinks
import BoyoRPG

#pygame.init()

#Jack's enemy test class
#some revision done by Alex

class Mob(object):
    def __init__(self, x, y, image, health = None):
        self.arrived = False
        self.x_vel = 0 #player x velocity
        self.y_vel = 0 #player y velocity
        self.x = x
        self.y = y
        self.health = 30
        self.dmg = 3
        self.knockback = "none"
        self.image = image
        self.atk = False
        self.rotate = False
        self.invent = []
        self.w = 30 #player width
        self.h = 35 #player height

    def displayMob(self):
        #pygame.draw.rect(BoyoRPG.gameDisplay, BoyoRPG.black,(self.x,self.y,30,35))
        self.image = BoyoRPG.orc
        image2 = pygame.transform.flip(self.image, 1, 0)
        #if mob is moving left
        if self.x_vel < 0: 
            self.rotate = True
            image2 = MapLinks.orcLstride
            #animation condition
            if (self.x % 3 == 0):
                image2 = MapLinks.orcLstride2
        #if mob is moving right
        elif self.x_vel > 0:
            self.rotate = False
            self.image = MapLinks.orcRstride
            #animation condition
            if (self.x % 3 == 0):
                self.image =  MapLinks.orcRstride2
        #blit the image for left animation
        if self.rotate:
            BoyoRPG.gameDisplay.blit(image2, (self.x,self.y))
         #blit the image for right animation              
        else:
            BoyoRPG.gameDisplay.blit(self.image, (self.x,self.y))
        swing = False
        self.healthBar()

    #Alex added hp bar based off players
    def healthBar(self):
        hpColor = BoyoRPG.green
        if (self.health < 0):
            self.health = 0
            #boyorpg.restart()
        pygame.draw.rect(BoyoRPG.gameDisplay, BoyoRPG.black, (self.x-2, self.y-11, 34, 9))
        pygame.draw.rect(BoyoRPG.gameDisplay, BoyoRPG.red, (self.x, self.y-9, 30, 5))
        pygame.draw.rect(BoyoRPG.gameDisplay, hpColor, (self.x, self.y-9, self.health, 5))
    
    #update mobs coordinates and screen boundary checking
    def moveMob(self, xN, yN):
        self.x += xN
        self.y += yN
        #boundary checking
        if (self.x > BoyoRPG.display_width-9):
            self.x = self.x - 5 
        if (self.x < 0):
            self.x = 0
        if (self.y > BoyoRPG.display_height - 10):
            self.y = self.y - 5
        if (self.y < 0):
            self.y = 0

        #moves a mob object toward the player
    def seek(self, pInst):
        if (self.x < pInst.x):
            self.x_vel = 2
        if(self.x > pInst.x):
            self.x_vel = -2  
        if (self.y < pInst.y):
            self.y_vel = 2 
        elif(self.y > pInst.y):
            self.y_vel = -2
        #move mob to new loaction

    #Set knockback value and take damage
    def takeDamage(self, damage):
        if self.knockback == "left":
            self.moveMob(-12,0)
            BoyoRPG.gameDisplay.blit(self.image, (self.x,self.y))
        if self.knockback == "right":
            self.moveMob(12,0)
            BoyoRPG.gameDisplay.blit(self.image, (self.x,self.y))
        if self.knockback == "top":
            self.moveMob(0,-12)
            BoyoRPG.gameDisplay.blit(self.image, (self.x,self.y))
        if self.knockback == "bottom":
            self.moveMob(0,12)
            BoyoRPG.gameDisplay.blit(self.image, (self.x,self.y))          
         
        self.health -= damage
        self.healthBar()
       
    #detects collision between and an enemy and player
    def charCollision(self, pInst):
        x = pInst.x + pInst.x_vel/2
        y = pInst.y + pInst.y_vel/2
        futurePlayRect = pygame.Rect(x, y, 30,35)
        x = self.x + self.x_vel/2
        y = self.y + self.y_vel/2
        futureEnemRect = pygame.Rect(x, y, 30, 35)
        if futurePlayRect.colliderect(futureEnemRect):
            pInst.takeDamage(self.dmg)
            if self.x + 30 - 1 <= futurePlayRect.left:
                self.x_vel = 0 #stop x velocity
                self.knockback = "left"
            if self.x >= futurePlayRect.right - 1 :
                self.x_vel = 0 #stop x velocity
                self.knockback = "right"
            if self.y + 35 - 1 <= futurePlayRect.top:
                self.y_vel = 0 #stop y velocity from the top
                self.knockback = "top"
            if self.y - 1 >= futurePlayRect.bottom - 1:
                self.y_vel = 0 #stop y velocity from the bottom
                self.knockback = "bottom"
            #if there is a collision, dont move mob
        #if theres no collision, move mob
        else:
            self.moveMob(self.x_vel,self.y_vel)


    def isAlive(self):
        if (self.health <= 0):
            return 0

        return 1

    def getX(self):
        return self.x

    def getY(self):
        return self.y
