import matplotlib.pyplot as plt
import numpy as np
import random

#State = tuple with the positions. It will be a np.array of 2 components
#in this case, each of them learns indipendently with the constraint that they loose 10 of reward if they collide

class game():
	def __init__(self):	
		self.size = 10

		#self.array_positions = array_positions = np.array([int(3*random.random()),int(3*random.random()),int(3*random.random()),int(10*random.random()),int(10*random.random()),int(10*random.random()),int(10*random.random()),int(10*random.random())])

		#self.position_robot_1 = np.array([array_positions[0],array_positions[1]])
		#self.position_robot_2 = np.array([array_positions[2],array_positions[3]])
		#self.position_target_1 = np.array([array_positions[4],array_positions[5]])
		#self.position_target_2 = np.array([array_positions[6],array_positions[7]])


		self.position_robot_1 = np.array([int(10*random.random()),int(10*random.random())])
		self.position_target_1 = np.array([int(10*random.random()),int(10*random.random())])
		self.position_target_2 = np.array([int(10*random.random()),int(10*random.random())])

		self.matrix = np.zeros((10,10))

		self.matrix[self.position_robot_1[0]][self.position_robot_1[1]]=9999
		#self.matrix[array_positions[2]][array_positions[3]]=9999
		self.matrix[self.position_target_1[0]][self.position_target_1[1]]=1111
		self.matrix[self.position_target_2[0]][self.position_target_2[1]]=1111

		self.ini_state_1 = self.position_robot_1
		#self.ini_state_2 = self.position_robot_2

		self.Q1 = np.zeros((10,10,4)) #en principi es la posicio els estats pero despres ho generalitzarem
		self.Q2 = np.zeros((10,10,4))

		self.alpha = 1
		self.completed_target_1 = False
		self.completed_target_2 = False

	def show(self):
		print(self.matrix)
	def get_pos_robot1(self):	
		return self.position_robot_1
	def get_pos_robot2(self):
		return self.position_robot_2


	def get_reward_robot1(self,state):
		reward = 0
		if ((state[0] == self.position_target_1[0]) and (state[1] ==self. position_target_1[1]) and self.completed_target_1 == False):
			reward = 100
			self.completed_target_1 = True
		if ((state[0] == self.position_target_2[0]) and (state[1] == self.position_target_2[1]) and self.completed_target_2 == False):
			reward = 100
			self.completed_target_2 = True
		return reward

	def get_reward_robot2(self,state2,state1):
		reward = 0
		if ((state[0] == self.position_target_1[0]) and (state[1] == self.position_target_1[1])):
			reward = 100
		if ((state[0] == self.position_target_2[0]) and (state[1] == self.position_target_2[1])):
			reward = 100
		if (state1 == state2):
			reward = -10
		reward -= 1
		return reward

	def feasible_action(self,state,action):
		new_state = np.array([0,0])
		if (action == 0):
			#means we want to move to the left
			new_state[0] = state[0]
			new_state[1] = state[1] - 1 

		if (action == 1):
			new_state[0] = state[0] - 1
			new_state[1] = state[1]

		if (action == 2):
			new_state[0] = state[0]
			new_state[1] = state[1] + 1

		if (action == 3):
			new_state[0] = state[0] + 1
			new_state[1] = state[1]

		if (new_state[0] < 0):
			return False
		if (new_state[1] < 0):
			return False
		if (new_state[0] >= 10):
			return False
		if (new_state[1] >= 10):
			return False
		#in either of these cases we will have gotten out of the grid
		return True

	def apply_transition(self,state,action):
		new_state = np.array([0,0])
		if (action == 0):
			#means we want to move to the left
			new_state[0] = state[0]
			new_state[1] = state[1] - 1 

		if (action == 1):
			new_state[0] = state[0] - 1
			new_state[1] = state[1]

		if (action == 2):
			new_state[0] = state[0]
			new_state[1] = state[1] + 1

		if (action == 3):
			new_state[0] = state[0] + 1
			new_state[1] = state[1]
		#print("new state is",new_state)
		self.matrix[new_state[0]][new_state[1]]=9999
		return new_state

	def choose_action_robot1(self,state):
		#We will apply Q-learning
		
		x_coor = state[0]
		y_coor = state[1]
		#action_indice = -1
		random_action = np.array([0,1,2,3])
		random.shuffle(random_action)
		maximum_value = np.min(self.Q1[x_coor][y_coor][:])
		#this way it doesn't get stuck into the right-down corner in the beggining
		
		for action in random_action:
			if (self.Q1[x_coor][y_coor][action] >= maximum_value):
				if (self.feasible_action(state,action)):
					#print("Han passat la prova",action)
					maximum_value = self.Q1[x_coor][y_coor][action]
					action_indice = action
		#print("action choosen is",action_indice)
		

		a = int(100*(random.random()))
		if (a < 5):
			random_action = int(4*random.random())
			if (self.feasible_action(state,random_action)):
				return random_action
		return action_indice

	def choose_action_robot2(self,state):
		#We will apply Q-learning
		maximum_value = -1000000
		x_coor = state[0]
		y_coor = state[1]
		action_indice = -1
		for action in range(4):
			if (Q1[x_coor][y_coor][action] >= maximum_value):
				if (feasible_action(state,action)):
					maximum_value = Q1[x_coor][y_coor][action]
					action_indice = action
		#in this loop we are selecting the action that has higher q value and gets us to a feasible state
		return action_indice

	def update_q1(self, old_state, action, reward, new_state, alpha):
		#We have to define states(cartesian product of the positions) and states(16 posible directions)
		#self.Q1[old_state[0]][old_state[1]][action] =+ self.alpha * (reward + np.max(self.Q1[new_state[0]][new_state[1]]) - self.Q1[old_state[0]][old_state[1]][action])
		self.Q1[old_state[0]][old_state[1]][action] += 0.1 * (reward + 0.9*(np.max(self.Q1[new_state[0]][new_state[1]][:])) - self.Q1[old_state[0]][old_state[1]][action])
	#Will try first with just one robot
	def run(self):
		for i in range(1000):
			self.completed_target_1 = False
			initial_state_1 = self.position_robot_1
			self.matrix[self.position_target_1[0]][self.position_target_1[1]]=1111
			self.matrix[self.position_target_2[0]][self.position_target_2[1]]=1111
			for j in range(10000):
				self.matrix[initial_state_1[0]][initial_state_1[1]]=0
				#initial_state_2 = self.ini_state_2
				choosen_action_1 = self.choose_action_robot1(initial_state_1) #the action robot 1 will choose
				#choosen_action_2 = choose_action_robot2(self.ini_state_2) #the action robot 2 will choose
				new_state = self.apply_transition(initial_state_1,choosen_action_1)
				self.matrix[new_state[0]][new_state[1]] = 9999
				#print(new_state)
				reward = self.get_reward_robot1(new_state)
				self.update_q1(initial_state_1,choosen_action_1,reward,new_state,0.1)
				initial_state_1 = new_state
				if (self.completed_target_1 and self.completed_target_2):
					print("we did it with j timesteps",j)
					break
				#print(self.matrix)
				
			#print(self.Q1)
			
game = game()
game.run()