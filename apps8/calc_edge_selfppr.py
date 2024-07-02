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


# /usr/bin/python3 /Users/tyama/tyama_exp/apps8/calc_edge_selfppr.py

# -------------------------- データ読み込み -------------------------
dataset_name = "dumbbell"
data_loader = DataLoader(dataset_name, is_directed=False)
G = data_loader.get_graph()
print(G) # グラフのノード数、エッジ数出力
print("-----------------------------------")

node_list = list(G.nodes)
n = len(node_list)
#------------------------------------------------------------------

#------------------------------------------------------------------
# 還流度読み込み
# self PPR 値を取得 {ノードID : Self PPR 値}
node_selfppr = {}
path = '../alpha_dir/' + dataset_name + '/selfppr_15_01_n.txt' # n の場合は正規化されている
with open(path) as f:
    for line in f:
        (id, val) = line.split()
        node_selfppr[int(id)] = float(val)

#------------------------------------------------------------------

#------------------------------------------------------------------
# エッジ還流度を計算

edge_list = list(G.edges())

edge_selfppr = {}

for edge in edge_list:
    
    edge_self_ppr_val = 0
    
    for id in edge:
        edge_self_ppr_val += node_selfppr[id] / len(list(G.neighbors(id)))
        
    edge_selfppr[edge] = edge_self_ppr_val 
#------------------------------------------------------------------

#------------------------------------------------------------------
# txt ファイル出力
path = '../alpha_dir/' + dataset_name + '/edge_selfppr_15_01_n.txt' # n の場合は正規化されている
f = open(path, 'a', encoding='UTF-8')

for tmp in sorted(edge_selfppr.items(), key=lambda x:x[1], reverse=True):
    f.write(str(tmp[0][0]))
    f.write(' ')
    f.write(str(tmp[0][1]))
    f.write(' ')
    f.write(str(tmp[1]))
    f.write('\n')
    
print("End")

#------------------------------------------------------------------




