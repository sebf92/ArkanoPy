import pygame

class Bullet(pygame.sprite.Sprite):
	LEFT = 826
	TOP = 36
	WIDTH = 6
	HEIGHT=14

	spriteSheet = pygame.image.load("./levels/sprites/sprites.png")
	laserSound = None

	def __init__(self, playfield):
		pygame.sprite.Sprite.__init__(self)

		self.playfield = playfield
		self.numeroSequence = 0
		self.numeroImage = 0

		if(Bullet.laserSound==None):
			Bullet.laserSound = pygame.mixer.Sound("sounds/original/Arkanoid SFX (3).mp3")
			Bullet.laserSound.set_volume(0.5)

		self.rect = pygame.Rect(0,0,Bullet.WIDTH,Bullet.HEIGHT)
		self.image = Bullet.spriteSheet.subsurface(pygame.Rect(58*14+24,36*1,Bullet.WIDTH,Bullet.HEIGHT))
		self.mask = pygame.mask.from_surface(self.image)


	def update(self,time):
		# on monte la munition
		self.rect = self.rect.move(0,-10)
		if(self.rect.y<self.playfield.y): # la munitition est sortie de l'écran, on la fait disparaitre
			self.kill()


	def setPosition(self, x,y):
		self.rect = pygame.Rect(x,y,Bullet.WIDTH, Bullet.HEIGHT)

	def playSound(self):
		Bullet.laserSound.play()
