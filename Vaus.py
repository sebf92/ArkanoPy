import pygame, random

from Bonus import Bonus

def buildSprites(x, y=0, width=44):
	sprite = list()
	spritemask = list()

	for i in range(0,4):
		left = Vaus.spriteSheet.subsurface(pygame.Rect(x,y+i*22,width,22))
		right = pygame.transform.flip(left,True,False)
		image = pygame.Surface([width*2,22], pygame.SRCALPHA, 32)
		image = image.convert_alpha()
		image.blit(left,pygame.Rect(0,0,left.get_width(),left.get_height()))
		image.blit(right,pygame.Rect(width,0,right.get_width(),right.get_height()))
		mask = pygame.mask.from_surface(image)
		sprite.append(image)
		spritemask.append(mask)
	for i in range(3,-1,-1):
		sprite.append(sprite[i])
		spritemask.append(spritemask[i])

	return (sprite, spritemask)


class Vaus(pygame.sprite.Sprite):
	NORMALVAUS = 0
	CATCHVAUS = 1
	LASERVAUS = 2
	ENLARGEVAUS = 3
	REDUCEVAUS = 4
	SUPERLASERVAUS = 5

	YPOS = 30 #position de la raquette par rapport au bas du playfield

	# les briques
	spriteSheet = pygame.image.load("./levels/sprites/vaus.png")

	# liste de listes
	spritelist = None
	spritemasklist = None

	sprite = list()
	spritemask = list()

	bouncingSound = None

	def __init__(self, playfield):
		pygame.sprite.Sprite.__init__(self)

		# la taille de Vaus
		self.WIDTH = 88
		self.HEIGHT=22

		self.playfield = playfield
		if(Vaus.bouncingSound==None):
			Vaus.bouncingSound = pygame.mixer.Sound("sounds/original/Arkanoid SFX (6).mp3")
			Vaus.bouncingSound.set_volume(0.5)

		self.numeroImage = 0
		self.sequence = 0
		self.bonus = None

		# on charge toutes les animations
		if(Vaus.spritelist==None):
			Vaus.spritelist = list()
			Vaus.spritemasklist = list()
			(sprite,spritemask) = buildSprites(0) # vaisseau normal
			self.spritelist.append(sprite)
			self.spritemasklist.append(spritemask)

			(sprite,spritemask) = buildSprites(0) # vaisseau qui colle les balles
			self.spritelist.append(sprite)
			self.spritemasklist.append(spritemask)

			(sprite,spritemask) = buildSprites(44) # vaisseau armé
			self.spritelist.append(sprite)
			self.spritemasklist.append(spritemask)

			(sprite,spritemask) = buildSprites(0,88,66) # vaisseau élargi
			self.spritelist.append(sprite)
			self.spritemasklist.append(spritemask)

			(sprite,spritemask) = buildSprites(0,0,22) # vaisseau réduit
			self.spritelist.append(sprite)
			self.spritemasklist.append(spritemask)

			(sprite,spritemask) = buildSprites(300) # vaisseau super armé
			self.spritelist.append(sprite)
			self.spritemasklist.append(spritemask)

		# selectionne une animation
		self.sprite = self.spritelist[self.sequence]
		self.spritemask = self.spritemasklist[self.sequence]

		# on initialise des images par défaut
		self.image = self.sprite[0]
		self.mask = self.spritemask[0]

		self.rect = pygame.Rect((640/2)-(self.WIDTH/2),self.playfield.y+self.playfield.height-Vaus.YPOS,self.WIDTH,self.HEIGHT)

		self.deltaTime = 0

	def update(self,time):
		# selectionne une animation
		self.sprite = self.spritelist[self.sequence]
		self.spritemask = self.spritemasklist[self.sequence]

		self.image = self.sprite[self.numeroImage]
		self.mask = self.spritemask[self.numeroImage]

		newwidth = self.image.get_width()
		newheight = self.image.get_height()
		if(newwidth!=self.WIDTH):
			deltax = (self.WIDTH-newwidth)/2
			self.rect = pygame.Rect(self.rect.x, self.rect.y, newwidth, self.rect.height)
			self.rect = self.rect.move(deltax,0).clamp(self.playfield)
			self.WIDTH = newwidth
		if(newheight!=self.HEIGHT):
			deltay = (self.HEIGHT-newheight)/2
			self.rect = pygame.Rect(self.rect.x, self.rect.y, self.rect.width, newheight)
			self.rect = self.rect.move(0,deltay).clamp(self.playfield)
			self.HEIGHT = newheight

		self.deltaTime = self.deltaTime + time
		if self.deltaTime>=200:
			self.deltaTime = 0

			self.numeroImage += 1
			self.numeroImage = self.numeroImage%len(self.sprite)

	def setPosition(self, x,y):
		self.rect = pygame.Rect(x,y,self.rect.width, self.rect.height)

	def move(self, x):
		currentX = self.rect.x
		currentX += x
		if(currentX<self.playfield.x):
			currentX = self.playfield.x
		elif(currentX>self.playfield.x+self.playfield.w-self.WIDTH):
			currentX = self.playfield.x+self.playfield.w-self.WIDTH

		self.rect.x = currentX

	# on simule un effet d'arrondi sur les bords de la raquette
	def getBallEffect(self, ball):
		deltaStart = ball.getPosition().x+5-self.rect.x

		if(deltaStart<20):
			return (2*(20-deltaStart),'left')
		elif(deltaStart>self.rect.width-20):
			return (2*(deltaStart-(self.rect.width-20)), 'right')
		else:
			return (0,'')			

	def playBouncingSound(self):
		Vaus.bouncingSound.play()

	def setVausType(self, type):
		'''
		Vaus.NORMALVAUS
		Vaus.CATCHVAUS
		Vaus.LASERVAUS
		'''
		if(self.sequence!=type):
			self.sequence = type
			self.numeroImage = 0

	def getVausType(self):
		'''
		Vaus.NORMALVAUS
		Vaus.CATCHVAUS
		Vaus.LASERVAUS
		'''
		return self.sequence

	def setBonus(self, bonusType):
		'''
		Laser	Collect the red capsule to transform the Vaus into its Laser-firing configuration. In this form, you can fire lasers at the top of the screen by pushing the fire button. Lasers can be used against every brick except Gold bricks, and against enemies. Silver bricks can only be destroyed by lasers when they are hit the required number of times.\n
		Enlarge	Collect the blue capsule to extend the width of the Vaus.\n
		Catch	Collect the green capsule to gain the catch ability. When the ball hits the Vaus, it will stick to the surface. Press the Fire button to release the ball. The ball will automatically release after a certain period of time has passed.\n
		'''
		if(self.bonus!=bonusType):
			self.bonus = bonusType

			if(self.bonus==Bonus.LASER):
				self.setVausType(Vaus.LASERVAUS)
			elif(self.bonus==Bonus.CATCH):
				self.setVausType(Vaus.CATCHVAUS)
			elif(self.bonus==Bonus.ENLARGE):
				self.setVausType(Vaus.ENLARGEVAUS)
			elif(self.bonus==Bonus.REDUCE):
				self.setVausType(Vaus.REDUCEVAUS)
			else:
				self.setVausType(Vaus.NORMALVAUS)

