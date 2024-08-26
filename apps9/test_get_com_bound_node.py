# コミュニティ境界ノード取得のテストコード

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

# /usr/bin/python3 /Users/tyama/tyama_exp/apps9/test_get_com_bound_node.py

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

for com_id in c_id:
    print(f"コミュニティラベル {com_id} のノード数: {len(c_id[com_id])}")

print("-----------------------------------")

node_list = list(G.nodes)
n = len(node_list)

edge_list = list(G.edges())

#print(edge_list)

#------------------------------------------------------------------

#------------------------------------------------------------------
# コミュニティ境界ノード取得

com_bound_dic = data_loader.get_bound_node()

#print(com_bound_dic)

v_deg, v_belong_com, com_bound_deg_dic = data_loader.get_node_info(558)

print(f"次数:{v_deg}")
print(f"所属コミュニティ:{v_belong_com}")
print(com_bound_deg_dic)

#------------------------------------------------------------------
