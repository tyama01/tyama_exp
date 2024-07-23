# エッジ還流度とエッジを結ぶノード間の次数をプロット

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


# /usr/bin/python3 /Users/tyama/tyama_exp/apps8/edge_selfppr_heatmap.py

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

for com_id in c_id:
    print(f"community {com_id} size : {len(c_id[com_id])}")
    
print("-----------------------------------")

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
# numpy 配列にエッジ還流度の値を格納

array = np.zeros((n, n))

for tmp in sorted(edge_selfppr.items(), key=lambda x:x[1], reverse=False):    
    array[tmp[0][0]][tmp[0][1]] = tmp[1]
    array[tmp[0][1]][tmp[0][0]] = tmp[1]
    


#------------------------------------------------------------------

#------------------------------------------------------------------
# ヒートマップ生成

plt.figure()
sns.heatmap(array, square=True, cmap='afmhot')
plt.show()

#------------------------------------------------------------------




