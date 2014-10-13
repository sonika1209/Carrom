import pygame, sys, os, random
from pygame.locals import *
import time, pdb
import math
from carrom import *

boardBoundary = pygame.Color(143,100,55)
boardColor = pygame.Color(211,184,141)
holeColor = pygame.Color(0,0,0)
redColor = pygame.Color(255,0,0)
whiteColor = pygame.Color(255,255,255)
blueColor = pygame.Color(0,0,255)
strikerRad = 40
strikerVelx = 0
strikerVely = 0
screen_width = 700
screen_height = 700
boundary_width = 40
friction = 0.1

screen_width=700
screen_height=700
boundary_width=40
hole_rad=25
red_rad=15
rect_width=30
arc_rad=50
arcx=210
arcy=440

class Striker(pygame.sprite.Sprite):
	def __init__(self,board, player=False):
		pygame.sprite.Sprite.__init__(self)
		self.draw()
		self.velx = strikerVelx
		self.vely = strikerVely
		self.have_collided = False
		self.state = 0

	def draw(self):
		self.image = pygame.Surface([strikerRad,strikerRad])
		self.image.fill(boardColor)
		self.image.set_colorkey(boardColor)
		r=0
		g=0
		b=255
		for i in range(strikerRad/2, strikerRad/15, -1):
			pygame.draw.circle(self.image,pygame.Color(r, g, b),(strikerRad/2,strikerRad/2),i,0)
			b = b-10
		# pygame.draw.circle(self.image,blueColor,(strikerRad/2,strikerRad/2),strikerRad/2,0)
		pygame.draw.circle(self.image,blueColor,(strikerRad/2,strikerRad/2),strikerRad/2,2)
		self.rect = self.image.get_rect()
		self.radius = strikerRad/2
		

	def update_striker(self):
		if(abs(self.velx)<0.5*friction):
			self.velx = 0
		else:
			self.velx = self.velx - (friction*self.velx)/math.sqrt((self.velx*self.velx)+(friction*self.velx*friction*self.velx))
		
		if(abs(self.vely)<0.5*friction):
			self.vely = 0
		else:
			self.vely = self.vely - (friction*self.vely)/math.sqrt((self.vely*self.vely)+(friction*self.vely*friction*self.vely))
		
		self.rect.x = self.rect.x + self.velx 
		self.rect.y = self.rect.y + self.vely
		
		if(self.rect.x > screen_width-boundary_width -strikerRad):
			self.velx = -1*self.velx
			self.rect.x = screen_width-boundary_width-strikerRad
		if(self.rect.x < boundary_width):
			self.velx = -1*self.velx
			self.rect.x = boundary_width
		if(self.rect.y > screen_width-boundary_width -strikerRad):
			self.vely = -1*self.vely
			self.rect.y = screen_width-boundary_width-strikerRad
		if(self.rect.y < boundary_width):
			self.vely = -1*self.vely
			self.rect.y = boundary_width
	
	def strikepos(self,player):
		pos = pygame.mouse.get_pos()	
		if(player == 0):
			self.rect.x = boundary_width+screen_width/6
			self.rect.y = (5*screen_width)/6 - rect_width - strikerRad/8
			if (pos[0]<((5*screen_width)/6 - boundary_width) and pos[0]>(boundary_width+screen_width/6)):
				self.rect.centerx = pos[0]
			elif (pos[0]>=((5*screen_width)/6 - boundary_width - red_rad)):
				self.rect.centerx = (5*screen_width)/6 - boundary_width
			else:
				self.rect.centerx = boundary_width+screen_width/6
		if(player == 1):
			self.rect.x = (5*screen_width)/6 - rect_width - strikerRad/8
			self.rect.y = boundary_width+screen_width/6
			if (pos[1]<((5*screen_width)/6 - boundary_width) and pos[1]>(boundary_width+screen_width/6)):
				self.rect.centery = pos[1]
			elif (pos[1]>=((5*screen_width)/6 - boundary_width - red_rad)):
				self.rect.centery = (5*screen_width)/6 - boundary_width
			else:
				self.rect.centery = boundary_width+screen_width/6

		if(player == 2):
			self.rect.x = boundary_width+screen_width/6 
			self.rect.y = screen_width/6 - strikerRad/8
			if (pos[0]<((5*screen_width)/6 - boundary_width) and pos[0]>(boundary_width+screen_width/6)):
				self.rect.centerx = pos[0]
			elif (pos[0]>=((5*screen_width)/6 - boundary_width - red_rad)):
				self.rect.centerx = (5*screen_width)/6 - boundary_width
			else:
				self.rect.centerx = boundary_width+screen_width/6

		if(player == 3):
			self.rect.x = screen_width/6 - strikerRad/8
			self.rect.y = boundary_width+screen_width/6 
			if (pos[1]<((5*screen_width)/6 - boundary_width) and pos[1]>(boundary_width+screen_width/6)):
				self.rect.centery = pos[1]
			elif (pos[1]>=((5*screen_width)/6 - boundary_width - red_rad)):
				self.rect.centery = (5*screen_width)/6 - boundary_width
			else:
				self.rect.centery = boundary_width+screen_width/6

