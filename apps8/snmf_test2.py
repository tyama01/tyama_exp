# SNMF 仮実装 ver 2

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


# /usr/bin/python3 /Users/tyama/tyama_exp/apps8/snmf_test2.py

#------------------------------------------------------------------

def snmf(A, n_components, max_iter=200, tol=1e-4, random_state=None):
    if random_state is not None:
        np.random.seed(random_state)
    
    n = A.shape[0]
    R = np.random.rand(n, n_components)
    
    for iteration in range(max_iter):
        R_old = R.copy()
        
        numerator = A @ R
        denominator = R @ (R.T @ R) + 1e-9
        
        R *= numerator / denominator
        
        if np.linalg.norm(R - R_old, 'fro') < tol:
            break

    return R

def best_snmf(A, n_components, max_iter=200, tol=1e-4, n_runs=10):
    best_R = None
    best_obj_value = float('inf')
    
    for i in range(n_runs):
        R = snmf(A, n_components, max_iter, tol, random_state=i)
        
        obj_value = np.linalg.norm(A - R @ R.T, 'fro')
        
        if obj_value < best_obj_value:
            best_obj_value = obj_value
            best_R = R

    return best_R


#------------------------------------------------------------------

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

# 最適なSNMFを適用して行列Rを取得
R = best_snmf(A, n_components)

print(R.shape)
#print(R)

R_normalized = normalize(R, norm='l1', axis=1)

print("Normalized Matrix R (membership probabilities):")
# print(R_normalized)

# # 各ノードのコミュニティ所属確率の表示
# for node in range(R_normalized.shape[0]):
#     print(f"Node {node}: {R_normalized[node]}")

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
    
#print(node_communities)
    
part = []

for com_id in node_communities:
    part.append(node_communities[com_id])
    
for i in range(len(part)):
    H = G.subgraph(part[i])
    Gcc = sorted(nx.connected_components(H), key=len, reverse=True)
    print(f"component num : {len(Gcc)}")
    
    
print(nx.community.modularity(G, part))

for i in range(len(part)):
    print(f"conductance {len(part[i])} : {nx.conductance(G, part[i])}")
    



#------------------------------------------------------------------
