import pygame

class Life(pygame.sprite.Sprite):
	LEFT = 684
	TOP = 176
	WIDTH = 32
	HEIGHT=32

	spriteSheet = pygame.image.load("./levels/sprites/sprites.png")
	laserSound = None

	def __init__(self):
		pygame.sprite.Sprite.__init__(self)

		self.rect = pygame.Rect(0,0,Life.WIDTH,Life.HEIGHT)
		self.image = Life.spriteSheet.subsurface(pygame.Rect(Life.LEFT,Life.TOP,Life.WIDTH,Life.HEIGHT))
		self.mask = pygame.mask.from_surface(self.image)


	def update(self,time):
		nop = 1


	def setPosition(self, x,y):
		self.rect = pygame.Rect(x,y,Life.WIDTH, Life.HEIGHT)
