# FORA との Self PPR の精度

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
import time
import math

# /usr/bin/python3 /Users/tyama/tyama_exp/apps6/accuracy_x.py

#------------------------------------------------------------------
# RWer 数決定

def calc_omega(delta, n):
    
    # 各種パラメータ
    Pf = 1/n
    eps = 0.1
    
    omega = (4 * math.log(1/Pf)) / ((eps**2) * delta)
    
    return math.ceil(omega)
    


#------------------------------------------------------------------


# -------------------------- データ読み込み -------------------------
#dataset_name = input("Enter the dataset name: ")
dataset_name = "facebook"
data_loader = DataLoader(dataset_name, is_directed=False)
G = data_loader.get_graph()
print(G) # グラフのノード数、エッジ数出力


print("-----------------------------------")

node_list = list(G.nodes)
n = len(node_list)
#------------------------------------------------------------------

#------------------------------------------------------------------
# 前準備

# 着目ノード
seed_node = 0

focus_id_list = list(G.neighbors(seed_node))
print(f"seed node ID : {seed_node}, degree : {len(focus_id_list)}")
print("-----------------------------------")


# 着目ノードとその隣接を含めたノード群
focus_id_list.append(seed_node)

# RW の終了確率
alpha = 0.15


time_list = []

#------------------------------------------------------------------


#------------------------------------------------------------------
# FORA
fora_obj = FORA(G)

# {ノードID : self PPR}
fora_self_ppr = {}



for node in focus_id_list:
    omega = calc_omega(delta=1/n, n=n)
    fora_ppr = fora_obj.calc_PPR_by_fora(source_node=node, alpha=0.15, walk_count=omega, has_index=False)
    fora_self_ppr[node] = (fora_ppr[node] - alpha) / (1 - alpha)
    
fora_self_ppr_sort = sorted(fora_self_ppr.items(), key=lambda x:x[1], reverse=True)

print(omega)

id_sort = []
val_sort = []

for item in fora_self_ppr_sort:
    id_sort.append(item[0])
    val_sort.append(item[1])


#------------------------------------------------------------------

#------------------------------------------------------------------
# Proposed
self_ppr = {}

self_obj = FORA(G)

for node in focus_id_list:
    omega = calc_omega(delta=alpha, n=n)
    tyama_self_ppr = self_obj.calc_PPR_by_fora(source_node=node, alpha=0.15, walk_count=omega, has_index=False)
    self_ppr[node] = (tyama_self_ppr[node] - alpha) / (1 - alpha)

print(omega)
    
  
self_ppr_val_sort = []   
for id in id_sort:
    self_ppr_val_sort.append(self_ppr[id])
    
    


#------------------------------------------------------------------

#------------------------------------------------------------------
# 精度比較のための前処理

tau, pval = kendalltau(val_sort, self_ppr_val_sort)
print(f"SELF tau : {tau}")

#------------------------------------------------------------------

# -----------------------------------------------
# Self PPR 値 プロット

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

#ax.set_xscale('log')
ax.set_yscale('log')

# x軸とy軸のラベルを設定する。
ax.set_xlabel("Rank (RW sort)", fontsize=14)
ax.set_ylabel("Self PPR value", fontsize=14)




#plt.xticks(eps_list)
#plt.ylim(-1,1)
x = [i for i in range(len(id_sort))]

ax.scatter(x, val_sort, label = "answer")
ax.plot(x, val_sort)

ax.scatter(x, self_ppr_val_sort, label = "Proposed")
#ax.plot(x, fora_val_sort)




# グリッドを表示する。
ax.set_axisbelow(True)
ax.grid(True, "major", "x", linestyle="--")
ax.grid(True, "major", "y", linestyle="--")

plt.legend()
plt.tight_layout()
plt.show()


# -----------------------------------------------





