import time
import numpy as np
import random
import tkinter as tk
from PIL import ImageTk, Image

np.random.seed(1)
PhotoImage = ImageTk.PhotoImage
UNIT = 100  # pixels
HEIGHT =  10  # grid height
WIDTH = 10  # grid width


class Env(tk.Tk):
	#This means Env class is a subclass of the class <tkinter.Tk>
	def __init__(self):
		super(Env, self).__init__()
		#This is just to say that we are initializing the tk.Tk interface. It is necessari. It shows the windos
		self.action_space = ['u','ur' 'r', 'rd','d', 'dl','l','lu']
		self.n_actions = len(self.action_space)
		self.title('Q Learning')
		self.geometry('{0}x{1}'.format(HEIGHT * UNIT, HEIGHT * UNIT))
		#I dont know what that's for
		self.shapes = self.load_images()
		#This stores a vector of shapes 
		self.canvas = self._build_canvas()
		self.texts = []
		self.achieved = np.array([False,False,False,False])

	def _build_canvas(self):
		canvas = tk.Canvas(self, bg='white',
						   height=HEIGHT * UNIT,
						   width=WIDTH * UNIT)
		# create grids
		for c in range(0, WIDTH * UNIT, UNIT):  # 0~400 by 80
			x0, y0, x1, y1 = c, 0, c, HEIGHT * UNIT
			canvas.create_line(x0, y0, x1, y1)
		for r in range(0, HEIGHT * UNIT, UNIT):  # 0~400 by 80
			x0, y0, x1, y1 = 0, r, HEIGHT * UNIT, r
			canvas.create_line(x0, y0, x1, y1)


		self.pos_robot_1_x = UNIT*int(WIDTH*((random.random()))) + UNIT/2
		self.pos_robot_1_y = UNIT*int(HEIGHT*((random.random()))) + UNIT/2
		self.pos_robot_2_x = UNIT*int(WIDTH*((random.random()))) + UNIT/2
		self.pos_robot_2_y = UNIT*int(HEIGHT*((random.random()))) + UNIT/2
		self.pos_obstacle_1_x = UNIT*int(WIDTH*((random.random()))) + UNIT/2
		self.pos_obstacle_1_y = UNIT*int(HEIGHT*((random.random()))) + UNIT/2
		self.pos_obstacle_2_x = UNIT*int(WIDTH*((random.random()))) + UNIT/2
		self.pos_obstacle_2_y = UNIT*int(HEIGHT*((random.random()))) + UNIT/2
		self.pos_target_1_x = UNIT*int(WIDTH*((random.random()))) + UNIT/2
		self.pos_target_1_y = UNIT*int(HEIGHT*((random.random()))) + UNIT/2
		self.pos_target_2_x = UNIT*int(WIDTH*((random.random()))) + UNIT/2
		self.pos_target_2_y = UNIT*int(HEIGHT*((random.random()))) + UNIT/2
		self.pos_target_3_x = UNIT*int(WIDTH*((random.random()))) + UNIT/2
		self.pos_target_3_y = UNIT*int(HEIGHT*((random.random()))) + UNIT/2

		print("la posicion del robot es",self.pos_robot_1_x,',',self.pos_robot_1_y,)
		print("la posicion del obstacle es",self.pos_obstacle_1_x,',',self.pos_obstacle_1_y,)
		print("la posicion del obstacle es",self.pos_obstacle_1_x,',',self.pos_obstacle_1_y,)
		print("la posicion del target es",self.pos_target_1_x,',',self.pos_target_1_y,)

		# add img to canvas
		self.robot_1 = canvas.create_image(self.pos_robot_1_x,self.pos_robot_1_y,image=self.shapes[0])
		self.robot_2 = canvas.create_image(self.pos_robot_2_x,self.pos_robot_2_y,image=self.shapes[3])
		self.triangle1 = canvas.create_image(self.pos_obstacle_1_x,self.pos_obstacle_1_y,image=self.shapes[1])
		self.triangle2 = canvas.create_image(self.pos_obstacle_2_x,self.pos_obstacle_2_y,image=self.shapes[1])
		self.circle_1 = canvas.create_image(self.pos_target_1_x,self.pos_target_1_y,image=self.shapes[2])
		self.circle_2 = canvas.create_image(self.pos_target_2_x,self.pos_target_2_y,image=self.shapes[2])
		self.circle_3 = canvas.create_image(self.pos_target_3_x,self.pos_target_3_y,image=self.shapes[2])

		# pack all
		canvas.pack()

		return canvas

	def load_images(self):
		rectangle = PhotoImage(
			Image.open("../img/ut.jpeg").resize((65, 65)))
		triangle = PhotoImage(
			Image.open("../img/triangle.png").resize((65, 65)))
		circle = PhotoImage(
			Image.open("../img/circle.png").resize((65, 65)))
		drako = PhotoImage(
			Image.open("../img/drako.jpg").resize((65, 65)))
		
		return rectangle, triangle, circle,drako

	def text_value(self, row, col, contents, action, font='Helvetica', size=4	,
				   style='normal', anchor="nw"):

		if action == 0: #up
			origin_x, origin_y = 7, 42

		elif action == 1:#upright
			origin_x, origin_y = 7, 75

		elif action == 2:#right
			origin_x, origin_y = 42, 75

		elif action == 3:#rightdown
			origin_x, origin_y = 82, 75
		
		elif action == 4:#down place
			origin_x, origin_y = 85, 42

		elif action == 5:#down-left
			origin_x, origin_y = 82, 7

		elif action == 6:#left place
			origin_x, origin_y = 42,7

		elif action == 7:
			origin_x, origin_y = 7, 5
		
		x, y = origin_y + (UNIT * col), origin_x + (UNIT * row)
		font = (font, str(size), style)
		text = self.canvas.create_text(x, y, fill="black", text=contents,
									   font=font, anchor=anchor)
		return self.texts.append(text)

	def print_value_all(self, q_table):
		for i in self.texts:
			self.canvas.delete(i)
			#you are deleting the q-value
		self.texts.clear()
		#This only empties the array
		for i in range(HEIGHT):
			for j in range(WIDTH):
				for action in range(0, 8):
					state = [i, j]
					if str(state) in q_table.keys():
						temp = q_table[str(state)][action]
						self.text_value(j, i, round(temp, 2), action)

	def coords_to_state(self, coords):
		x = int((coords[0] - 50) / 100)
		y = int((coords[1] - 50) / 100)
		return [x, y]

	def state_to_coords(self, state):
		x = int(state[0] * 100 + 50)
		y = int(state[1] * 100 + 50)
		return [x, y]

	def reset_1(self):
		self.update()
		self.achieved = np.array([False,False,False,False])
		time.sleep(0.0001)
		x, y = self.canvas.coords(self.robot_1)
		self.canvas.move(self.robot_1,-x + self.pos_robot_1_x, -y + self.pos_robot_1_y)
		self.render()
		# return observation
		return self.coords_to_state(self.canvas.coords(self.robot_1))

	def reset_2(self):
			self.update()
			self.achieved = np.array([False,False,False,False])
			time.sleep(0.0001)
			x, y = self.canvas.coords(self.robot_2)
			self.canvas.move(self.robot_2,-x + self.pos_robot_2_x, -y + self.pos_robot_2_y)
			self.render()
			# return observation
			return self.coords_to_state(self.canvas.coords(self.robot_1))


	def step_1(self, action):
		state = self.canvas.coords(self.robot_1)
		base_action = np.array([0, 0])
		self.render()
		#0-up,1-down,2-rigth,3-down
		if action == 0:  # up
			if state[1] > UNIT:
				base_action[1] -= UNIT

		#The condition for going upright is simple (going up and right)
		if action == 1:  # upright
			if (state[1] > UNIT and  state[0] < (WIDTH - 1) * UNIT):
				base_action[1] -= UNIT
				base_action[0] += UNIT

		elif action == 2:  # right
			if state[0] < (WIDTH - 1) * UNIT:
				base_action[0] += UNIT

		elif action == 3:  # rightdown
			if (state[0] < (WIDTH - 1) * UNIT and state[1] < (HEIGHT - 1) * UNIT):
				base_action[0] += UNIT
				base_action[1] += UNIT

		#We want to add the case
		elif action == 4:  # down
			if state[1] < (HEIGHT - 1) * UNIT:
				base_action[1] += UNIT

		elif action == 5:  # downleft
			if (state[0] < (WIDTH - 1) * UNIT and state[0] > UNIT):
				base_action[1] += UNIT
				base_action[0] -= UNIT

		elif action == 6:  # left
			if state[0] > UNIT:
				base_action[0] -= UNIT

		elif action == 7:  # leftup
			if (state[0] > UNIT and state[1] > UNIT):
				base_action[0] -= UNIT
				base_action[1] -= UNIT

		
		# move agent
		self.canvas.move(self.robot_1, base_action[0], base_action[1])
		# move robot_1 to top level of canvas
		self.canvas.tag_raise(self.robot_1)
		next_state = self.canvas.coords(self.robot_1)

		# reward function
		if (next_state == self.canvas.coords(self.circle_1)):
			reward = 100
			self.achieved[0] = True
		if (next_state == self.canvas.coords(self.circle_2)):
			reward = 100
			self.achieved[1] = True
		if (next_state == self.canvas.coords(self.circle_1)):
			reward = 100
			self.achieved[2] = True

		if next_state in [self.canvas.coords(self.triangle1),
							self.canvas.coords(self.triangle2)]:
			reward = -100
			self.achieved[3] = True
		else:
			reward = -1
			done = False

		next_state = self.coords_to_state(next_state)
		return next_state, reward, self.achieved

	def step_2(self, action):
		state = self.canvas.coords(self.robot_2)
		base_action = np.array([0, 0])
		self.render()

		#0-up,1-down,2-rigth,3-down
		if action == 0:  # up
			if state[1] > UNIT:
				base_action[1] -= UNIT

		#The condition for going upright is simple (going up and right)
		if action == 1:  # upright
			if (state[1] > UNIT and  state[0] < (WIDTH - 1) * UNIT):
				base_action[1] -= UNIT
				base_action[0] += UNIT

		elif action == 2:  # right
			if state[0] < (WIDTH - 1) * UNIT:
				base_action[0] += UNIT

		elif action == 3:  # rightdown
			if (state[0] < (WIDTH - 1) * UNIT and state[1] < (HEIGHT - 1) * UNIT):
				base_action[0] += UNIT
				base_action[1] += UNIT

		#We want to add the case
		elif action == 4:  # down
			if state[1] < (HEIGHT - 1) * UNIT:
				base_action[1] += UNIT

		elif action == 5:  # downleft
			if (state[0] < (WIDTH - 1) * UNIT and state[0] > UNIT):
				base_action[1] += UNIT
				base_action[0] -= UNIT

		elif action == 6:  # left
			if state[0] > UNIT:
				base_action[0] -= UNIT

		elif action == 7:  # leftup
			if (state[0] > UNIT and state[1] > UNIT):
				base_action[0] -= UNIT
				base_action[1] -= UNIT

		
		# move agent
		self.canvas.move(self.robot_2, base_action[0], base_action[1])
		# move robot_1 to top level of canvas
		self.canvas.tag_raise(self.robot_1)
		next_state = self.canvas.coords(self.robot_2)

		# reward function
		if (next_state == self.canvas.coords(self.circle_1)):
			reward = 100
			self.achieved[0] = True
		if (next_state == self.canvas.coords(self.circle_2)):
			reward = 100
			self.achieved[1] = True
		if (next_state == self.canvas.coords(self.circle_1)):
			reward = 100
			self.achieved[2] = True

		if next_state in [self.canvas.coords(self.triangle1),
							self.canvas.coords(self.triangle2)]:
			reward = -100
			self.achieved[3] = True
		else:
			reward = -1
			done = False

		next_state = self.coords_to_state(next_state)
		return next_state, reward, self.achieved


	def render(self):
		time.sleep(0.00001)
		self.update()

	def get_achieved(self):
		return self.achieved