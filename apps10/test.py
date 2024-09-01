# FLOW を pickle ファイルで出力

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

# /usr/bin/python3 /Users/tyama/tyama_exp/apps10/test.py

# -------------------------- データ読み込み -------------------------
dataset_name = "wheel"
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

print(edge_selfppr)

#------------------------------------------------------------------
