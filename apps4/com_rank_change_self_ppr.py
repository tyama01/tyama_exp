# self PPR のランキングが各コミュニティでどの順位にいるかを調べるコード

from utils import *
import pickle
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib import rcParams as rcp
import numpy as np


# -------------------------- データ読み込み -------------------------
dataset_name = input("Enter the dataset name: ")
data_loader = DataLoader(dataset_name, is_directed=False)
G = data_loader.get_graph()
print(G) # グラフのノード数、エッジ数出力

data_loader.load_community()

# {所属するコミュニティ：頂点idのリスト}, {頂点id:所属するコミュニティ}
c_id, id_c = data_loader.get_communities() 

print("-----------------------------------")

node_list = list(G.nodes)
n = len(node_list)
#------------------------------------------------------------------

#------------------------------------------------------------------
# networkx PR 演算
pr = nx.pagerank(G, alpha=0.85)

# 通常の PR を降順にソート
pr_sort = sorted(pr.items(), key=lambda x:x[1], reverse=True)

id_sort = []
pr_value_sort = []
for item in pr_sort:
    id_sort.append(item[0])
    pr_value_sort.append(item[1])

# pr 順位を格納    
pr_rank_dic = {com_id : [] for com_id in c_id}

for rank_num in range(n):
    pr_rank_dic[id_c[id_sort[rank_num]]].append(rank_num) 

#------------------------------------------------------------------

#------------------------------------------------------------------
# selfPPR の結果読み込み
alpha = 15
self_ppr = {}

path = '../alpha_dir/' + dataset_name + '/self_ppr_' + str(alpha) + '.txt'
with open(path) as f:
    for line in f:
        (id, val) = line.split()
        self_ppr[int(id)] = float(val)

# Self PPR を降順にソート
self_ppr_sort = sorted(self_ppr.items(), key=lambda x:x[1], reverse=True)
        
self_ppr_id_sort = []
self_ppr_value_sort = []

for item in self_ppr_sort:
    self_ppr_id_sort.append(item[0])
    self_ppr_value_sort.append(item[1])
    
# Self PPR の順位をコミュニティ別で格納        
self_ppr_rank_dic = {com_id : [] for com_id in c_id}

for rank_num in range(n):
    self_ppr_rank_dic[id_c[self_ppr_id_sort[rank_num]]].append(rank_num)

#------------------------------------------------------------------

#------------------------------------------------------------------
# 箱ひげ図　プロット 通常 PR ver

y = []
for i in range(len(c_id)):
    y.append(len(c_id[i]))

z = np.sort(y)[::-1]
labels_data = np.argsort(y)[::-1]
labels_data = labels_data.tolist()
labels_data.reverse()
x = np.arange(len(labels_data))


y1 = []
for com_id in labels_data:
    y1.append(pr_rank_dic[com_id])

fig, ax = plt.subplots()

ax.boxplot(y1, vert=False)
ax.set_yticklabels(labels_data)
ax.set_xlabel("Rank")
ax.set_ylabel("Community label")

# グリッドを表示する。
ax.set_axisbelow(True)
ax.grid(True, "major", "x", linestyle="--")
ax.grid(True, "major", "y", linestyle="--")

#plt.legend()
plt.tight_layout()
plt.show()

#------------------------------------------------------------------

#------------------------------------------------------------------
# 箱ひげ図　プロット 通常 PR ver

y = []
for i in range(len(c_id)):
    y.append(len(c_id[i]))

z = np.sort(y)[::-1]
labels_data = np.argsort(y)[::-1]
labels_data = labels_data.tolist()
labels_data.reverse()
x = np.arange(len(labels_data))


y1 = []
for com_id in labels_data:
    y1.append(self_ppr_rank_dic[com_id])

fig, ax = plt.subplots()

ax.boxplot(y1, vert=False)
ax.set_yticklabels(labels_data)
ax.set_xlabel("Rank")
ax.set_ylabel("Community label")

# グリッドを表示する。
ax.set_axisbelow(True)
ax.grid(True, "major", "x", linestyle="--")
ax.grid(True, "major", "y", linestyle="--")

#plt.legend()
plt.tight_layout()
plt.show()

#------------------------------------------------------------------

