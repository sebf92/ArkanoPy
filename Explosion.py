import pygame, math, random

class Explosion(pygame.sprite.Sprite):

	playfield = pygame.Rect((0,0),(0,0))

	spriteSheet = pygame.image.load("./levels/sprites/explosion.png")
#	explosionsound = None
	sequences = [(0,64,True, True)]

	# Constructeur de la classe
	# FPS: le nombre d'images par secondes (pour les animations)
	def __init__(self, FPS, initialsprite = None):
		pygame.sprite.Sprite.__init__(self)

		self.spriteSheet.convert_alpha()

#		if(Explosion.explosionsound==None):
#			Explosion.explosionsound = pygame.mixer.Sound("sounds/explosion.mp3")
#			Explosion.explosionsound.set_volume(0.5)
		self.image = Explosion.spriteSheet.subsurface(pygame.Rect(0,0,44,44))

		self.rect = pygame.Rect(0,0,44,44)
		self.rect.bottom = 44
		if(initialsprite!=None):
			x = initialsprite.rect.x+initialsprite.rect.width/2
			y = initialsprite.rect.y+initialsprite.rect.height/2
			positionennemi = pygame.Rect(x,y,initialsprite.rect.width, initialsprite.rect.height)
			self.setPositionCenter(positionennemi.x, positionennemi.y)

		self.numeroSequence = 0
		self.numeroImage = 0

		self.deltaTime = 0

		self.FPS = FPS

	def update(self,time):
		self.deltaTime = self.deltaTime + time
		

		if self.deltaTime>=1000/self.FPS:
			self.deltaTime = 0

			# on calcule l'image à afficher
			n = Explosion.sequences[self.numeroSequence][0]+self.numeroImage
			self.image = Explosion.spriteSheet.subsurface(pygame.Rect(n%8*44,n//8*44,44,44))
			
			self.numeroImage = self.numeroImage+1
			
			if self.numeroImage == Explosion.sequences[self.numeroSequence][1]:
				if Explosion.sequences[self.numeroSequence][3]:
					self.kill()
				if Explosion.sequences[self.numeroSequence][2]:
					self.numeroImage = 0
				else:
					self.numeroImage = self.numeroImage-1
	
	def setPosition(self, x, y):
		self.rect = pygame.Rect(x,y,44,44)

	def setPositionCenter(self, x, y):
		self.rect = pygame.Rect(x-44/2,y-44/2,44,44)

	def getPosition(self):
		return self.rect

	def getPositionCenter(self):
		x = self.rect.x+self.rect.width/2
		y = self.rect.y+self.rect.height/2
		return pygame.Rect(x,y,self.rect.width, self.rect.height)

	def playSound(self):
		return
		#Explosion.explosionsound.play()
