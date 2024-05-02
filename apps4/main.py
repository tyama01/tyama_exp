# 自ノード PPR で重み付けした中心性指標

from utils import *
import networkx as nx
import sys
import pickle
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import math
import matplotlib as mpl
from matplotlib import rcParams as rcp
from scipy.stats import kendalltau


# /usr/bin/python3 /Users/tyama/tyama_exp/apps4/main.py

# -------------------------- データ読み込み -------------------------
dataset_name = input("Enter the dataset name: ")
data_loader = DataLoader(dataset_name, is_directed=True)
G = data_loader.get_graph()
print(G) # グラフのノード数、エッジ数出力

#data_loader.load_community()

# {所属するコミュニティ：頂点idのリスト}, {頂点id:所属するコミュニティ}
#c_id, id_c = data_loader.get_communities() 

print("-----------------------------------")

node_list = list(G.nodes)
n = len(node_list)
#------------------------------------------------------------------

#------------------------------------------------------------------
# PR 演算

# alpha の値を設定
alpha = 15
print(f'alpha = {alpha}')
path = '../alpha_dir/wiki/alpha_' + str(alpha) + '.pkl'
with open(path, 'rb') as f:
    ppr_dic = pickle.load(f)

# 普通の PR を計算
pr = {target_node : 0 for target_node in ppr_dic}

for src_node in ppr_dic:
    for target_node in node_list:
        if target_node in ppr_dic[src_node]:
            pr[target_node] += ppr_dic[src_node][target_node] / n
            
        else:
            continue
        
# 通常の PR を降順にソート
pr_sort = sorted(pr.items(), key=lambda x:x[1], reverse=True)

id_sort = []
pr_value_sort = []
for item in pr_sort:
    id_sort.append(item[0])
    pr_value_sort.append(item[1])

#------------------------------------------------------------------

#------------------------------------------------------------------

# 自ノードから見た PPR 読み込み
self_ppr_dic = dict()
with open("../alpha_dir/wiki/self_ppr_15.txt") as f:
    for line in f:
        (id, val) = line.split()
        self_ppr_dic[int(id)] = float(val)
        
# 提案手法 flow PR の計算
flow_pr_obj = flow_PR(G)

flow_pr = flow_pr_obj.calc_flow_rw_pr(self_ppr_dic=self_ppr_dic, alpha=0.15, w=4)

flow_pr_val = []

for id in id_sort:
    flow_pr_val.append(flow_pr[id])

c = 0
for id in flow_pr:
    c += flow_pr[id]
    
print(c)

print("End")
#------------------------------------------------------------------

#------------------------------------------------------------------
# plot PR 順位降順

# フォントを設定する。
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
ax.set_xlabel("Node ID (PR sort)", fontsize=14)
ax.set_ylabel("value of node importance (log scale)", fontsize=14)

#ax.set_yscale('log')

x = np.arange(len(id_sort))

#ax.scatter(x, pr_value_sort)
ax.scatter(x, flow_pr_val)


plt.show()


#------------------------------------------------------------------

#------------------------------------------------------------------


# フォントを設定する。
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
ax.set_xlabel("Self PPR value", fontsize=14)
ax.set_ylabel("value of node importance", fontsize=14)

# ax.set_xscale('log')
# ax.set_yscale('log')

self_ppr_list = []
pr_list = []
flow_pr_list = []

for id in self_ppr_dic:
    self_ppr_list.append(self_ppr_dic[id])
    pr_list.append(pr[id])
    flow_pr_list.append(flow_pr[id])


ax.scatter(self_ppr_list, pr_list, label="PR")
ax.scatter(self_ppr_list, flow_pr_list, label = "Proposed")

plt.legend()
plt.tight_layout()
plt.show()



#------------------------------------------------------------------




