# SBM のおかしな結果を調査

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


# /usr/bin/python3 /Users/tyama/tyama_exp/apps8/test_sbm.py

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

# 部分グラフのリスト
H_list = []

for com_id in c_id:
    print(f"community {com_id} size : {len(c_id[com_id])}")
    H = G.subgraph(c_id[com_id])
    print(H)
    H_list.append(H)
    
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

#------------------------------------------------------------------

#------------------------------------------------------------------


edge_list = []


# エッジ還流度が低いやつからリストに追加
# tmp[0]：(エッジ), tmp[1]：還流度値
for tmp in sorted(edge_selfppr.items(), key=lambda x:x[1], reverse=False):
    
    # ２ノードの次数を調査 エッジ(a, b)
    node_a_deg = len(list(G.neighbors(tmp[0][0])))
    node_b_deg = len(list(G.neighbors(tmp[0][1])))
    
    
    # コミュニティ間エッジ(=コミュニティラベルが違う)    
    if(id_c[tmp[0][0]] != id_c[tmp[0][1]]):
        #edge_list.append(tmp[0])
        print(f"com id : {id_c[tmp[0][0]]}, degree : {node_a_deg} || com id : {id_c[tmp[0][1]]}, degree : {node_b_deg}")
        
#print(len(edge_list))

