import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib as mpl

# /usr/bin/python3 /Users/tyama/tyama_exp/apps9/test_plot.py

#mpl.style.use('ggplot')
mpl.style.use('seaborn-darkgrid')

fig, ax = plt.subplots(figsize=(5, 5))
ax.plot([1, 2, 4, 8])
ax.plot([2, 3, 6, 7])

plt.show()