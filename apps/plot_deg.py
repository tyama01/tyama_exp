import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from scipy.stats import linregress
from utils import *

# /usr/bin/python3 /Users/tyama/tyama_exp/apps/plot_deg.py
dataset_name = input("Enter the dataset name: ")
data_loader = DataLoader(dataset_name)
data_loader.load_graph()
data_loader.load_community()
G = data_loader.get_graph()

# {所属するコミュニティ：頂点idのリスト}, {頂点id:所属するコミュニティ}
c_id, id_c = data_loader.get_communities() 


print("----------------------------")

degree = dict(G.degree())
pos_degree_vals = list(filter(lambda val:val>0, degree.values()))
uq_pos_degree_vals = sorted(set(pos_degree_vals))
in_hist = [pos_degree_vals.count(x) for x in uq_pos_degree_vals]

x = np.asarray(uq_pos_degree_vals, dtype = float)
y = np.asarray(in_hist, dtype = float)

logx = np.log10(x)
logy = np.log10(y)

a, b = np.polyfit(logx, logy, 1)

plt.figure(figsize=(10,10))
#plt.xlim(min(logx), max(logx))
plt.xlabel('log10 (In Degree)')
plt.ylabel('log10 (Number of nodes)')
plt.title('In Degree Distribution of network')
scatter_plot = plt.plot(logx, logy, 'o')
scatter_plot_regression = plt.plot(logx, a*logx + b)

plt.show()

print("a: " + str(a))
print("b: " + str(b))