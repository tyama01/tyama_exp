import seaborn as sns 
import pandas as pd 
import numpy as np 
import matplotlib as mpl
import matplotlib.pyplot as plt

# /usr/bin/python3 /Users/tyama/tyama_exp/apps8/test_heatmap.py

array = np.arange(-8, 8).reshape((4, 4))
print(array)

plt.figure()
sns.heatmap(array, square=True, cmap='gist_heat_r')
plt.show()