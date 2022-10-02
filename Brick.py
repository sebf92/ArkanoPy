import pygame

class Brick(pygame.sprite.Sprite):
	# les types de brique disponibles
	WHITE=0
	ORANGE=1
	CYAN=2
	GREEN=3
	SILVER=4
	SILVERBLINK=5
	SILVERINJURED=6
	RED=7
	BLUE=8
	MAGENTA=9
	YELLOW=10
	GOLD=11
	GOLDBLINK=12

	# la taille d'une brique
	WIDTH = 44
	HEIGHT=22

	# les briques
	spriteSheet = pygame.image.load("./levels/sprites/sprites.png")
	score = [50, 60, 70, 80, 0, 0, 50, 90, 100, 110, 120, 0, 0] # score when a brick is destroyed

	# matrice de 15*2 briques
	sequences = [(0,1,False),(1,1,False),(2,1,False),(3,1,False),(4,1,False),(4,10,True),(14,1,False),(15,1,False),(16,1,False),(17,1,False),(18,1,False),(19,1,False),(19,10,True)]

	breakSound = None
	goldSound = None

	def __init__(self,level=1):
		pygame.sprite.Sprite.__init__(self)

		self.level = level
		if(Brick.breakSound==None):
			Brick.breakSound = pygame.mixer.Sound("sounds/original/Arkanoid SFX (7).mp3")
			Brick.breakSound.set_volume(0.5)
			Brick.goldSound = pygame.mixer.Sound("sounds/original/Arkanoid SFX (8).mp3")
			Brick.goldSound.set_volume(0.5)

		self.numeroSequence = 0
		self.numeroImage = 0

		self.rect = pygame.Rect(0,0,Brick.WIDTH,Brick.HEIGHT)
		self.image = Brick.spriteSheet.subsurface(pygame.Rect(0,0,Brick.WIDTH,Brick.HEIGHT))
		self.mask = pygame.mask.from_surface(self.image)

		self.deltaTime = 0

		self.nblife = 1

	def update(self,time):
		# on calcule l'image à afficher
		n = Brick.sequences[self.numeroSequence][0]+self.numeroImage
		self.image = Brick.spriteSheet.subsurface(pygame.Rect(n%15*(42+16),n//15*(20+16),Brick.WIDTH,Brick.HEIGHT))

		self.deltaTime = self.deltaTime + time
		if self.deltaTime>=20:
			self.deltaTime = 0

			self.numeroImage = self.numeroImage+1
			
			if self.numeroImage == Brick.sequences[self.numeroSequence][1]:
				# traitement particulier pour les briques argentées et dorées
				if self.numeroSequence == Brick.SILVERBLINK:
					if(self.nblife>1):
						self.numeroSequence = Brick.SILVER
					else:
						self.numeroSequence = Brick.SILVERINJURED
					self.numeroImage = 0
				elif self.numeroSequence == Brick.GOLDBLINK:
					self.numeroSequence = Brick.GOLD
					self.numeroImage = 0
				else:
					# pour les autres on joue les animations si besoin
					if Brick.sequences[self.numeroSequence][2]:
						self.numeroImage = 0
					else:
						self.numeroImage = self.numeroImage-1

	# WHITE
	# ORANGE
	# CYAN
	# GREEN
	# SILVER
	# RED
	# BLUE
	# MAGENTA
	# YELLOW
	# GOLD
	def setBrickType(self,n):
		if(n<0 or n>=len(Brick.sequences)):
			return
		if self.nblife != n:
			self.numeroImage = 0
			self.numeroSequence = n
			self.image = Brick.spriteSheet.subsurface(pygame.Rect(n%15*(42+16),n//15*(20+16),Brick.WIDTH,Brick.HEIGHT))

			if(n==Brick.SILVER):
				self.nblife=2+self.level//8
			elif(n==Brick.GOLD):
				self.nblife=99999
			elif(n!=Brick.SILVERINJURED):
				self.nblife=1

	def isBreakable(self):
		return self.nblife<100

	def setPosition(self, x,y):
		self.rect = pygame.Rect(x,y,self.rect.width, self.rect.height)

	# returns true if dead
	def injured(self):
		self.playSound()
		self.nblife -= 1
		if(self.nblife==0):
			self.kill()
			return True

		if(self.numeroSequence == Brick.SILVER):
			self.numeroSequence = Brick.SILVERBLINK
			self.numeroImage = 0
		elif(self.numeroSequence == Brick.GOLD):
			self.numeroSequence = Brick.GOLDBLINK
			self.numeroImage = 0
		
		return False
	def destroy(self):
		self.playSound()
		self.nblife = 0
		self.kill()

	def getScore(self):
		if(self.numeroSequence==Brick.SILVERINJURED):
			return self.score[self.numeroSequence]*self.level # dans le cas d'une brique argentée le score est fonction du niveau
		else:
			return self.score[self.numeroSequence]

	def playSound(self):
		if self.numeroSequence in (Brick.SILVER, Brick.SILVERBLINK, Brick.SILVERINJURED, Brick.GOLD, Brick.GOLDBLINK):
			Brick.goldSound.play()
		else:
			Brick.breakSound.play()
