
import pygame,math

def collide_point_rect(sprite1, sprite2):
	'''
	Collider implementation of a Point and a Rectangle\n
	This method uses the Center of the first Rect and test it against the second Rect\n
	Returns True if the Point is inside the Rectangle
	'''
	sprite1x = sprite1.rect.centerx
	sprite1y = sprite1.rect.centery

	if(sprite1x<sprite2.rect.x):
		return False
	elif(sprite1x>sprite2.rect.topright[0]):
		return False
	elif(sprite1y<sprite2.rect.y):
		return False
	elif(sprite1y>sprite2.rect.bottomleft[1]):
		return False
	else:
		return True

def collide_circle_rect(sprite1, sprite2):
	'''
	Collider implementation of a Circle and a Rectangle\n
	This method consider the first sprite as a Circle and the second sprite as a Rectangle.\n
	In order to work properly, this method assumes that the property "radius" is defined in the first sprite and that the property rect is defined in the second sprite\n
	If no 'radius' is defined in the first sprite, a circle is created that is big enough to completely enclose the sprites rect as given by the “rect” attribute.\n
	Returns True if the Circle represented by sprite1.rect.center and sprite1.radius intersects the sprite2 Rectangle
	'''

	r = None # rayon du cercle
	if(hasattr(sprite1, 'radius')):
		r = sprite1.radius
	else:
		r = math.sqrt(sprite1.rect.w/2**2.0+sprite1.rect.h**2.0)
	centerx,centery = sprite1.rect.center # centre du cercle
	rect = sprite2.rect # le rectangle a tester

	circle_distance_x = abs(centerx-rect.centerx)
	circle_distance_y = abs(centery-rect.centery)
	if circle_distance_x > rect.w/2.0+r or circle_distance_y > rect.h/2.0+r:
		return False
	if circle_distance_x <= rect.w/2.0 or circle_distance_y <= rect.h/2.0:
		return True
	corner_x = circle_distance_x-rect.w/2.0
	corner_y = circle_distance_y-rect.h/2.0
	corner_distance_sq = corner_x**2.0 +corner_y**2.0
	return corner_distance_sq <= r**2.0