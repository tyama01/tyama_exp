# コミュニティ内エッジのエッジ還流度分布を箱ひげ図でプロット
# できればコミュニティサイズ順にソート ラベルがコミュニティサイズ

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

# /usr/bin/python3 /Users/tyama/tyama_exp/apps9/main_boxplot_edge_selfppr.py

# -------------------------- データ読み込み -------------------------
dataset_name = "facebook"
data_loader = DataLoader(dataset_name, is_directed=False)
G = data_loader.get_graph()
print(G) # グラフのノード数、エッジ数出力

Gcc = sorted(nx.connected_components(G), key=len, reverse=True)
print(f"component num : {len(Gcc)}")

edge_list = list(G.edges())
print(len(edge_list))

#print(list(G.neighbors(3437)))


# edge = (3437, 698)
# print(edge in edge_list)
# print("aaaaaaaa")
    

data_loader.load_community()

# {所属するコミュニティ：頂点idのリスト}, {頂点id:所属するコミュニティ}
c_id, id_c = data_loader.get_communities() 

print("-----------------------------------")

node_list = list(G.nodes)
n = len(node_list)
print(n)

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

# 各手法のコミュニティ部分グラフを生成

#------------------------------------------------------------------


# Louvain 手法

# # {コミュニティラベル : 部分グラフ}
# com_G_dic = {}

# for com_id in c_id:
#     com_G_dic[com_id] = G.subgraph(c_id[com_id])
    
#------------------------------------------------------------------

# NMF 手法

# {コミュニティラベル : 部分グラフ}
com_G_dic = {}

k = 16

snmf_obj = SNMF(S)
R = snmf_obj.get_best_Rvec(k=k) 

R_normalized = normalize(R, norm='l1', axis=1)

# コミュニティの抽出
communities = np.argmax(R, axis=1)

# コミュニティごとにノードをグループ化
node_communities = {}
for node, community in enumerate(communities):
    if community not in node_communities:
        node_communities[community] = []
    node_communities[community].append(node)
    
for com_id in node_communities:
    com_G_dic[com_id] = G.subgraph(node_communities[com_id])

#------------------------------------------------------------------

#------------------------------------------------------------------
# コミュニティ内エッジ還流度を保管

# {com_id : [エッジ還流度]} 
edge_flow_dic = {com_id : [] for com_id in com_G_dic}

for com_id in com_G_dic:
    com_edge_list = list(com_G_dic[com_id].edges())
    
    for tmp_edge in com_edge_list:
        if(tmp_edge in edge_list):
            edge_flow_dic[com_id].append(edge_selfppr[tmp_edge])
        else:
            continue
        

#------------------------------------------------------------------

#------------------------------------------------------------------
# 箱ひげ図プロット

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
ax.set_xlabel("コミュニティサイズ", fontsize=20)
ax.set_ylabel("エッジ還流度の値", fontsize=20)


# コミュニティラベル大きい順
y = []
for i in range(len(com_G_dic)):
    y.append(len(com_G_dic[i]))
z = np.sort(y)[::-1]
labels_data = np.argsort(y)[::-1]
labels_data = labels_data.tolist()

# 小さい順
#labels_data.reverse()

com_size_list = []
for com_id in labels_data:
    com_size_list.append(len(com_G_dic[com_id]))
    
#print(com_size_list)

data = []
for com_id in labels_data:
    data.append(edge_flow_dic[com_id])

ax.boxplot(data)

# ラベル表示
ax.set_xticklabels(com_size_list, fontsize=20)


# グリッドを表示する。
ax.set_axisbelow(True)
ax.grid(True, "major", "x", linestyle="--")
ax.grid(True, "major", "y", linestyle="--")


plt.tight_layout()
plt.show()

#------------------------------------------------------------------