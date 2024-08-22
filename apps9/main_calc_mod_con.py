# tyama 手法のモジュラリティとコンダクタンスを調査

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

# /usr/bin/python3 /Users/tyama/tyama_exp/apps9/main_calc_mod_con.py

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

pr = nx.pagerank(G=G, alpha=0.9)

# エッジ還流度計算

eppr_obj = EPPR(G)


edge_selfppr = eppr_obj.calc_edge_selfppr(node_selfppr=node_selfppr)

print("End Calc Edge_selfPPR")

print(len(edge_selfppr))

#------------------------------------------------------------------

#------------------------------------------------------------------
# NMF を適用

# 隣接行列を取得
A = data_loader.get_adj_matrix(is_directed=False)
print("Complete convert G to A")

# 還流度行列
S = data_loader.get_adj_matrix(is_directed=False)
#S = nx.to_numpy_array(G)
for tmp in sorted(edge_selfppr.items(), key=lambda x:x[1], reverse=False):
    S[tmp[0][0]][tmp[0][1]] = tmp[1]
    S[tmp[0][1]][tmp[0][0]] = tmp[1]
    
snmf_obj = SNMF(A)
R = snmf_obj.get_best_Rvec(k=16) 

print(R.shape)
#print(R)

R_normalized = normalize(R, norm='l1', axis=1)

print("Normalized Matrix R (membership probabilities):")

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
    

part = []

for com_id in node_communities:
    part.append(node_communities[com_id])
    
for i in range(len(part)):
    H = G.subgraph(part[i])
    Gcc = sorted(nx.connected_components(H), key=len, reverse=True)
    print(f"component num {len(part[i])} : {len(Gcc)}")
    
# モジュラリティ計算    
print(f"modularity : {nx.community.modularity(G, part)}")

# コンダクタンス計算
for i in range(len(part)):
    print(f"conductance {len(part[i])} : {nx.conductance(G, part[i])}")


#------------------------------------------------------------------
