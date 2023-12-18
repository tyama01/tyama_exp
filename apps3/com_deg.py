import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from scipy.stats import linregress
from utils import *

# /usr/bin/python3 /Users/tyama/tyama_exp/apps3/com_deg.py
# コミュニティと次数分布の関係

dataset_name = input("Enter the dataset name: ")
data_loader = DataLoader(dataset_name, is_directed=False)
data_loader.load_community()
G = data_loader.get_graph()

# {所属するコミュニティ：頂点idのリスト}, {頂点id:所属するコミュニティ}
c_id, id_c = data_loader.get_communities()

y = []
for i in range(len(c_id)):
    y.append(len(c_id[i]))

z = np.sort(y)[::-1]
labels_data = np.argsort(y)[::-1] # コミュニティサイズが大きいラベル
#print(labels_data) 

print("----------------------------")

gamma_list = []

for com_id in labels_data:
    sub_G = G.subgraph(c_id[com_id])
    degree = dict(sub_G.degree())
    pos_degree_vals = list(filter(lambda val:val>0, degree.values()))
    uq_pos_degree_vals = sorted(set(pos_degree_vals))
    in_hist = [pos_degree_vals.count(x) for x in uq_pos_degree_vals]

    x = np.asarray(uq_pos_degree_vals, dtype = float)
    y = np.asarray(in_hist, dtype = float)

    logx = np.log10(x)
    logy = np.log10(y)

    a, b = np.polyfit(logx, logy, 1)
    gamma_list.append(a)


"""
plt.figure(figsize=(10,10))
#plt.xlim(min(logx), max(logx))
plt.xlabel('log10 (In Degree)')
plt.ylabel('log10 (Number of nodes)')
plt.title('In Degree Distribution of network')
scatter_plot = plt.plot(logx, logy, 'o')
scatter_plot_regression = plt.plot(logx, a*logx + b)

plt.show()
"""

#print("a: " + str(a))
#print("b: " + str(b))

i = 0
for com_id in labels_data:
    print(f"Com ID: {com_id} | gamma: {gamma_list[i]}")
    i+=1