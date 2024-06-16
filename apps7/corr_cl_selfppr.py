# クラスタリング係数と還流度の相関

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


# /usr/bin/python3 /Users/tyama/tyama_exp/apps7/corr_cl_selfppr.py

# -------------------------- データ読み込み -------------------------
dataset_name = "facebook"
data_loader = DataLoader(dataset_name, is_directed=False)
G = data_loader.get_graph()
print(G) # グラフのノード数、エッジ数出力

print("-----------------------------------")

node_list = list(G.nodes)
n = len(node_list)
#------------------------------------------------------------------

#------------------------------------------------------------------

# self ppr 読み込み

alpha = 15

# {ID : 還流度}
self_ppr_val = {}

# self PPR 値を取得 {ノードID : Self PPR 値}
self_ppr_val = {}
path = '../alpha_dir/' + dataset_name + '/selfppr_15_01.txt'
with open(path) as f:
    for line in f:
        (id, val) = line.split()
        self_ppr_val[int(id)] = float(val)
    
# 正規化
self_ppr_sum = 0

for src in self_ppr_val:
    self_ppr_sum += self_ppr_val[src]
    
for src_node in self_ppr_val:
        self_ppr_val[src_node] /=  self_ppr_sum
        
self_ppr_sort = sorted(self_ppr_val.items(), key=lambda x:x[1], reverse=True)

self_ppr_id_sort = []
self_ppr_val_sort = []

for item in self_ppr_sort:
    
    self_ppr_id_sort.append(item[0])
    self_ppr_val_sort.append(item[1])


#------------------------------------------------------------------

#------------------------------------------------------------------
# クラスタリング係数読み込み

clustering_dic = {}

path = '../clustering_dir/' + dataset_name + '_clustering.txt'
with open(path) as f:
    for line in f:
        (id, val) = line.split()
        clustering_dic[int(id)] = float(val)
        
clustering_val = []

for id in self_ppr_id_sort:
    clustering_val.append(clustering_dic[id])



#------------------------------------------------------------------

#------------------------------------------------------------------
# plot 縦軸： Self PPR 値の増減比

# フォントを設定する。
rcp['font.family'] = 'sans-serif'
rcp['font.sans-serif'] = ['Hiragino Maru Gothic Pro', 'Yu Gothic', 'Meirio', 'Takao', 'IPAexGothic', 'IPAPGothic', 'VL PGothic', 'Noto Sans CJK JP']

# カラーマップを用意する。
cmap = plt.get_cmap("tab10")

# Figureを作成する。
fig = plt.figure()
# Axesを作成する。
ax = fig.add_subplot(111)

# Figureの解像度と色を設定する。
fig.set_dpi(150)
fig.set_facecolor("white")

# Axesのタイトルと色を設定する。
#ax.set_title("物品の所有率")
ax.set_facecolor("white")

ax.set_xscale('log')
#ax.set_yscale('log')

# x軸とy軸のラベルを設定する。
ax.set_xlabel(r"還流度 ($\alpha$=0.15)", fontsize=14)
ax.set_ylabel("クラスタリング係数", fontsize=14)

ax.scatter(self_ppr_val_sort, clustering_val)

s1 = pd.Series(self_ppr_val_sort)
s2 = pd.Series(clustering_val)

res = s1.corr(s2)

print(res)



#plt.xlim(0.0002, 0.0005)

#plt.xlim(0, 10**-3)


#plt.xticks(x)
#plt.ylim(0,1)


# グリッドを表示する。
ax.set_axisbelow(True)
ax.grid(True, "major", "x", linestyle="--")
ax.grid(True, "major", "y", linestyle="--")

plt.legend(loc='upper left', bbox_to_anchor=(1, 1))
plt.tight_layout()
plt.show()


#------------------------------------------------------------------