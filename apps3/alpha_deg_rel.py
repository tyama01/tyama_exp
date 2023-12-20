import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from scipy.stats import linregress
from utils import *
import pickle
from matplotlib import cm
from matplotlib import rcParams as rcp



# /usr/bin/python3 /Users/tyama/tyama_exp/apps3/alpha_deg_rel.py

# コミュニティと次数分布の関係

dataset_name = input("Enter the dataset name: ")
data_loader = DataLoader(dataset_name, is_directed=False)
data_loader.load_community()
G = data_loader.get_graph()

nodes_list = list(G.nodes())
n = len(nodes_list)

# {所属するコミュニティ：頂点idのリスト}, {頂点id:所属するコミュニティ}
c_id, id_c = data_loader.get_communities()

y = []
for i in range(len(c_id)):
    y.append(len(c_id[i]))

z = np.sort(y)[::-1]
com_size_sort_data = np.argsort(y)[::-1] # コミュニティサイズが大きいラベル
#print(labels_data) 

print("----------------------------")

alpha_list = [alpha for alpha in range(5, 100, 5)]
#print(alpha_list)

# {alpha : {node_id : PR 値}}
pr_alpha_dic = {}

for alpha in alpha_list:
    path = '../alpha_dir/facebook/alpha_' + str(alpha) + '.pkl'
    with open(path, 'rb') as f:
        ppr_dic = pickle.load(f)
        
    ppr_sum_dic = {node : 0 for node in ppr_dic}
    
    for src_node in ppr_dic:
        for node in nodes_list:
            if node in ppr_dic[src_node]:
                ppr_sum_dic[node] += ppr_dic[src_node][node] / n
            else:
                continue
            
    pr_alpha_dic[alpha] = ppr_sum_dic

# 各ノードのベスト α を保持
best_alpha_dic = {id : 0 for id in nodes_list}

for id in nodes_list:
    alpha_dic = {a1 : 0 for a1 in alpha_list}
    for a2 in alpha_list:
        alpha_dic[a2] = pr_alpha_dic[a2][id]
    best_alpha_dic[id] = max(alpha_dic, key=alpha_dic.get)

# 次数を計算    
degree = dict(G.degree())

best_alpha_list = []
degree_list = []

for id in nodes_list:
    best_alpha_list.append(best_alpha_dic[id])
    degree_list.append(degree[id])
    
# key, val 入れ替え
#best_alpha_dic_swap = {v: k for k, v in best_alpha_dic.items()}

box_list = []

for alpha in alpha_list:
    sub_box_list = []
    for id in nodes_list:
        if best_alpha_dic[id] == alpha:
            sub_box_list.append(degree[id])
            
    box_list.append(sub_box_list)

# ------------------ Plot ----------------------

rcp['font.family'] = 'sans-serif'
rcp['font.sans-serif'] = ['Hiragino Maru Gothic Pro', 'Yu Gothic', 'Meirio', 'Takao', 'IPAexGothic', 'IPAPGothic', 'VL PGothic', 'Noto Sans CJK JP']

# カラーマップを用意する。
cmap = plt.get_cmap("tab10")

# Figureを作成する。
fig = plt.figure()
# Axesを作成する。
ax = fig.add_subplot(111)

# Figureの解像度と色を設定する。
fig.set_dpi(150)
fig.set_facecolor("white")

# Axesのタイトルと色を設定する。
#ax.set_title("物品の所有率")
ax.set_facecolor("white")

# x軸とy軸のラベルを設定する。
ax.set_xlabel("alpha", fontsize=14)
ax.set_ylabel("Degree", fontsize=14)

x = np.arange(5, 100, 5)

ax.scatter(np.array(best_alpha_list)/100, degree_list)

ax.minorticks_on()
ax.set_xticks([x/100 for x in range(5, 100, 5)])
ax.grid(which="major", color="gray", linestyle="solid")
ax.grid(which="minor", color="lightgray", linestyle="dotted")

plt.xticks(rotation=90)
plt.tight_layout()
plt.show()
#plt.savefig("../fig/alpha_deg.pdf")

# ------------------ Plot ----------------------

rcp['font.family'] = 'sans-serif'
rcp['font.sans-serif'] = ['Hiragino Maru Gothic Pro', 'Yu Gothic', 'Meirio', 'Takao', 'IPAexGothic', 'IPAPGothic', 'VL PGothic', 'Noto Sans CJK JP']

# カラーマップを用意する。
cmap = plt.get_cmap("tab10")

fig, ax = plt.subplots()

x = np.arange(5, 100, 5)


# Figureの解像度と色を設定する。
fig.set_dpi(150)
fig.set_facecolor("white")

# Axesのタイトルと色を設定する。
#ax.set_title("物品の所有率")
ax.set_facecolor("white")

# x軸とy軸のラベルを設定する。
ax.set_xlabel("alpha", fontsize=14)
ax.set_ylabel("Degree", fontsize=14)


#ax.minorticks_on()
ax.set_xticklabels([x/100 for x in range(5, 100, 5)])
#ax.grid(which="major", color="gray", linestyle="solid")
#ax.grid(which="minor", color="lightgray", linestyle="dotted")

ax.boxplot(box_list)


plt.xticks(rotation=90)
plt.tight_layout()
plt.show()