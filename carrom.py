import pygame, sys, os, random
from pygame.locals import *
import time, pdb
from striker import *
from coin import *
import math

boardBoundary = pygame.Color(92,51,25)
boardColor = pygame.Color(211,195,141)
holeColor = pygame.Color(0,0,0)
redColor = pygame.Color(255,0,0)
greenColor = pygame.Color(0, 255, 0)

actual_width = 1200
screen_width=700
wid = actual_width - screen_width
screen_height=700
boundary_width=40
hole_rad=25
red_rad=15
rect_width=30
arc_rad=50
arcx=210
arcy=440
mod = lambda v: math.sqrt(v[0] * v[0] + v[1] * v[1])

friction = 0.1
all_sprite_list = pygame.sprite.Group()
all_coin_list = pygame.sprite.Group()

pygame.font.init()
font = pygame.font.SysFont("", 35)
font1 = pygame.font.SysFont("", 30)
font2 = pygame.font.SysFont("", 50)
# class Player(self):
# 	def __init__(self):

class Player():
	def __init__(self,ID,name=None):
		self.score = 0
		self.name =  name if name is not None else 'Player '+str(ID+1)
		self.is_active = False
		self.ID = ID
		self.black = 0
		self.white = 0
						
class Carrom():
	def __init__(self,width=actual_width,height=screen_height,caption='Carrom Board',coin_num = 19,nplayers=4):
		pygame.init()
		self.width, self.height = width, height
		self.coin_num = coin_num
		self.carromBoard = pygame.display.set_mode((self.width, self.height))
		pygame.display.set_caption(caption)	
		self.striker = Striker(self.carromBoard)
		self.nplayers = nplayers
		self.player = [0]*nplayers
		for i in range (0,self.nplayers):
			self.player[i] = Player(i)
		self.active_player = self.player[0]
		self.striker.strikepos(0)
		self.player[0].is_active = True
		self.change = True
		self.turn = 0
		self.change2 = 0
		self.displayed = False
		self.queen_state = False
		self.black = 9
		self.white = 9
		self.striked = False
		self.coins = [0]*coin_num
		for i in range (0,coin_num):
			if i==0:
				curr = True
			else:
				curr = False
			if i%2 == 0:
				temp = True
			else:
				temp = False
			self.coins[i] = Coin(self.carromBoard,temp,curr)
			self.coins[i].position(i)
			all_coin_list.add(self.coins[i])
			all_sprite_list.add(self.coins[i])
		all_sprite_list.add(self.striker)
		self.run()
	def run(self):
		self.drawBoard(self.carromBoard)
		for event in pygame.event.get():
			if event.type==pygame.QUIT:
				pygame.quit()
				sys.exit()
			if self.striker.state == 3:
				pos = pygame.mouse.get_pos()
				pygame.draw.line(self.carromBoard, pygame.Color(0, 255, 0), (self.striker.rect.centerx,self.striker.rect.centery),(pygame.mouse.get_pos()),5)
				self.striker.velx = (pos[0]-self.striker.rect.centerx)*0.2*(-1)
				self.striker.vely = (pos[1]-self.striker.rect.centery)*0.2*(-1)
				self.striker.state = 0
				self.turn = 1
			if event.type == MOUSEBUTTONDOWN and self.striker.state == 2:
				self.striker.state = 3			
			if self.striker.state == 2:
				pygame.draw.line(self.carromBoard, pygame.Color(0, 255, 0), (self.striker.rect.centerx,self.striker.rect.centery),(pygame.mouse.get_pos()),5)	
			if event.type == MOUSEBUTTONDOWN and self.striker.state == 1:
				self.striker.state = 2				
			if self.striker.state == 1:
				if(self.change ==True and self.turn==1):
					self.active_player.is_active = False
					self.player[(self.active_player.ID+1)%4].is_active = True
					self.active_player = self.player[(self.active_player.ID+1)%4]
				if(self.change2 == 1 and self.turn == 1 and self.change == False):
					self.active_player.score +=50
					self.change2 = 0
				if(self.change2 == 1 and self.turn == 1 and self.change == True):
					all_sprite_list.add(self.coins[0])
					self.coins[0].position(0)
					self.change2 = 0
					# self.coins[0].rect.y = screen_height/2-coinRad/2
				if(self.change == False and self.queen_state == True and self.turn==1):
					self.change2 = 1
				if(self.change == False and self.queen_state == True and self.turn == 1 and self.striked == True):
					self.active_player.score += 50
					self.change2 = 0
				self.striked = False
				self.queen_state = False
				self.striker.strikepos(self.active_player.ID)
				self.change=True
				if self.turn ==1 and not self.displayed:
					self.score_display()
					self.displayed = True
				self.turn = 0
				self.displayed = False
			if event.type == MOUSEBUTTONDOWN and self.striker.state == 0:
				self.striker.state = 1

		all_sprite_list.draw(self.carromBoard)
		for disk in all_sprite_list:
			self.goToHoles(disk)
		for disk1 in all_sprite_list:
		 	for disk2 in all_sprite_list:
		 		if disk1 != disk2 and (not disk1.have_collided or not disk2.have_collided):
		 			self.collide_coin(disk1,disk2)
		self.striker.update_striker()
		for i in range (0,self.coin_num):
			self.coins[i].update_coin()
		for disk1 in all_sprite_list:
			disk1.have_collided = False
		pygame.display.update()
		return True
	def collide_coin(self,disk1,disk2):
		if pygame.sprite.collide_circle(disk1, disk2):
			if self.striker.state == 0:
				disk2.have_collided = True
			 	disk1.have_collided = True
				c1x = disk1.rect.centerx
				c1y = disk1.rect.centery
				c2x = disk2.rect.centerx
				c2y = disk2.rect.centery
				c1 = [disk1.rect.x+coinRad, disk1.rect.y+coinRad]
				c2 = [disk2.rect.x+coinRad, disk2.rect.y+coinRad]
				distx = (c2[0]-c1[0])
				disty = (c1[1]-c2[1])
				dist = [(c2[0]-c1[0]), (c1[1]-c2[1])]
				if dist[1]==0:
					costheta = 1
					sintheta = 0
				elif dist[0]==0:
					costheta = 0
					sintheta = 1
				if mod(dist)>0:
					costheta = abs(distx)/mod(dist)
					sintheta = abs(disty)/mod(dist)
				if mod(dist)<coinRad + coinRad:
					diff = coinRad + coinRad - mod(dist)
					if disk2.rect.x>=disk1.rect.x:
						disk2.rect.x += math.ceil(diff*costheta)
					else:
						disk1.rect.x += math.ceil(diff*costheta)
					if disk2.rect.y>disk1.rect.y:
						disk2.rect.y += math.ceil(diff*costheta)
					else:
						disk1.rect.y += math.ceil(diff*costheta)
				if c1x != c2x:
					m = (c2y-c1y)/(c2x-c1x)
					tempx1=(((disk2.velx)*(m*m))-(disk1.vely*m)+disk1.velx+(disk2.vely*m))/((m*m)+1)
					tempx2=(((disk1.velx)*(m*m))-(disk2.vely*m)+(disk2.velx)+(disk1.vely*m))/((m*m)+1)
					tempy1=((disk2.velx*m)+(disk1.vely*(m*m))-(disk1.velx*m)+disk2.vely)/((m*m)+1)
					tempy2=((disk1.velx*m)+(disk2.vely*(m*m))-(disk2.velx*m)+disk1.vely)/((m*m)+1)
					disk1.velx = tempx1
					disk1.vely = tempy1
					disk2.velx = tempx2
					disk2.vely = tempy2
					soundObj1 = pygame.mixer.Sound('coinhit.ogg')
					soundObj1.play(loops=0, maxtime=75)
				else:
					tempy1 = disk1.vely
					disk1.vely = disk2.vely
					disk2.vely = tempy1
			elif self.striker.state != 0:
				if disk1 == self.striker or disk2 == self.striker:
					# self.striker.state = 0
					self.Foul_display()
					# time.sleep(0.3)


	def drawBoard(self, board):
		self.score_display2()

		# for boundary and boundary lines
		
		i=0
		r=51
		g=25
		b=0
		for i in range(0, boundary_width):
			# boardBoundary = pygame.Color(r,g,b)
			pygame.draw.rect(board, pygame.Color(r, g, b), (i,i,screen_width-(2*i),i) )
			pygame.draw.rect(board, pygame.Color(r, g, b), (i,i,i,screen_height-(2*i)) )
			pygame.draw.rect(board, pygame.Color(r, g, b), (screen_width-(2*i),i,i,screen_height-(2*i)))
			pygame.draw.rect(board, pygame.Color(r, g, b), (i,screen_height-(2*i),screen_width-(2*i),i))
			r = r+2
			g = g+1

		# for main board on which game is played
		pygame.draw.rect(board, boardColor, (boundary_width,boundary_width,screen_width-(2*boundary_width),screen_width-(2*boundary_width)))

		# for the four holes which are coins final destination
		pygame.draw.circle(board, holeColor, (boundary_width+hole_rad-hole_rad/2,boundary_width+hole_rad-hole_rad/2),hole_rad,0)
		pygame.draw.circle(board, holeColor, (boundary_width+hole_rad-hole_rad/2,screen_width-boundary_width-hole_rad+hole_rad/2),hole_rad,0)
		pygame.draw.circle(board, holeColor, (screen_width-boundary_width-hole_rad+hole_rad/2,boundary_width+hole_rad-hole_rad/2),hole_rad,0)
		pygame.draw.circle(board, holeColor, (screen_width-boundary_width-hole_rad+hole_rad/2,screen_width-boundary_width-hole_rad+hole_rad/2),hole_rad,0)

		# for the circles which is the starting point of the coins
		pygame.draw.circle(board, holeColor, (screen_width/2,screen_width/2),screen_width/10,2)
		pygame.draw.circle(board, holeColor, (screen_width/2,screen_width/2),screen_width/15,2)

		# for the four places from which the player plays the game
		pygame.draw.rect(board, holeColor, (boundary_width+screen_width/6,screen_width/6,screen_width-(2*boundary_width+2*screen_width/6),rect_width), 2)
		pygame.draw.circle(board, redColor, (boundary_width+screen_width/6,screen_width/6 + red_rad), red_rad,0)
		pygame.draw.circle(board, holeColor, (boundary_width+screen_width/6,screen_width/6 + red_rad), red_rad,2)
		pygame.draw.circle(board, redColor, ((5*screen_width)/6 - boundary_width,screen_width/6 + red_rad), red_rad,0)
		pygame.draw.circle(board, holeColor, ((5*screen_width)/6 - boundary_width,screen_width/6 + red_rad), red_rad,2)

		pygame.draw.rect(board, holeColor, (screen_width/6,boundary_width+screen_width/6,rect_width,screen_width-(2*boundary_width+2*screen_width/6)), 2)
		pygame.draw.circle(board, redColor, (screen_width/6 + red_rad,boundary_width+screen_width/6), red_rad,0)
		pygame.draw.circle(board, holeColor, (screen_width/6 + red_rad,boundary_width+screen_width/6), red_rad,2)
		pygame.draw.circle(board, redColor, (screen_width/6 + red_rad,(5*screen_width)/6 - boundary_width), red_rad,0)
		pygame.draw.circle(board, holeColor, (screen_width/6 + red_rad,(5*screen_width)/6 - boundary_width), red_rad,2)

		pygame.draw.rect(board, holeColor, (boundary_width+screen_width/6,(5*screen_width)/6 -rect_width,screen_width-(2*boundary_width+2*screen_width/6),rect_width), 2)
		pygame.draw.circle(board, redColor, (boundary_width+screen_width/6,(5*screen_width)/6 - red_rad), red_rad,0)
		pygame.draw.circle(board, holeColor, (boundary_width+screen_width/6,(5*screen_width)/6 - red_rad), red_rad,2)
		pygame.draw.circle(board, redColor, ((5*screen_width)/6 - boundary_width,(5*screen_width)/6 - red_rad), red_rad,0)
		pygame.draw.circle(board, holeColor, ((5*screen_width)/6 - boundary_width,(5*screen_width)/6 - red_rad), red_rad,2)

		pygame.draw.rect(board, holeColor, ((5*screen_width)/6 -rect_width,boundary_width+screen_width/6,rect_width,screen_width-(2*boundary_width+2*screen_width/6)), 2)
		pygame.draw.circle(board, redColor, ((5*screen_width)/6 - red_rad,boundary_width+screen_width/6), red_rad,0)
		pygame.draw.circle(board, holeColor, ((5*screen_width)/6 - red_rad,boundary_width+screen_width/6), red_rad,2)
		pygame.draw.circle(board, redColor, ((5*screen_width)/6 - red_rad,(5*screen_width)/6 - boundary_width), red_rad,0)
		pygame.draw.circle(board, holeColor, ((5*screen_width)/6 - red_rad,(5*screen_width)/6 - boundary_width), red_rad,2)

		# for the four diagonal design

		pygame.draw.line(board, holeColor, ((7*screen_width/6)/10,(7*screen_width/6)/10), (screen_width/3,screen_width/3), 2)
		pygame.draw.arc(board, holeColor, (arcx,arcx,arc_rad,arc_rad), 0, 6.28,2 )

		pygame.draw.line(board, holeColor, ((7*screen_width/6)/10,screen_width-(7*screen_width/6)/10), (screen_width/3,(2*screen_width)/3), 2)
		pygame.draw.arc(board, holeColor, (arcx,arcy,arc_rad,arc_rad), 0, 6.28,2 )

		pygame.draw.line(board, holeColor, (screen_width-(7*screen_width/6)/10,screen_width-(7*screen_width/6)/10), ((2*screen_width)/3,(2*screen_width)/3), 2)
		pygame.draw.arc(board, holeColor, (arcy,arcy,arc_rad,arc_rad), 0, 6.28,2 )

		pygame.draw.line(board, holeColor, (screen_width-(7*screen_width/6)/10,(7*screen_width/6)/10), ((2*screen_width)/3,screen_width/3), 2)
		pygame.draw.arc(board, holeColor, (arcy,arcx,arc_rad,arc_rad), 0, 6.28,2 )
	def goToHoles(self,disk):
		if((disk.rect.centerx <= boundary_width+hole_rad and disk.rect.centery<=boundary_width+hole_rad) or (disk.rect.centerx >= screen_width-boundary_width-hole_rad and disk.rect.centery<=boundary_width+hole_rad) or (disk.rect.centerx >= screen_width-boundary_width-hole_rad and disk.rect.centery>=screen_width-boundary_width-hole_rad) or (disk.rect.centerx <= boundary_width+hole_rad and disk.rect.centery>=screen_width-boundary_width-hole_rad)) :
			soundObj = pygame.mixer.Sound('pocket.wav')
			soundObj.play()
			# time.sleep(0.3) # wait and let the sound play for 1 second
			# soundObj.stop()
			if disk != self.striker:
				all_sprite_list.remove(disk)
				all_coin_list.remove(disk)
				self.change = False
				if(disk.is_queen == False and disk.is_white== False):
					self.active_player.score += 10
					self.active_player.black +=1
					self.striked = True
					self.black -=1
				elif(disk.is_queen == False):
					self.active_player.score += 20
					self.active_player.white +=1
					self.white -=1
					self.striked = True
				else:
					self.queen_state = True
				if self.black == 0 and self.white == 0 and self.queen_state == False:
					for i in range (0,self.active_player.white):
						self.new_coin = Coin(self.carromBoard,True)
						self.new_coin.rect.x = screen_width/2-coinRad/2
						self.new_coin.rect.y = screen_height/2-coinRad/2 
						all_sprite_list.add(self.new_coin)
					for i in range (0,self.active_player.black):
						self.new_coin = Coin(self.carromBoard)
						self.new_coin.rect.x = screen_width/2-coinRad/2
						self.new_coin.rect.y = screen_height/2-coinRad/2 
						all_sprite_list.add(self.new_coin)
					self.active_player.score = 0
					self.change = True
				if self.black == 0 and self.white ==0 and self.queen_state == True:
					self.game_over_display()
			else:
				self.change = True
				if self.active_player.score >=10 :
					if self.active_player.black >0:
						self.active_player.score -= 10
						self.active_player.black -= 1
						self.black +=1
						self.new_coin = Coin(self.carromBoard)
						self.new_coin.rect.x = screen_width/2-coinRad/2
						self.new_coin.rect.y = screen_height/2-coinRad/2 
						all_sprite_list.add(self.new_coin)
					elif self.active_player.white >0:
						self.active_player.score -= 20
						self.active_player.white -= 1
						self.white +=1
						self.new_coin = Coin(self.carromBoard,True,False)
						self.new_coin.rect.x = screen_width/2-coinRad/2
						self.new_coin.rect.y = screen_height/2-coinRad/2 
						all_sprite_list.add(self.new_coin)
				self.active_player.is_active = False
				self.player[(self.active_player.ID+1)%4].is_active = True
				self.active_player = self.player[(self.active_player.ID+1)%4]
				self.striker.strikepos(self.active_player.ID)
				self.striker.velx=0
				self.striker.vely=0
				self.score_display()
				self.displayed = False
				self.turn = 0
	def score_display(self):
		print 'Player ID\tScore\tStatus'
		underline = lambda s: '='*len(s)
		print underline('Player ID')+'\t'+underline('Score')+'\t'+underline('Status')
		for plyer in self.player:
			status = '* Active' if plyer.is_active else 'Idle'
			print '%s\t%s\t'%(plyer.name,plyer.score) + status
	def score_display2(self):
		pygame.draw.rect(self.carromBoard, (50,50,50), [screen_width,0,wid,screen_height])
		header = font2.render("Score Board", 5, (217, 84, 57))
		self.carromBoard.blit(header,(850,20))
		p1_scores = self.player[0].score
		p1_score = font.render("Player 1 :  " + str(p1_scores), 5, (217, 84, 57))
		self.carromBoard.blit(p1_score,(885,70))
		p2_scores = self.player[1].score
		p2_score = font.render("Player 2 :  " + str(p2_scores), 5, (217, 84, 57))
		self.carromBoard.blit(p2_score,(885,120))
		p3_scores = self.player[2].score
		p3_score = font.render("Player 3 :  " + str(p3_scores), 5, (217, 84, 57))
		self.carromBoard.blit(p3_score,(885,170))
		p4_scores = self.player[3].score
		p4_score = font.render("Player 4 :  " + str(p4_scores), 5, (217, 84, 57))
		self.carromBoard.blit(p4_score,(885,220))
		insHead = font2.render("Instructions", 5, (217, 84, 57))
		self.carromBoard.blit(insHead,(850,280))
		insHead1 = font1.render(" 1. Press Left Mouse Button to decide the position", 5, (217, 84, 57))
		insHead2 = font1.render("     of the striker.", 5, (217, 84, 57))
		self.carromBoard.blit(insHead1,(700,340))
		self.carromBoard.blit(insHead2,(700,365))
		insHead3 = font1.render(" 2. Press it again to fix the striker.", 5, (217, 84, 57))
		self.carromBoard.blit(insHead3,(700,395))
		insHead4 = font1.render(" 3. Press it the third time to impart power to the", 5, (217, 84, 57))
		insHead5 = font1.render("     striker.", 5, (217, 84, 57))
		self.carromBoard.blit(insHead4,(700,425))
		self.carromBoard.blit(insHead5,(700,450))
		insHead6 = font1.render(" 4. Press it the fourth time to shoot the striker.", 5, (217, 84, 57))
		self.carromBoard.blit(insHead6,(700,480))
	def Foul_display(self):
		header = font.render("Wrong Move",5,(217, 84, 57))
		self.carromBoard.blit(header,(280,330))
	def game_over_display(self):
		header = font.render("Game Over",5,(217, 84, 57))
		self.carromBoard.blit(header,(280,330))
		won = self.player[0]
		for i in range (1,4):
			if self.player[i].score > won.score:
				won = self.player[i]
		won_player = won.ID
		header2 = font.render("Player " + str(won_player),5,(217, 84, 57) )
		self.carromBoard.blit(header2,(280,360))


def main():
    game = Carrom()
    while game.run():
        pass

if __name__ == '__main__':
	main()
# fpsClock.tick(30)