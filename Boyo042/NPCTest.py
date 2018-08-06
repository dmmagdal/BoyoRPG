import pygame
import time
import random
import MapLinks
import BoyoRPG
import PlayerTest
import random as rand


#Code to spawn/manage the NPCs (non-player and non-enemy in this case)
class NPC(object):

	def __init__(self, x, y, image, quest):
		self.x = x
		self.y = y
		self.image = image
		self.dialogue = []
		self.health = 1
		self.quest = quest

	def talk(self, pInst):
		#shopping = False
		#pygame.draw.rect(BoyoRPG.gameDisplay, BoyoRPG.blue, (100, 500, 600, 50))
		smallText = pygame.font.Font('freesansbold.ttf', 12)
		if len(self.dialogue) > 120:
			TextSurf, TextRect = BoyoRPG.text_objects(self.dialogue[:120], smallText, BoyoRPG.white)
			TextRect.center = (400, 500)
			TextSurf2, TextRect2 = BoyoRPG.text_objects(self.dialogue[120:], smallText, BoyoRPG.white)
			TextRect2.center = (400, 525)
			BoyoRPG.gameDisplay.blit(TextSurf, TextRect)
			BoyoRPG.gameDisplay.blit(TextSurf2, TextRect2)
		else:
			TextSurf, TextRect = BoyoRPG.text_objects(self.dialogue, smallText, BoyoRPG.white)
			TextRect.center = (400, 500)
			BoyoRPG.gameDisplay.blit(TextSurf, TextRect)

		'''
		if self.dialogue == " Welcome. What can I get for you?\n":
			#shopping = True
			x = pInst.x + pInst.x_vel/2
			y = pInst.y + pInst.y_vel/2
			futurePlayRect = pygame.Rect(x, y, 30, 35)
			if self.x + 30 - 1 <= futurePlayRect.left:
				#self.x_vel = 0 #stop x velocity
				#self.knockback = "left"
				pInst.x -= 5
			if self.x >= futurePlayRect.right - 1 :
				#self.x_vel = 0 #stop x velocity
				#self.knockback = "right"
				pInst.x += 5
			if self.y + 35 - 1 <= futurePlayRect.top:
				#self.y_vel = 0 #stop y velocity from the top
				#self.knockback = "top"
				pInst.y -= 5
			if self.y - 1 >= futurePlayRect.bottom - 1:
				#self.y_vel = 0 #stop y velocity from the bottom
				#self.knockback = "bottom"
				pInst.y -= 5
			#self.shop(pInst)
			print("Entering shop()")
			BoyoRPG.shop(pInst)
		'''


	def displayNPC(self):
		#pygame.draw.rect(BoyoRPG.gameDisplay, BoyoRPG.black, (self.x, self.y, 30, 35))
		transColor = self.image.get_at((1,1))
		self.image.set_colorkey(transColor)
		BoyoRPG.gameDisplay.blit(self.image, (self.x, self.y))


	def charCollision(self, pInst):
		x = pInst.x + pInst.x_vel/2
		y = pInst.y + pInst.y_vel/2
		futurePlayRect = pygame.Rect(x, y, 30, 35)
		x = self.x
		y = self.y
		futureEnemRect = pygame.Rect(x, y, 30, 35)
		if futurePlayRect.colliderect(futureEnemRect):
			self.talk(pInst)
			return True


	def rotateNPC(self):
		self.image = pygame.transform.flip(self.image, 1, 0)

	#def seek(self, playerx, playery):
	#	pass

	'''
	def exitShop(self):
		global shopping
		shopping = False


	def shop(self, pInst):
		pygame.draw.rect(BoyoRPG.gameDisplay, BoyoRPG.sand, (100, 25, 250, 50))
		pygame.draw.rect(BoyoRPG.gameDisplay, BoyoRPG.sand, (600, 25, 100, 50))
		mediumText = pygame.font.Font('freesansbold.ttf', 50)
		TextSurf, TextRect = BoyoRPG.text_objects("Inventory", mediumText, BoyoRPG.orangold)
		TextRect.center = (225, 75)
		TextSurf2, TextRect2 = BoyoRPG.text_objects("Shop", mediumText, BoyoRPG.orangold)
		TextRect2.center = (700, 75)
		BoyoRPG.gameDisplay.blit(TextSurf, TextRect)
		BoyoRPG.gameDisplay.blit(TextSurf2, TextRect2)

		shopChat = ["Nice choice", "No refunds", "That's a rare one"]

		global shopText
		shopText = rand.choice(shopChat)

		while True:
			# variables and their initializations
			store = pygame.image.load('png/shop.png')
			for item in pInst.invent:
				colorfix(item)
			PlayerArray = pInst.invent
			ShopInventory = self.initializeInventory()
			ShopPrice = [15, 20, 35, 75, 100, 30, 50,
						20, 65, 100, 25, 50]
			ShopArray = [ShopInventory, ShopPrice]

			shopStore = PlayerTest.World(0, 0, store)
			shopStore.displayWorld()
			# initialize buttons
			BoyoRPG.button_mm("Leave", 100, 500, 100, 50, BoyoRPG.gold, BoyoRPG.yellow, self.exitShop)

			# player inventory
			pygame.draw.rect(BoyoRPG.gameDisplay, BoyoRPG.sand, (30, 100, 350, 300))
			for i in range(len(PlayerArray)):
				if i < 5:
					BoyoRPG.gameDisplay.blit(PlayerArray[i].image.convert(), (30+(i*70), 100))
				elif i < 10 and i > 4:
					BoyoRPG.gameDisplay.blit(PlayerArray[i].image.convert(), (30+((i-5)*70), 175))
				elif i < 15 and i > 9:
					BoyoRPG.gameDisplay.blit(PlayerArray[i].image.convert(), (30+((i-10)*70), 250))
				else:
					BoyoRPG.gameDisplay.blit(PlayerArray[i].image.convert(), (30+((i-15)*70), 325))

			# shop inventory
			for j in range(12):
				if j < 4:
					BoyoRPG.button_mm("", 750-(j*70), 100, 70, 75, BoyoRPG.sand, BoyoRPG.orangold, self.addToInvent, pInst, j)
					BoyoRPG.gameDisplay.blit(ShopArray[0][j].image.convert(), (750-(j*70), 100))
				elif j < 8 and j > 3:
					BoyoRPG.button_mm("", 750-((j-4)*70), 175, 70, 75, BoyoRPG.sand, BoyoRPG.orangold, self.addToInvent, pInst, j)
					BoyoRPG.gameDisplay.blit(ShopArray[0][j].image.convert(), (750-((j-4)*70), 175))
				else:
					BoyoRPG.button_mm("", 750-((j-8)*70), 250, 70, 75, BoyoRPG.sand, BoyoRPG.orangold, self.addToInvent, pInst, j)
					BoyoRPG.gameDisplay.blit(ShopArray[0][j].image.convert(), (750-((j-8)*70), 250))

			pygame.display.update()


	def addToInvent(self, pInst, index):
		if len(ShopArray[0]) >= 20:
			# not enough space
			# print(Error message)
			shopText = "Not enough space"
		elif (pInst.gole - ShopArray[1][index]) < 0:
			# not enough money
			# print(Error message)
			shopText = "Not enough money"
		else:
			pInst.invent.append(ShopArray[0][index])
			pInst.gole = pInst.gole - ShopArray[1][index]


	def initializeInventory(self):
		sword1 = PlayerTest.Weapon(5, 'weapons/sword1.png')
		sword2 = PlayerTest.Weapon(6, 'weapons/sword2.png')
		sword3 = PlayerTest.Weapon(7, 'weapons/sword3.png')
		sword4 = PlayerTest.Weapon(8, 'weapons/sword4.png')
		sword5 = PlayerTest.Weapon(9, 'weapons/sword5.png')
		shield1 = PlayerTest.Armor(5,'weapons/shield1.png')
		shield2 = PlayerTest.Armor(7,'weapons/shield2.png')
		shield3 = PlayerTest.Armor(9,'weapons/shield3.png')
		axe = PlayerTest.Weapon(6, 'weapons/axe.png')
		mace = PlayerTest.Weapon(7, 'weapons/mace.png')
		potion1 = PlayerTest.Potion(25, 'weapons/potion1.png')
		potion2 = PlayerTest.Potion(100, 'weapons/potion2.png')
		inventory = [sword1, sword2, sword3, sword4, sword5,
					axe, mace, shield1, shield2, shield3,
					potion1, potion2]
		for item in inventory:
			BoyoRPG.colorFix(item)
		return inventory
	'''
