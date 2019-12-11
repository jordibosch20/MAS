import matplotlib.pyplot as plt
import numpy as np
from matplotlib import colors
from matplotlib.ticker import PercentFormatter
import time

N_points = 100000
n_bins = 40

file = open("output_file/output_RL_1.txt","r")
suma_prova = 0
x = np.array([])

for f in file:
	#print(f)
	a = int(f)
	x = np.append(x,[a])
	#we append to the np array x, the new value readed

fig, axs = plt.subplots(1, 1, sharey=True, tight_layout=True,figsize=(14,10))
#Subplot of the same figure with 1 row, 2 columns, sharing the Y-axis
#axs is not axes, it stands for each one of my plots. and tight_layout is for everything to be
#correctly displayed	

# We can set the number of bins with the `bins` kwarg
#I want to study the vector of results, Supose that x = vector of results

counter = 0
sum = 0
y = []
for i in x:
	counter += 1
	sum += i
	if (counter % 10 == 0):
		y.append(sum / 10)
		sum = 0
		#We group the data in the averages of 10
#Right now the vector y has the averages 10 by 10
fig.suptitle("Result of diferent brains and separate joint action space",fontsize=16)
axs.plot(y)
#axs.set_title('subplot 1')
axs.set_xlabel('Number of episodes',fontsize=15,labelpad=20)
axs.set_ylabel('Average of 10 from the number of steps needed',fontsize=15,labelpad=20)

axs.plot(y)
#axs[0].hist(x, bins=n_bins)
#axs[1].hist(y, bins=n_bins)
plt.savefig("output_image/output_RL.png")

plt.show()
