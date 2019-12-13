import time
import numpy as np
import random
from environment_RL_separate_joint_space import Env
import random
from collections import defaultdict
import tkinter as tk
from PIL import ImageTk, Image
PhotoImage = ImageTk.PhotoImage


class Env(tk.Tk):
	#This means Env class is a subclass of the class <tkinter.Tk>
	def __init__(self):
		super(Env, self).__init__()
		#This is just to say that we are initializing the tk.Tk interface. It is necessari. It shows the windos
		self.action_space = ['u','ur' 'r', 'rd','d', 'dl','l','lu']
		self.n_actions = len(self.action_space)
		self.title('Q Learning')
		self.geometry('{0}x{1}'.format(100 * 10, 100 * 10))
		#I dont know what that's for
		self.shapes = self.load_images()
		#This stores a vector of shapes 
		self.canvas = self._build_canvas()
		self.texts = []
		self.achieved = [False,False,False,False]

	def _build_canvas(self):

		print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
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

		self.pos_target_3_x = UNIT*int(WIDTH*((random.random()))) + UNIT/2
		self.pos_target_3_y = UNIT*int(HEIGHT*((random.random()))) + UNIT/2

		self.robot_1 = canvas.create_image(self.pos_robot_1_x,self.pos_robot_1_y,image=self.shapes[0])
		self.circle_3 = canvas.create_image(self.pos_target_3_x,self.pos_target_3_y,image=self.shapes[2])

		# pack all
		canvas.pack()

		return canvas

	def load_images(self):
	rectangle = PhotoImage(
		Image.open("img/ut.jpeg").resize((65, 65)))
	triangle = PhotoImage(
		Image.open("img/triangle.png").resize((65, 65)))
	circle = PhotoImage(
		Image.open("img/circle.png").resize((65, 65)))
	drako = PhotoImage(
		Image.open("img/drako.jpg").resize((65, 65)))
	
	return rectangle, triangle, circle,drako


if __name__ == "__main__":
	env = Env()
	print("aasdfasdf")
	env.update()