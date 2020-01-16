import time
import numpy as np
import random
from environment_RL_separate_joint_space import Env
import random
from collections import defaultdict

class QLearningAgent:
	def __init__(self, actions):
		# actions = [0, 1, 2, 3, 4, 5, 6, 7]
		self.actions = actions
		self.learning_rate = 0.01
		self.discount_factor = 0.9
		self.epsilon = 0.05
		self.q_table = defaultdict(lambda: [0.0, 0.0, 0.0, 0.0,0.0,0.0,0.0,0.0])
		self.elig = defaultdict(lambda: [0.0, 0.0, 0.0, 0.0,0.0,0.0,0.0,0.0])
		self.landa = 1

	# update q function with sample <s, a, r, s'>
	def learn(self, state, action, reward, next_state):

		self.elig[state][action] += 1
		current_q = self.q_table[state][action]
		# using Bellman Optimality Equation to update q function
		new_q = reward + self.discount_factor * max(self.q_table[next_state])
		#print(new_q)
		#self.q_table[state][action] += self.learning_rate * (new_q - current_q)
		#The RHS is what we should update multiplied by the eligibility trace
		for i in self.q_table:
			for j in range(8):
				self.q_table[i][j] += self.elig[i][j]*self.learning_rate*(new_q - current_q)

		for i in self.elig:
			for j in range(8):
				self.elig[i][j] = self.elig[i][j]*self.discount_factor*self.landa

		#print(self.elig)
		#print("This is the qtable")
		#print(self.q_table)
	# get action for the state according to the q function table
	# agent pick action of epsilon-greedy policy
	def get_action(self, state):
		if np.random.rand() < self.epsilon:
			# take random action
			action = np.random.choice(self.actions)
		else:
			# take action according to the q function table
			state_action = self.q_table[state]
			action = self.arg_max(state_action)
		return action

	@staticmethod
	def arg_max(state_action):
		max_index_list = []
		max_value = state_action[0]
		for index, value in enumerate(state_action):
			if value > max_value:
				max_index_list.clear()
				max_value = value
				max_index_list.append(index)
			elif value == max_value:
				max_index_list.append(index)
		return random.choice(max_index_list)

if __name__ == "__main__":
	env = Env()
	agent_1 = QLearningAgent(actions=list(range(env.n_actions)))
	agent_2 = QLearningAgent(actions=list(range(env.n_actions)))
	for episode in range(1000):
		state_1 = env.reset(1,episode)
		state_2 = env.reset(2,episode)
		counter = 0
		while True:
			counter += 1
			env.render()
			#time.sleep(0.1)
			# take action and proceed one step in the environment
			action_1 = agent_1.get_action(str(state_1))

			next_state_1, reward_1, done_1 = env.step_1(action_1)
			agent_1.learn(str(state_1), action_1, reward_1, str(next_state_1))
			#We have to update elig_trace of state1

			state_1 = next_state_1
			env.print_value_all(agent_1.q_table)

			#Here it starts Agent 2
			action_2 = agent_2.get_action(str(state_2))

			next_state_2, reward_2, done_2 = env.step_2(action_2)
			agent_2.learn(str(state_2), action_2, reward_2, str(next_state_2))
			

			state_2 = next_state_2
			#env.print_value_all(agent_2.q_table_2)
			#time.sleep(0.2)

			# if episode ends, then break
			resultat = np.logical_or(done_1,done_2)
			#print("el resultat es", resultat)

			if resultat[0] and resultat[1] and resultat[2]:
				print(counter)
				env.render()
				#time.sleep(2)
				break
			if resultat[3]:
				env.render()
				#print("BAD:",counter)
				#time.sleep(0.00005)
				break
