import pygame
import time
import random
import BoyoRPG

#pygame.init()


class Sprite(object):
    def __init__(self, x, y, image, health=None):
        self.x = x
        self.y = y
        #AM 4/28/18 : moved velocity status
        self.x_vel = 0 #player x velocity
        self.y_vel = 0 #player y velocity
        self.health = 100
        self.defense = 10 #base defense
        self.baseDmg = 13 #base damage
        self.image = image
        self.atk = False
        self.rotate = False
        self.invent = []
        self.equipment = []
        self.w = 30 #player width
        self.h = 35 #player height
        self.dmg = self.getStats()

#Returns baseDmg and modifies defense correctly
    def getStats(self):
        self.defense = 15 #base defense
        self.baseDmg = 13 #base damage
        for x in range(0,len(self.equipment)):
            if type(self.equipment[x]) is Armor:
                self.defense = (self.defense +
                                (self.equipment[x].defense))
            elif type(self.equipment[x]) is Weapon:
                 self.baseDmg = (self.baseDmg +
                                 (self.equipment[x].attack))
            else:
                self.baseDmg *= 1 #filler for backlog
                self.defense *= 1
        #print("My ", self.baseDmg, self.defense)
        return self.baseDmg
    
#Stat correction and animations        
    def displayCharacter(self, swing):
        self.dmg = self.getStats()
        if swing:                      
            self.image = BoyoRPG.playerAtk      #store swing animation
        else:
            self.image = BoyoRPG.player     #store rotated swing animation
        image2 = pygame.transform.flip(self.image, 1, 0)
        if self.y_vel < 0 or self.y_vel  > 0:   #if player is moving up or down, display U/D animation
            if self.rotate == False:
                self.image = BoyoRPG.playerRstride
                if (self.y % 3   == 0):                 #creates actual animation
                    self.image =  BoyoRPG.playerRstride2
            else:
                image2 = pygame.transform.flip(BoyoRPG.playerRstride, 1, 0)   #flip image if image should be rotated
                if (self.y % 3   == 0):                                     #animation effect
                    image2 = pygame.transform.flip(BoyoRPG.playerRstride2, 1, 0)
        if self.x_vel < 0:      #if player is moving left
            self.rotate = True
            image2 = BoyoRPG.playerLstride
            if (self.x % 3   == 0):
                image2 =  BoyoRPG.playerLstride2    #animation effect
        elif self.x_vel  > 0:                       #if player is moving right
            self.rotate = False
            self.image = BoyoRPG.playerRstride
            if (self.x % 3 == 0):                   #animation effect
                self.image =  BoyoRPG.playerRstride2
            
        if self.rotate:
            BoyoRPG.gameDisplay.blit(image2, (self.x,self.y))   #print knight-standing image
        else:
            BoyoRPG.gameDisplay.blit(self.image, (self.x,self.y))   #flip knight-standing image
        swing = False
        return swing
    
#Movement of player
    def move(self):
        self.x += self.x_vel
        self.y += self.y_vel
        if self.x > BoyoRPG.display_width-9:
            self.x = self.x - 5
        if self.x < 0:
            self.x = 0
        if self.y > BoyoRPG.display_height - 10:
            self.y = self.y - 5
        if self.y < 0:
            self.y = 0
            
#Also displays stats
    def healthBar(self):
        smallText = pygame.font.Font('freesansbold.ttf', 14)
        temp = "Damge: " + str(self.dmg)
        temp2 = "Defense: " + str(self.defense)
        #print(temp2)
        TextSurf, TextRect = BoyoRPG.text_objects(temp, smallText, BoyoRPG.black)
        TextRect.center = (725, 480)
        TextSurf2, TextRect2 = BoyoRPG.text_objects(temp2, smallText, BoyoRPG.black)
        TextRect2.center = (725, 500)
        BoyoRPG.gameDisplay.blit(TextSurf, TextRect)
        BoyoRPG.gameDisplay.blit(TextSurf2, TextRect2)

        hpColor = BoyoRPG.green
        if (self.health < 0):
            self.health = 0
        elif (self.health > 100):
            self.health = 100
            #boyorpg.restart()
        pygame.draw.rect(BoyoRPG.gameDisplay, BoyoRPG.black, (675, 520, 110, 35))
        pygame.draw.rect(BoyoRPG.gameDisplay, BoyoRPG.red, (680, 525, 100, 25))
        pygame.draw.rect(BoyoRPG.gameDisplay, hpColor, (680, 525, self.health, 25))

    def swingBoundary(self,eInst):
        if eInst:
            degree = 0
            if self.rotate == True:
                swingBound = pygame.Rect(self.x - 10, self.y - 10, 25, 55)  
            else:
                swingBound = pygame.Rect(self.x + 40, self.y - 10, 25, 55)
            pygame.draw.rect(BoyoRPG.gameDisplay, BoyoRPG.blue, swingBound, 1)
            enemRect = pygame.Rect(eInst.getX(), eInst.getY(), eInst.w, eInst.h)
            if (swingBound.colliderect(enemRect)):
                eInst.takeDamage(self.dmg)
                if not eInst.isAlive:
                    eInst.moveMob(-20,-20)
                    del eInst    
            
    def add2In(self, item):
        if len(self.invent) != 20:
            self.invent.append(item)

    def dropFIn(self, item):
        self.invent.remove(item)

    def getHealth(self):
        return self.health

    def getInvent(self):
        return self.invent

    def getEquipment(self):
        return self.equipment

#Miigate damage tank based of defense stat
    def takeDamage(self, damage):
        damage = damage - (0.15 * self.defense)
        if damage < 1:
            damage = 1 
        self.health -= damage
         
        



class World(object):
    def __init__(self, x, y, Map, button=None):
        self.x = x
        self.y = y
        self.Map = Map
        self.button = button
        
    def displayWorld(self):
        BoyoRPG.gameDisplay.blit(self.Map, (self.x,self.y))
        
    def makeWorld(self, x1):
        self.displayWorld()
        #print(x1)
        
    def button(self, x, y, w, h, px, py, action, *args):
        mouse = BoyoRPG.pygame.mouse.get_pos()
        click = BoyoRPG.pygame.mouse.get_pressed()
        #global enter
    
        if x + w > px > x and y + h > py > y:
            print('almost') 
            if click[0] == 1 and action != None:
                print('yea')
                #enter = not enter
                action(*args) #runs object as function
        else:
            print('no')

    def mapLinks(self, x, y, width, height): #note lists
        for xarg, yarg, w, h in zip(x, y, width, height):
            print("xarg = ", xarg, "yarg = ", yarg, "w = ", w," h= ", h)

class ItemObj(object):
    def __init__(self):
        self.equippable = False
        self.consumable = False

    def colorFix(self):
        transColor = self.image.get_at((1,1))
        self.image.set_colorkey(transColor)

class Armor(ItemObj):
    def __init__(self, defense, image):
        #super(Armor,ItemObj).__init__()
        ItemObj.__init__(self)
        self.defense = defense
        self.image = pygame.image.load(image).convert()
        self.equippable = True
        self.consumable = not self.equippable

    def colorFix(self):
        transColor = self.image.get_at((1,1))
        self.image.set_colorkey(transColor)

class Weapon(ItemObj):
    def __init__(self, attack, image):
        #super(Weapon,ItemObj).__init__()
        ItemObj.__init__(self)
        self.attack = attack
        self.image = pygame.image.load(image).convert()
        self.equippable = True
        self.consumable = not self.equippable
        
    def colorFix(self):
            transColor = self.image.get_at((1,1))
            self.image.set_colorkey(transColor)

class Potion(ItemObj):
    def __init__(self, healthRestored, image):
        #super(Potion,ItemObj).__init__()
        ItemObj.__init__(self)
        self.healthRestored = healthRestored
        self.image = pygame.image.load(image).convert()
        self.equippable = False
        self.consumable = not self.equippable

    def colorFix(self):
        transColor = self.image.get_at((1,1))
        self.image.set_colorkey(transColor)

    def consume(self, pInst):
        updatedHealth = pInst.health + self.healthRestored
        if updatedHealth > 100:
            pInst.health = 100
        else:
            pInst.health = updatedHealth 
