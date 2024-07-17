# エッジ還流度とコミュニティ間エッジの関係をプロット

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


# /usr/bin/python3 /Users/tyama/tyama_exp/apps8/plot_bound_edge.py

# -------------------------- データ読み込み -------------------------
dataset_name = "sbm03"
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

# コミュニティサイズ, 連結性などを調べる

for com_id in c_id:
    print(f"community {com_id} size : {len(c_id[com_id])}")
    
print("-----------------------------------")

    
# Gcc = sorted(nx.connected_components(G), key=len, reverse=True)

# print(len(Gcc))
#print("-----------------------------------")

#------------------------------------------------------------------

#------------------------------------------------------------------
# 還流度読み込み
# self PPR 値を取得 {ノードID : Self PPR 値}
node_selfppr = {}
path = '../alpha_dir/' + dataset_name + '/selfppr_10_01_n.txt' # n の場合は正規化されている
with open(path) as f:
    for line in f:
        (id, val) = line.split()
        node_selfppr[int(id)] = float(val)

#------------------------------------------------------------------

#------------------------------------------------------------------

# エッジ還流度計算

eppr_obj = EPPR(G)


edge_selfppr = eppr_obj.calc_edge_selfppr(node_selfppr=node_selfppr)

print("End Calc Edge_selfPPR")

print(len(edge_selfppr))

x = np.arange(len(edge_selfppr))

#------------------------------------------------------------------

#------------------------------------------------------------------
# 次数 1 のノードを含むエッジ還流度 コミュニティ間エッジの還流度 それ以外のエッジ還流度で場合わけ

# 次数 1 のノードを含むエッジの還流度値リスト 
deg_1_edge_list = np.array([])

# コミュニティ境界のエッジの還流度値リスト
com_bound_edge_list = np.array([])

# 上記以外のエッジ還流度値リスト (次数 1 でないコミュニティ内エッジの還流度値リスト)
other_edge_list = np.array([])

# エッジ還流度が低いやつからリストに追加
# tmp[0]：(エッジ), tmp[1]：還流度値
for tmp in sorted(edge_selfppr.items(), key=lambda x:x[1], reverse=False):
    
    # ２ノードの次数を調査 エッジ(a, b)
    node_a_deg = len(list(G.neighbors(tmp[0][0])))
    node_b_deg = len(list(G.neighbors(tmp[0][1])))
    
    # 次数 1 のノードを含むエッジの場合 -> 還流度値を追加
    # それ以外は nan を追加
    if(node_a_deg == 1 or node_b_deg == 1):
        deg_1_edge_list = np.append(deg_1_edge_list, tmp[1])
        com_bound_edge_list = np.append(com_bound_edge_list, np.nan)
        other_edge_list = np.append(other_edge_list, np.nan)
    
    # コミュニティ間エッジ(=コミュニティラベルが違う)    
    elif(id_c[tmp[0][0]] != id_c[tmp[0][1]]):
        deg_1_edge_list = np.append(deg_1_edge_list, np.nan)
        com_bound_edge_list = np.append(com_bound_edge_list, tmp[1])
        other_edge_list = np.append(other_edge_list, np.nan)
    
    # 上記以外のエッジ還流度値リスト (次数 1 でないコミュニティ内エッジの還流度値リスト)    
    else:
        deg_1_edge_list = np.append(deg_1_edge_list, np.nan)
        com_bound_edge_list = np.append(com_bound_edge_list, np.nan)
        other_edge_list = np.append(other_edge_list, tmp[1])
#------------------------------------------------------------------

#------------------------------------------------------------------
# plot

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
ax.set_xlabel("エッジ (ソート)", fontsize=18)
ax.set_ylabel("エッジ還流度値", fontsize=18)

alpha = 1
range_x = len(edge_selfppr)

ax.scatter(x[:range_x], other_edge_list[:range_x], label="コミュニティ内エッジ(次数1を含まない)", s=10, alpha=alpha)
ax.scatter(x[:range_x], deg_1_edge_list[:range_x], label="次数1を含むエッジ", s=10, alpha=alpha)
ax.scatter(x[:range_x], com_bound_edge_list[:range_x], label="コミュニティ間エッジ", s=10, alpha=alpha)


plt.legend()
plt.tight_layout()
plt.show()

#------------------------------------------------------------------



