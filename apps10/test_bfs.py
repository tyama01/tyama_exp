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
# BFS 検証
bfs_obj = BFS(G)
dist = bfs_obj.calc_simple_bfs(src_node=0)

print(dist)

#------------------------------------------------------------------
