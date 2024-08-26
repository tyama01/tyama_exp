# α を変えた場合、NMF によって検出されるコミュニティ境界ノードのコミュニティ所属確率をみる

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

# /usr/bin/python3 /Users/tyama/tyama_exp/apps9/main_check_bound.py

# -------------------------- データ読み込み -------------------------
dataset_name = "sbm03"
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
# 境界ノードの取得

com_bound_node_id = 558

#------------------------------------------------------------------


#------------------------------------------------------------------
# ノード還流度読み込み
# self PPR 値を取得 {ノードID : Self PPR 値}
node_selfppr = {}
path = '../alpha_dir/' + dataset_name + '/selfppr_15_01_n.txt' # n の場合は正規化されている
with open(path) as f:
    for line in f:
        (id, val) = line.split()
        node_selfppr[int(id)] = float(val)

#------------------------------------------------------------------

#------------------------------------------------------------------
# PR 演算
pr = nx.pagerank(G=G, alpha=0.85)

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

#-----------------------------------------------------------------

#-----------------------------------------------------------------
#  着目ノードの所属確率を所得

snmf_obj = SNMF(A)
R = snmf_obj.get_best_Rvec(k=3) 

print(R.shape)
#print(R)

R_normalized = normalize(R, norm='l1', axis=1)

print("Normalized Matrix R (membership probabilities):")

print(R_normalized[com_bound_node_id])
print(R_normalized[com_bound_node_id].shape)

print("-----------------------------------")


# コミュニティの抽出
communities = np.argmax(R, axis=1)

# コミュニティごとにノードをグループ化
node_communities = {}
for node, community in enumerate(communities):
    if community not in node_communities:
        node_communities[community] = []
    node_communities[community].append(node)
    
for com_id in node_communities:
    print(f"community ID {com_id} : {len(node_communities[com_id])}")


#-----------------------------------------------------------------

# #-----------------------------------------------------------------
# # ヒートマッププロット

# plt.figure()
# sns.heatmap([R_normalized[com_bound_node_id]], square=True, cmap='coolwarm', vmin=0, vmax=1)
# plt.show()

# #-----------------------------------------------------------------

