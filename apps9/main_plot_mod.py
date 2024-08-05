# 分割数とモジュラリティをプロット

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

from sklearn.preprocessing import normalize

import pandas as pd

# /usr/bin/python3 /Users/tyama/tyama_exp/apps9/main_plot_mod.py

# -------------------------- データ読み込み -------------------------
dataset_name = "facebook"
data_loader = DataLoader(dataset_name, is_directed=False)
G = data_loader.get_graph()
print(G) # グラフのノード数、エッジ数出力

Gcc = sorted(nx.connected_components(G), key=len, reverse=True)
print(f"component num : {len(Gcc)}")
    

data_loader.load_community()

# {所属するコミュニティ：頂点idのリスト}, {頂点id:所属するコミュニティ}
c_id, id_c = data_loader.get_communities() 

print("-----------------------------------")

node_list = list(G.nodes)
n = len(node_list)

edge_list = list(G.edges())

#print(edge_list)

#------------------------------------------------------------------

#------------------------------------------------------------------
# ノード還流度読み込み
# self PPR 値を取得 {ノードID : Self PPR 値}
node_selfppr = {}
path = '../alpha_dir/' + dataset_name + '/selfppr_10_01_n.txt' # n の場合は正規化されている
with open(path) as f:
    for line in f:
        (id, val) = line.split()
        node_selfppr[int(id)] = float(val)

#------------------------------------------------------------------

#------------------------------------------------------------------
# PR 演算
pr = nx.pagerank(G=G, alpha=0.9)

#------------------------------------------------------------------

#------------------------------------------------------------------

# エッジ還流度計算

eppr_obj = EPPR(G)

edge_pr = eppr_obj.calc_edge_selfppr(node_selfppr=pr)

edge_selfppr = eppr_obj.calc_edge_selfppr(node_selfppr=node_selfppr)


print("End Calc Edge_selfPPR")

#------------------------------------------------------------------

#------------------------------------------------------------------
# 隣接行列取得

# 隣接行列を取得
A = data_loader.get_adj_matrix(is_directed=False)
print("Complete convert G to A")

# PR 行列
P = data_loader.get_adj_matrix(is_directed=False)
for tmp in sorted(edge_pr.items(), key=lambda x:x[1], reverse=False):
    P[tmp[0][0]][tmp[0][1]] = tmp[1]
    P[tmp[0][1]][tmp[0][0]] = tmp[1]

# 還流度行列
S = data_loader.get_adj_matrix(is_directed=False)
for tmp in sorted(edge_selfppr.items(), key=lambda x:x[1], reverse=False):
    S[tmp[0][0]][tmp[0][1]] = tmp[1]
    S[tmp[0][1]][tmp[0][0]] = tmp[1]

#------------------------------------------------------------------

#------------------------------------------------------------------
# NMF を適用

# モジュラリティを格納しとく 辞書型 {行列 : [モジュラリティ値]}
array_dict = {'A':A, 'P':P, 'S':S}
mod_dict = {'A':[0, 0], 'P':[0, 0], 'S':[0, 0]}

# 分割数
k = 20

# louvain mod値
part = []

for com_id in c_id:
    part.append(c_id[com_id])
louvain_mod = nx.community.modularity(G, part)
louvain_mod_list = []

for _ in range(k+1):
    louvain_mod_list.append(louvain_mod)

for array in array_dict:
    for tmp_k in range(2, k+1): 
        
        snmf_obj = SNMF(array_dict[array])
        R = snmf_obj.get_best_Rvec(k=tmp_k)
        R_normalized = normalize(R, norm='l1', axis=1)
        
        # コミュニティの抽出
        communities = np.argmax(R, axis=1)
        
        # コミュニティごとにノードをグループ化
        node_communities = {}
        for node, community in enumerate(communities):
            if community not in node_communities:
                node_communities[community] = []
            node_communities[community].append(node)
            
        
        part = []

        for com_id in node_communities:
            part.append(node_communities[com_id])
            
        mod_dict[array].append(nx.community.modularity(G, part))
        print(nx.community.modularity(G, part))


#------------------------------------------------------------------

#------------------------------------------------------------------
# プロット

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

#ax.set_xscale('log')
#ax.set_yscale('log')

# x軸とy軸のラベルを設定する。
ax.set_xlabel("コミュニティ分割数 k", fontsize=20)
ax.set_ylabel("Modularity", fontsize=20)

x_list = [i for i in range(len(louvain_mod_list))]


ax.plot(x_list, louvain_mod_list, "_", label="Louvain", c="r")

ax.scatter(x_list, mod_dict['A'], label="隣接行列", c="m")
ax.plot(x_list, mod_dict['A'], c="m")

ax.scatter(x_list, mod_dict['P'], label="PR行列", c="g")
ax.plot(x_list, mod_dict['P'], c="g")


ax.scatter(x_list, mod_dict['S'], label="還流度行列", c="b")
ax.plot(x_list, mod_dict['S'], c="b")

# グリッドを表示する。
ax.set_axisbelow(True)
ax.grid(True, "major", "x", linestyle="--")
ax.grid(True, "major", "y", linestyle="--")

pos_x = [i for i in range(0, k+1)]
pos_y = [i/10 for i in range(0, 11)]

ax.set_xticks(pos_x)
ax.set_yticks(pos_y)

plt.legend()
plt.legend(loc='upper left', bbox_to_anchor=(1, 1))

plt.tight_layout()
plt.show()

#------------------------------------------------------------------






