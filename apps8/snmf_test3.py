# SNMF 仮実装 ver 3

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
from scipy.sparse.csgraph import connected_components
from sklearn.decomposition import NMF
import pandas as pd


# /usr/bin/python3 /Users/tyama/tyama_exp/apps8/snmf_test3.py

#------------------------------------------------------------------


#------------------------------------------------------------------

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

# エッジ還流度計算

eppr_obj = EPPR(G)


edge_selfppr = eppr_obj.calc_edge_selfppr(node_selfppr=node_selfppr)

print("End Calc Edge_selfPPR")

#------------------------------------------------------------------



#------------------------------------------------------------------
# 演算してみる

A = nx.to_numpy_array(G)

for tmp in sorted(edge_selfppr.items(), key=lambda x:x[1], reverse=False):    
    A[tmp[0][0]][tmp[0][1]] = tmp[1] * 100000000000000
    A[tmp[0][1]][tmp[0][0]] = tmp[1] * 100000000000000
print("-----------------------------------")

n_components = 20

model = NMF(n_components=n_components, init='random', random_state=42)
R = model.fit_transform(A)
H = model.components_

print(R.shape)
print(R)

R_normalized = normalize(R, norm='l1', axis=1)

print("Normalized Matrix R (membership probabilities):")
print(R_normalized)

# 各ノードのコミュニティ所属確率の表示
for node in range(R_normalized.shape[0]):
    print(f"Node {node}: {R_normalized[node]}")


# コミュニティの抽出
# W 行列の各行に対して最大値のインデックスを取ることで、ノードがどのコミュニティに属するかを決定
communities = np.argmax(R, axis=1)


# コミュニティごとにノードをグループ化
node_communities = {}
for node, community in enumerate(communities):
    if community not in node_communities:
        node_communities[community] = []
    node_communities[community].append(node)
    
# 非連結コミュニティを連結成分ごとに分割
connected_components_list = []
for community, nodes in node_communities.items():
    subgraph = G.subgraph(nodes)
    connected_components = list(nx.connected_components(subgraph))
    connected_components_list.extend(connected_components)

# 再度マージして指定した数のコミュニティ数にする
new_node_communities = {i: [] for i in range(n_components)}
for i, component in enumerate(connected_components_list):
    target_community = i % n_components
    new_node_communities[target_community].extend(component)
    
for com_id in new_node_communities:
    print(f"{com_id} : {len(new_node_communities[com_id])}")
    
part = []

for com_id in new_node_communities:
    part.append(new_node_communities[com_id])
    
for i in range(len(part)):
    H = G.subgraph(part[i])
    Gcc = sorted(nx.connected_components(H), key=len, reverse=True)
    print(f"component num : {len(Gcc)}")
    
    
print(nx.community.modularity(G, part))

for i in range(len(part)):
    print(f"conductance {len(part[i])} : {nx.conductance(G, part[i])}")
    



#------------------------------------------------------------------
