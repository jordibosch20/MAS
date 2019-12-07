import time
import numpy as np
import random
from environment_2_robots import Env
import random
from collections import defaultdict

class QLearningAgent:
	def __init__(self, actions):
		# actions = [0, 1, 2, 3, 4, 5, 6, 7]
		self.actions = actions
		self.learning_rate = 0.01
		self.discount_factor = 0.9
		self.epsilon = 0.1
		self.q_table_1 = defaultdict(lambda: [0.0, 0.0, 0.0, 0.0,0.0,0.0,0.0,0.0])
		self.q_table_2 = defaultdict(lambda: [0.0, 0.0, 0.0, 0.0,0.0,0.0,0.0,0.0])

	# update q function with sample <s, a, r, s'>
	def learn_1(self, state, action, reward, next_state):
		current_q = self.q_table_1[state][action]
		# using Bellman Optimality Equation to update q function
		new_q = reward + self.discount_factor * max(self.q_table_1[next_state])
		self.q_table_1[state][action] += self.learning_rate * (new_q - current_q)

	def learn_2(self, state, action, reward, next_state):
		current_q = self.q_table_2[state][action]
		# using Bellman Optimality Equation to update q function
		new_q = reward + self.discount_factor * max(self.q_table_2[next_state])
		self.q_table_2[state][action] += self.learning_rate * (new_q - current_q)

	# get action for the state according to the q function table
	# agent pick action of epsilon-greedy policy
	def get_action_1(self, state):
		if np.random.rand() < self.epsilon:
			# take random action
			action = np.random.choice(self.actions)
		else:
			# take action according to the q function table
			state_action = self.q_table_1[state]
			action = self.arg_max(state_action)
		return action

	def get_action_2(self, state):
		if np.random.rand() < self.epsilon:
			# take random action
			action = np.random.choice(self.actions)
		else:
			# take action according to the q function table
			state_action = self.q_table_2[state]
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
		state_1 = env.reset_1()
		state_2 = env.reset_2()
		while True:
			env.render()

			# take action and proceed one step in the environment
			action_1 = agent_1.get_action_1(str(state_1))
			next_state_1, reward_1, done_1 = env.step_1(action_1)

			# with sample <s,a,r,s'>, agent learns new q function
			agent_1.learn_1(str(state_1), action_1, reward_1, str(next_state_1))

			state_1 = next_state_1
			env.print_value_all(agent_1.q_table_1)

			#Here it starts Agent 2

			action_2 = agent_2.get_action_2(str(state_2))
			next_state_2, reward_2, done_2 = env.step_2(action_2)

			# with sample <s,a,r,s'>, agent learns new q function
			agent_2.learn_2(str(state_2), action_2, reward_2, str(next_state_2))

			state_2 = next_state_2
			#env.print_value_all(agent_2.q_table_2)


			# if episode ends, then break

			resultat = np.logical_or(done_1,done_2)
			if resultat[0] and resultat[1] and resultat[2]:
				env.render()
				time.sleep(5)
				break
			if resultat[3]:
				env.render()
				time.sleep(0.00005)
				break