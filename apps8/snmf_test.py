# SNMF 仮実装

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


# /usr/bin/python3 /Users/tyama/tyama_exp/apps8/snmf_test.py

#------------------------------------------------------------------

def snmf(A, n_components, max_iter=200, tol=1e-10):
    n = A.shape[0]
    
    # ランダム初期化
    R = np.random.rand(n, n_components)

    for iteration in range(max_iter):
        R_old = R.copy()
        
        # 更新ルールに基づいて R を更新
        numerator = A @ R
        denominator = R @ (R.T @ R) + 1e-9  # 0での除算を防ぐために小さい値を加える
        
        R *= numerator / denominator
        
        # 収束判定
        if np.linalg.norm(R - R_old, 'fro') < tol:
            break

    return R

#------------------------------------------------------------------


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

#------------------------------------------------------------------
# 演算してみる

A = nx.to_numpy_array(G)
print("-----------------------------------")


# コミュニティ数（低ランク近似のランク）
n_components = 3
# SNMFを適用して行列Rを取得
R = snmf(A, n_components)
print("-----------------------------------")


print(R.shape)
print("-----------------------------------")

# コミュニティの抽出
communities = np.argmax(R, axis=1)

#print(communities)

# コミュニティごとにノードをグループ化
node_communities = {}
for node, community in enumerate(communities):
    if community not in node_communities:
        node_communities[community] = []
    node_communities[community].append(node)
    
#print(node_communities)

for com_id in node_communities:
    print(f"{com_id} : {len(node_communities[com_id])}")
    
part = []

for com_id in node_communities:
    part.append(node_communities[com_id])
    
print(nx.community.modularity(G, part))

for i in range(len(part)):
    print(f"conductance {len(part[i])} : {nx.conductance(G, part[i])}")
    



#------------------------------------------------------------------
