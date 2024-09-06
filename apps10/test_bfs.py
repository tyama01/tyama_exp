# BFS 実装の確認

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

import japanize_matplotlib

from sklearn.preprocessing import normalize

import pandas as pd

# /usr/bin/python3 /Users/tyama/tyama_exp/apps10/test_bfs.py

# -------------------------- データ読み込み -------------------------
dataset_name = "facebook"
data_loader = DataLoader(dataset_name, is_directed=False)
G = data_loader.get_graph()
print(G) # グラフのノード数、エッジ数出力

Gcc = sorted(nx.connected_components(G), key=len, reverse=True)
print(f"component num : {len(Gcc)}")
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
path = '../alpha_dir/' + dataset_name + '/selfppr_5_01_n.txt' # n の場合は正規化されている
with open(path) as f:
    for line in f:
        (id, val) = line.split()
        node_selfppr[int(id)] = float(val)

#------------------------------------------------------------------

#------------------------------------------------------------------
# FLOW の結果読み込み
alpha = 5

# self_ppr {src_node : {node_id : ppr 値}}

path = '../alpha_dir/' + dataset_name + '/flow_' + str(alpha) + '.pkl'
with open(path, 'rb') as f:
    flow_dic = pickle.load(f)
    
#------------------------------------------------------------------

#------------------------------------------------------------------
# エッジ還流度計算

eppr_obj = EPPR(G)
edge_selfppr = eppr_obj.calc_flow_edge_selfppr(node_selfppr=node_selfppr, flow=flow_dic)

print("End Calc Edge_selfPPR")

#print(edge_selfppr)

#------------------------------------------------------------------

#------------------------------------------------------------------
# BFS 検証
bfs_obj = BFS(G)
#dist = bfs_obj.calc_simple_bfs(src_node=0)

#print(len(dist))
#print("End calc")

Gcc = bfs_obj.get_com_by_bfs_kai(node_selfppr=node_selfppr, edge_selfppr=edge_selfppr, a_ratio=0.2)
print(Gcc)

# print(list(G.neighbors(3987))) # [3980, 4012]
# print(list(G.neighbors(4012))) # [3980, 3987]

#print(list(G.neighbors(3984))) # [3980] 次数 1


#print(list(G.neighbors(3980)))


#print(len(list(G.neighbors(3980))))

# max_edge = (3987, 4012)
# print(edge_selfppr[max_edge])


# base_edge = (3980, 3987)
# print(f"base_edge_selfppr {base_edge} : {edge_selfppr[base_edge]}")

# cnt = 0

# for adj_node in list(G.neighbors(3980)):
    
#     try:
#         edge_selfppr_val = edge_selfppr[(3980, adj_node)]
#     except KeyError:
#         edge_selfppr_val = edge_selfppr[(adj_node, 3980)]
        
#     if(edge_selfppr_val > edge_selfppr[base_edge]):
#         cnt += 1
#         print("---------------------")
#         print(edge_selfppr_val)
#         print("---------------------")
        
        
# print(f"cnt : {cnt}")
        
        


#------------------------------------------------------------------
