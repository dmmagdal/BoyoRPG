import pygame
import time
import random
import MapLinks
import BoyoRPG

#pygame.init()

#Jack's enemy test class
#some revision done by Alex


#Boss is a non-player-seeking object
#It merely paths between two regions on the screen

#Boss2 is a player seeking object
class Boss(object):
    def __init__(self, x, y, image, health = None):
        self.arrived = False
        self.x_vel = 0 #player x velocity
        self.y_vel = 0 #player y velocity
        self.x = x
        self.y = y
        self.health = 215
        self.dmg = 4
        self.knockback = "none"
        self.image = image
        self.atk = False
        self.rotate = False
        self.invent = []
        self.w = 215 #player width
        self.h = 235 #player height

    def displayMob(self):
        BoyoRPG.gameDisplay.blit(self.image, (self.x,self.y))
        swing = False
        self.healthBar()

    #Alex added hp bar based off players
    def healthBar(self):
        hpColor = BoyoRPG.green
        if (self.health < 0):
            self.health = 0
            #boyorpg.restart()
        pygame.draw.rect(BoyoRPG.gameDisplay, BoyoRPG.black, (self.x-2, self.y-11, 219, 9))
        pygame.draw.rect(BoyoRPG.gameDisplay, BoyoRPG.red, (self.x, self.y-9, 215, 5))
        pygame.draw.rect(BoyoRPG.gameDisplay, hpColor, (self.x, self.y-9, self.health, 5))
    
#update mobs coordinates and screen boundary checking
    def moveMob(self, xN, yN):
        self.x += xN
        self.y += yN

#moves a mob object toward the player
    def seek(self, pInst):
        if self.rotate:
            self.moveMob(0, -2)
        else:
            self.moveMob(0, 2)
        
        if (self.y > 350):
            self.rotate = True
        if (self.y < 10):
            self.rotate = False
            
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
        futureEnemRect = pygame.Rect(x, y, 215, 235)
        pygame.draw.rect(BoyoRPG.gameDisplay, (0,0,0), (x, y, 215, 235), 1)
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

    def fireAtk(self, pInst):
        ball1 = FireBall(self.x - 20, self.y - 20)
        ball2 = FireBall(self.x - 20, self.y + 20)
        ball3 = FireBall(self.x - 20, self.y + 40)
        ball1.seek(pInst.x, pInst.y)
        ball2.seek(pInst.x, pInst.y)
        ball3.seek(pInst.x, pInst.y)        
            
    def isAlive(self):
        if (self.health <= 0):
            return 0
        return 1

    def getX(self):
        return self.x

    def getY(self):
        return self.y


#Fireballs are essentially mob projectiles that seek towards player
#They spawn from another mob's location in our usage
class FireBall(object):
    def __init__(self, x, y, image, health = None):
        self.arrived = False
        self.x_vel = 0 # x velocity
        self.y_vel = 0 # y velocity
        self.x = x
        self.y = y
        self.health = 30
        self.dmg = 1
        self.knockback = "none"
        self.image = image
        self.atk = False
        self.rotate = False
        self.invent = []
        self.w = 30 # width
        self.h = 35 # height

    def seek(self, pInst):
        if random.randint(0, 100) < 5:
            if (self.x < pInst.x):
                self.x_vel = 2
            if(self.x > pInst.x):
                self.x_vel = -2  
            if (self.y < pInst.y):
                self.y_vel = 2 
            elif(self.y > pInst.y):
                self.y_vel = -2
        self.moveMob(self.x_vel, self.y_vel)
        self.charCollision(pInst)

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


    def displayMob(self):
        BoyoRPG.gameDisplay.blit(self.image, (self.x,self.y))
        if self.isAlive(): 
            self.healthBar()
        swing = False


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

    def charCollision(self, pInst):
        x = pInst.x + pInst.x_vel/2
        y = pInst.y + pInst.y_vel/2
        futurePlayRect = pygame.Rect(x, y, 30,35)
        x = self.x + self.x_vel/2
        y = self.y + self.y_vel/2
        futureEnemRect = pygame.Rect(x, y, self.w, self.h)
        #pygame.draw.rect(BoyoRPG.gameDisplay, (0,0,0), (x, y, self.w, self.h), 1)
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

    def healthBar(self):
        hpColor = BoyoRPG.green
        if (self.health < 0):
            self.health = 0
        pygame.draw.rect(BoyoRPG.gameDisplay, BoyoRPG.black, (self.x-2, self.y-11, 34, 9))
        pygame.draw.rect(BoyoRPG.gameDisplay, BoyoRPG.red, (self.x, self.y-9, 30, 5))
        pygame.draw.rect(BoyoRPG.gameDisplay, hpColor, (self.x, self.y-9, self.health, 5))
    

    def isAlive(self):
        if (self.health <= 0):
            return 0
        return 1

    def respawn(self, eInst):
        self.x = eInst.x - 20
        self.y = eInst.y - 20
        self.health = 30
        
    def getX(self):
        return self.x

    def getY(self):
        return self.y

#These are just the falling rocks in lavaroom and arena
class Rocks(object):
    def __init__(self, image, health = None):
        self.arrived = False
        self.x_vel = 0 # x velocity
        self.y_vel = 0 # y velocity
        self.x = random.randint(0, 800) 
        self.y = random.randint(-300, -40)
        self.dmg = 1
        self.health = 1
        self.image = image
        self.atk = False
        self.rotate = False
        self.w = 30 # width
        self.h = 35 # height

    def fall(self, pInst):
        pygame.draw.rect(BoyoRPG.gameDisplay, BoyoRPG.black, (self.x, self.y, 30, 35))
        self.y += 5
        self.charCollision(pInst) 
        if self.y >= 600:
                self.y = random.randint(-300, -40)
                self.x = random.randint(0, 800)
                
    def charCollision(self, pInst):
        x = pInst.x + pInst.x_vel/2
        y = pInst.y + pInst.y_vel/2
        futurePlayRect = pygame.Rect(x, y, 30,35)
        x = self.x + self.x_vel/2
        y = self.y + self.y_vel/2
        futureEnemRect = pygame.Rect(x, y, self.w, self.h)
        #pygame.draw.rect(BoyoRPG.gameDisplay, (0,0,0), (x, y, self.w, self.h), 1)
        if futurePlayRect.colliderect(futureEnemRect):
            pInst.takeDamage(self.dmg)


    def displayMob(self):
        #pygame.draw.rect(BoyoRPG.gameDisplay, BoyoRPG.black, (self.x, self.y, 30, 35))
        BoyoRPG.gameDisplay.blit(self.image, (self.x,self.y))
        self.y += 5
        if self.y >= 600:
                self.y = random.randint(-300, -40)
                self.x = random.randint(0, 800)

    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def seek(self, pInst):
        pass
    def isAlive(self):
        return 1
        
    def healthBar(self, pInst):
        pass
    
    def takeDamage(self, damage):
        pass


#Boss2 IS a player seeking object
class Boss2(object):
    def __init__(self, x, y, image, health = None):
        self.arrived = False
        self.x_vel = 0 # x velocity
        self.y_vel = 0 # y velocity
        self.x = x
        self.y = y
        self.health = 215
        self.dmg = 4
        self.knockback = "none"
        self.image = image
        self.atk = False
        self.rotate = False
        self.invent = []
        self.w = 215 # width
        self.h = 235 # height

    def displayMob(self):
        BoyoRPG.gameDisplay.blit(self.image, (self.x,self.y))
        swing = False
        self.healthBar()

#Alex added hp bar based off players
    def healthBar(self):
        hpColor = BoyoRPG.green
        if (self.health < 0):
            self.health = 0
            #boyorpg.restart()
        pygame.draw.rect(BoyoRPG.gameDisplay, BoyoRPG.black, (self.x-2, self.y-11, 219, 9))
        pygame.draw.rect(BoyoRPG.gameDisplay, BoyoRPG.red, (self.x, self.y-9, 215, 5))
        pygame.draw.rect(BoyoRPG.gameDisplay, hpColor, (self.x, self.y-9, self.health, 5))
    
#update mobs coordinates and screen boundary checking
    def moveMob(self, xN, yN):
        self.x += xN
        self.y += yN
 
#moves a mob object toward the player
    def seek(self, pInst):
        #print(self, self.x, self.y)
        if random.randint(0, 100) < 18:
            if (self.x < pInst.x):
                self.x_vel = 2
            if(self.x > pInst.x):
                self.x_vel = -2  
            if (self.y < pInst.y):
                self.y_vel = 2 
            elif(self.y > pInst.y):
                self.y_vel = -2
        self.moveMob(self.x_vel, self.y_vel)
        self.charCollision(pInst)
            
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
        futureEnemRect = pygame.Rect(x, y, 215, 235)
        pygame.draw.rect(BoyoRPG.gameDisplay, (0,0,0), (x, y, 215, 235), 1)
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

    def fireAtk(self, pInst):
        ball1 = FireBall(self.x - 20, self.y - 20)
        ball2 = FireBall(self.x - 20, self.y + 20)
        ball3 = FireBall(self.x - 20, self.y + 40)
        ball1.seek(pInst.x, pInst.y)
        ball2.seek(pInst.x, pInst.y)
        ball3.seek(pInst.x, pInst.y)        
            
    def isAlive(self):
        if (self.health <= 0):
            return 0
        return 1

    def getX(self):
        return self.x

    def getY(self):
        return self.y


