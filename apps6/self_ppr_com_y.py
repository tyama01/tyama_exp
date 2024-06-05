# コミュニティごとでの SelfPPR の相関を見るコード

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

import pandas as pd



# /usr/bin/python3 /Users/tyama/tyama_exp/apps6/self_ppr_com_y.py

# -------------------------- データ読み込み -------------------------
dataset_name = "facebook"
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
# selfPPR の結果読み込み
alpha = 15

# self_ppr {src_node : {node_id : ppr 値}}

path = '../alpha_dir/' + dataset_name + '/self_ppr_' + str(alpha) + '.pkl'
with open(path, 'rb') as f:
    self_ppr = pickle.load(f)

# self PPR 値を取得 {ノードID : Self PPR 値}
self_ppr_val = {}

for src_node in self_ppr:
    self_ppr_val[src_node] = self_ppr[src_node][src_node]
    

# 正規化
self_ppr_sum = 0

for src_node in self_ppr_val:
    self_ppr_sum += self_ppr_val[src_node]
    
for src_node in self_ppr_val:
    self_ppr_val[src_node] /= self_ppr_sum
    
#------------------------------------------------------------------

#------------------------------------------------------------------
# コミュニティごとの PR を計算

# コミュニティごとの PR 
# {com_id : PR 値}
com_pr = {}

total = 0

for com_id in c_id:
    
    # そのコミュニティの部分グラフ
    H = G.subgraph(c_id[com_id])
    n_H = len(list(H.nodes))
    
    com_pr[com_id] = nx.pagerank(H, alpha=0.85)
    
    # com_pr_before = nx.pagerank(H, alpha=0.85)
    
    # # for id in com_pr_before:
    # #     com_pr_before[id] =  com_pr_before[id] / n_H
            
    # #  正規化
    # com_before_sum = 0
    # for id in com_pr_before:
    #     com_before_sum += com_pr_before[id]
        
    # total += com_before_sum
        
    # com_pr_after = {}
        
    # for id in com_pr_before:
    #     com_pr_after[id] = com_pr_before[id] / com_before_sum
        
    # com_pr[com_id] = com_pr_before
    

# for com_id in c_id:
    
#     for id in com_pr[com_id]:
        
#         com_pr[com_id][id] /= total
    

#------------------------------------------------------------------




#------------------------------------------------------------------
# Self PPR と ComPR の値を一致させる

# {com_id : [Self PPR値]}
per_com_self_ppr_dic = {com_id : [] for com_id in c_id}

for com_id in c_id:
    for id in com_pr[com_id]:
        per_com_self_ppr_dic[com_id].append(self_ppr_val[id])

#{com_id : [ComPR値]}
per_com_pr_dic = {com_id : [] for com_id in c_id}

for com_id in c_id:
    for id in com_pr[com_id]:
        per_com_pr_dic[com_id].append(com_pr[com_id][id])

#------------------------------------------------------------------


#------------------------------------------------------------------
# plot 縦軸： ComPR 値, 横軸： SelfPPR

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

# ax.set_xscale('log')
ax.set_yscale('log')


# x軸とy軸のラベルを設定する。
ax.set_xlabel(r"還流度 ($\alpha$=0.15)", fontsize=14)
ax.set_ylabel(r"ComPR($\alpha$=0.15)", fontsize=14)


y = []
for i in range(len(c_id)):
    y.append(len(c_id[i]))

z = np.sort(y)[::-1]
labels_data = np.argsort(y)[::-1]
labels_data = labels_data.tolist()

#plt.xticks(x)
#plt.ylim(0,1)

for com_id in labels_data:
    ax.scatter(per_com_self_ppr_dic[com_id], per_com_pr_dic[com_id], label = str(com_id))
    
    s1 = pd.Series(per_com_self_ppr_dic[com_id])
    s2 = pd.Series(per_com_pr_dic[com_id])
        
    res = s1.corr(s2)
    print(f"{com_id} : {res}")


# com_id = 1
# ax.scatter(per_com_self_ppr_dic[com_id], per_com_pr_dic[com_id], label = str(com_id))

# グリッドを表示する。
ax.set_axisbelow(True)
ax.grid(True, "major", "x", linestyle="--")
ax.grid(True, "major", "y", linestyle="--")

plt.legend()
plt.tight_layout()
plt.show()


#------------------------------------------------------------------