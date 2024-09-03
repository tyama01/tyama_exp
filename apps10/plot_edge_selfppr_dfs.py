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

import japanize_matplotlib

from sklearn.preprocessing import normalize

import pandas as pd

# /usr/bin/python3 /Users/tyama/tyama_exp/apps10/plot_edge_selfppr_dfs.py

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

#print(edge_selfppr)

#------------------------------------------------------------------

#------------------------------------------------------------------
# dfs した際の仮の経路

sample_dfs_list = [(0, 1), (0, 2), (2, 3), (3, 4), (4, 10), (10, 6), (6, 7)]

sample_edge_selfppr_val_list = []

for edge in sample_dfs_list:
    
    # 無向グラフでの例外処理
    try: # キーがエッジだが、(3, 0) がキーにある場合(0, 3) がないので両方対応するため
        sample_edge_selfppr_val_list.append(edge_selfppr[edge])
    except KeyError:
        sample_edge_selfppr_val_list.append(edge_selfppr[(edge[1], edge[0])])
     
hop_num_list = [i for i in range(1, len(sample_edge_selfppr_val_list) + 1)] 
 
#------------------------------------------------------------------

#------------------------------------------------------------------
# plot

sns.set()
sns.set(font='IPAexGothic')

# Figureを作成する。
fig = plt.figure(figsize=(8, 6))
# Axesを作成する。
ax = fig.add_subplot(111)

fig.set_dpi(150)

# x軸とy軸のラベルを設定する。
ax.set_xlabel("Hop 数", fontsize=20)
ax.set_ylabel("エッジ還流度", fontsize=20)

#labelsizeで軸の数字の文字サイズ変更
plt.tick_params(labelsize=18)

# グラフ装飾用カラー

# cool
# jet
# spring
# summer
# autumn
# winter


cm = plt.get_cmap("cool")


ax.scatter(hop_num_list, sample_edge_selfppr_val_list, color=cm(500))
ax.plot(hop_num_list, sample_edge_selfppr_val_list, color=cm(500))

plt.tight_layout()
plt.show()
#plt.savefig('../apps10/plot/wheel_edge_selfppr_dfs.pdf')

#------------------------------------------------------------------


