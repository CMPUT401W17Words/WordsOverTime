#from http://pythonprogramminglanguage.com/line-charts/
#Need to install numpy and matplotlib
#On Linux, use 'pip install numpy' and 'pip install matplotlib'

import numpy as np
import matplotlib.pyplot as plt

x = [2,3,4,5,7,9,13,15,17]
plt.plot(x)
plt.ylabel('Sunlight')
plt.xlabel('Time')
plt.show()
