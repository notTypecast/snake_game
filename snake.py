#!/usr/bin/env python2
import pygame
from pygame.locals import *
from random import randint, choice
from math import sin, cos


#Notes:
# --> user score is calculated using len(tail) - 4, since the tail's initial length is 4 but score starts from 0

# --> points awarded per apple are calculated as follows:
# red: sin of score * 10, rounded
# blue: cos of score * 10, rounded
# green: sin of score * cos of score * 10, rounded

class Run(object):
	#Game methods

	#disables powerup states
	def GAME_disable_powerup(self):

		self.combo_powerup = 0



		self.STATE_powerup = False

		self.speed = 5

		self.self_death = True

		self.point_multiplier = 1

		self.snake_color = (255, 255, 255)

		self.powerup_timer_text = None

		self.combo_text = None

		#reset powerup activation variables

		self.powerup_sequence = [choice(self.rgb_colors.keys()), choice(self.rgb_colors.keys()), choice(self.rgb_colors.keys())]

		self.powerup_history = []



	#activates powerup state
	def GAME_activate_powerup(self):

		#add 1 to combo multiplier
		self.combo_powerup += 1


		self.powerup_start_time = pygame.time.get_ticks() / 1000

		self.STATE_powerup = True
		
		self.speed += (2 * self.combo_powerup)

		self.self_death = False

		self.point_multiplier = (1.2 * self.combo_powerup)

		self.snake_color = (randint(30, 255), randint(0, 255), randint(30, 255))

		#preparation for combo powerup

		self.powerup_sequence = [choice(self.rgb_colors.keys()), choice(self.rgb_colors.keys()), choice(self.rgb_colors.keys())]






	#Execution methods
	def __init__(self):

		##Basic execution variables
		self._running = True
		self._display_surf = None
		self.size = self.length, self.height = 1220, 820
		self.clock = pygame.time.Clock()
		pygame.font.init()
		self.myfont = pygame.font.SysFont('Comic Sans MS', 30)

		self.UI = pygame.image.load('assets/UI.png')
		self.UI.set_alpha(122)

		self.tick = pygame.image.load('assets/tick.png')

		##Game variables

		#pos variables correspond to head
		self.x_pos = 600
		self.y_pos = 400

		self.speed = 5
		self.movement_direction = 'right'

		self.tail = [[590, 400], [580, 400], [570, 400], [560, 400]]

		self.apple_pos = [randint(10, self.length - 10), randint(25, self.height - 10)]
		self.blue_apple_pos = [randint(10, self.length - 10), randint(25, self.height - 10)]
		self.green_apple_pos = [randint(10, self.length - 10), randint(25, self.height - 10)]

		self.snake_color = (255, 255, 255)

		#powerup state check variables
		self.rgb_colors = {'r' : (255, 0, 0,), 'g' : (0, 255, 0,), 'b' : (0, 0, 255,)}
		self.powerup_sequence = [choice(self.rgb_colors.keys()), choice(self.rgb_colors.keys()), choice(self.rgb_colors.keys())]
		self.pickup_history = []

		#powerup state variables
		self.STATE_powerup = False
		self.combo_powerup = 0
		self.powerup_start_time = None
		self.colorchange_rate_sign = '+'

		#Feature variables // Decide whether a game feature is enabled or disabled
		self.self_death = True #die when touching own tail
		self.point_multiplier = 1

		#text on screen
		self.defeat_text = None
		self.powerup_timer_text = None
		self.combo_text = None
 
	def on_init(self):
		pygame.init()
		self._display_surf = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
		self._running = True
 
	def on_event(self, event):
		if event.type == pygame.QUIT:
			self._running = False

		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_LEFT:
				if self.movement_direction != 'right':
					self.movement_direction = 'left'

			elif event.key == pygame.K_RIGHT:
				if self.movement_direction != 'left':
					self.movement_direction = 'right'

			elif event.key == pygame.K_UP:
				if self.movement_direction != 'down':
					self.movement_direction = 'up'

			elif event.key == pygame.K_DOWN:
				if self.movement_direction != 'up':
					self.movement_direction = 'down'

	def on_loop(self):

		#make position of each piece equal to that of the one in front of it (position of first piece = previous position of head, also remove position of last piece)
		new_tail = [[self.x_pos, self.y_pos]]
		for piece_pos in self.tail[:len(self.tail) - 1]:
			new_tail.append(piece_pos)

		self.tail = list(new_tail)

		#move the head to its new position
		if self.movement_direction == 'right':
			self.x_pos += self.speed
		elif self.movement_direction == 'left':
			self.x_pos -= self.speed
		elif self.movement_direction == 'up':
			self.y_pos -= self.speed
		elif self.movement_direction == 'down':
			self.y_pos += self.speed

		#check if user ate an apple
		if (self.apple_pos[0] - 10 <= self.x_pos <= self.apple_pos[0] + 10) and (self.apple_pos[1] - 10 <= self.y_pos <= self.apple_pos[1] + 10):

			points_awarded = int(round( int( round( (abs(sin( len(self.tail) - 4)) * 10 ) ) ) * self.point_multiplier ))

			for _ in (xrange(points_awarded) if points_awarded else [1]):
				self.tail.append(self.tail[len(self.tail) - 1])

			#create new apple position
			self.apple_pos = [randint(10, self.length - 10), randint(25, self.height - 10)]
			self.pickup_history.append('r')

		#check if user ate a blue apple
		if (self.blue_apple_pos[0] - 10 <= self.x_pos <= self.blue_apple_pos[0] + 10) and (self.blue_apple_pos[1] - 10 <= self.y_pos <= self.blue_apple_pos[1] + 10):

			points_awarded = int(round( int( round( (abs(cos( len(self.tail) - 4)) * 10 ) ) ) * self.point_multiplier ))

			for _ in (xrange(points_awarded) if points_awarded else [1]):
				self.tail.append(self.tail[len(self.tail) - 1])

			#create new apple position
			self.blue_apple_pos = [randint(10, self.length - 10), randint(25, self.height - 10)]
			self.pickup_history.append('b')

		#check if user ate a green apple
		if (self.green_apple_pos[0] - 10 <= self.x_pos <= self.green_apple_pos[0] + 10) and (self.green_apple_pos[1] - 10 <= self.y_pos <= self.green_apple_pos[1] + 10):

			points_awarded = int(round( int( round( (abs(sin( len(self.tail) - 4) * cos( len(self.tail) - 4 )) * 10 ) ) ) * self.point_multiplier ))

			for _ in (xrange(points_awarded) if points_awarded else [1]):
				self.tail.append(self.tail[len(self.tail) - 1])

			#create new apple position
			self.green_apple_pos = [randint(10, self.length - 10), randint(25, self.height - 10)]
			self.pickup_history.append('g')

		#during powerup state
		if self.STATE_powerup:

			#add/subtract 1 to/from blue color value of snake_color
			snake_color = list(self.snake_color)

			if snake_color[1] == 255:
				self.colorchange_rate_sign = '-'
			elif snake_color[1] == 0:
				self.colorchange_rate_sign = '+'

			if self.colorchange_rate_sign == '+':
				snake_color[1] += 1
			else:
				snake_color[1] -= 1

			self.snake_color = tuple(snake_color)

			#count powerup time, create timer text
			current_powerup_time = (pygame.time.get_ticks() / 1000) - self.powerup_start_time
			self.powerup_timer_text = self.myfont.render(str(current_powerup_time), False, self.snake_color)
			if current_powerup_time >= 10:
				self.GAME_disable_powerup()

			#create combo text
			self.combo_text = self.myfont.render('Powerup x {}'.format(self.combo_powerup), False, self.snake_color)

		#update score text
		self.score_count = self.myfont.render('Score: {}'.format(len(self.tail) - 4), False, (255, 255, 255))

		#check if user has lost
		defeat = False
		if self.x_pos < 0 or self.x_pos > self.length or self.y_pos < 0 or self.y_pos > self.height:
			defeat = True
		elif [self.x_pos, self.y_pos] in self.tail and self.self_death:
			defeat = True

		if defeat:
			self._running = False
			self.defeat_text = self.myfont.render('Defeat', False, (255, 0, 0))



	def on_render(self):
		self._display_surf.fill((0, 0, 0,))

		#draw head
		pygame.draw.ellipse(self._display_surf, self.snake_color, (self.x_pos, self.y_pos, 10, 10))

		#draw tail
		for piece_pos in self.tail:
			pygame.draw.rect(self._display_surf, self.snake_color, (piece_pos[0], piece_pos[1], 10, 10))

		#draw eyes
		pygame.draw.circle(self._display_surf, (255, 0, 0,), (self.x_pos + 1, self.y_pos), 2)
		pygame.draw.circle(self._display_surf, (255, 0, 0,), (self.x_pos + 9, self.y_pos), 2)

		#draw apple
		pygame.draw.rect(self._display_surf, (255, 0, 0,), (self.apple_pos[0], self.apple_pos[1], 10, 10))

		#draw blue apple
		pygame.draw.rect(self._display_surf, (0, 0, 255,), (self.blue_apple_pos[0], self.blue_apple_pos[1], 10, 10))

		#draw green apple
		pygame.draw.rect(self._display_surf, (0, 255, 0,), (self.green_apple_pos[0], self.green_apple_pos[1], 10, 10))

		#draw color powerup panel
		self._display_surf.blit(self.UI.convert_alpha(), (0,0))
		pygame.draw.rect(self._display_surf, self.rgb_colors[self.powerup_sequence[0]], (10, 10, 20, 20), 5)
		pygame.draw.rect(self._display_surf, self.rgb_colors[self.powerup_sequence[1]], (40, 10, 20, 20), 5)
		pygame.draw.rect(self._display_surf, self.rgb_colors[self.powerup_sequence[2]], (70, 10, 20, 20), 5)

		#decide if/where to draw ticks in powerup panel
		if self.pickup_history:
			if self.pickup_history[0] == self.powerup_sequence[0]:
				self._display_surf.blit(self.tick, (14, 10))

				if len(self.pickup_history) in [2, 3]:
					if self.pickup_history[1] == self.powerup_sequence[1]:
						self._display_surf.blit(self.tick, (44, 10))

						if len(self.pickup_history) == 3:
							if self.pickup_history[2] == self.powerup_sequence[2]:
								self._display_surf.blit(self.tick, (74, 10))
								self.GAME_activate_powerup()

								self.pickup_history = []

							else:
								self.pickup_history = []

								self.powerup_sequence = [choice(self.rgb_colors.keys()), choice(self.rgb_colors.keys()), choice(self.rgb_colors.keys())]

					else:
						self.pickup_history = []

						self.powerup_sequence = [choice(self.rgb_colors.keys()), choice(self.rgb_colors.keys()), choice(self.rgb_colors.keys())]

			else:
				self.pickup_history = []

				self.powerup_sequence = [choice(self.rgb_colors.keys()), choice(self.rgb_colors.keys()), choice(self.rgb_colors.keys())]

		#show score count
		self._display_surf.blit(self.score_count, (self.length - 160, 0))

		if self.defeat_text:
			self._display_surf.blit(self.defeat_text, (600, 400))

		if self.STATE_powerup:

			#show powerup timer
			if self.powerup_timer_text:
				self._display_surf.blit(self.powerup_timer_text, (100, 0))

			#show combo text
			if self.combo_text:
				self._display_surf.blit(self.combo_text, (0, 35))

		pygame.display.update()

	def on_cleanup(self):
		pygame.quit()
		exit()
 
	def on_execute(self):
		if self.on_init() == False:
			self._running = False
 
		while( self._running ):
			self.clock.tick(60)

			for event in pygame.event.get():
				self.on_event(event)

			self.on_loop()

			self.on_render()

		while True:
			for event in pygame.event.get():
				if event.type == pygame.KEYDOWN:
					self.on_cleanup()


if __name__ == '__main__':
	run = Run()
	run.on_execute()
