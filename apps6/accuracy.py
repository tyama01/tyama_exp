# FP の精度をみてみる

# FP と RW で求めた PPR の実行時間を比較するコード


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

# /usr/bin/python3 /Users/tyama/tyama_exp/apps6/accuracy.py


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

# 各種パラメータ
count = 10**4
alpha = 0.15

#eps = 10**-4
#eps_list = [10**-4, 10**-3, 10**-2, 10**-1]

time_list = []

#------------------------------------------------------------------

#------------------------------------------------------------------

# Self PPR 読み込み

self_ppr_obj = SelfPPR(G)
#ppr_obj = PPR(G)

# {focus_id : self PPR 値}
focus_self_ppr_dic = {}

for node in focus_id_list:
    self_ppr = self_ppr_obj.calc_self_ppr_by_random_walk(source_id=node, alpha=alpha, count=count)
    #self_ppr = ppr_obj.calc_ppr_by_random_walk(source_id=node, alpha=alpha, count=count)
    focus_self_ppr_dic[node] = self_ppr[node]
    
# ソート
focus_self_ppr_sort = sorted(focus_self_ppr_dic.items(), key=lambda x:x[1], reverse=True)

id_sort = []
val_sort = []
for item in focus_self_ppr_sort:
    id_sort.append(item[0])
    val_sort.append(item[1])

#------------------------------------------------------------------

#------------------------------------------------------------------

# FORA で PPR 演算

fora_obj = FORA(G)

# {ノードID : self PPR}
fora_self_ppr = {}

for node in focus_id_list:
    fora_ppr = fora_obj.calc_PPR_by_fora(source_node=node, alpha=alpha, walk_count=count, has_index=False)
    fora_self_ppr[node] = (fora_ppr[node] - alpha) / (1 - alpha)
    
fora_val_sort = []

for id in id_sort:
    fora_val_sort.append(fora_self_ppr[id])


#------------------------------------------------------------------

#------------------------------------------------------------------
# FP

fp_self_ppr = {}

for node in focus_id_list:
    fp_ppr, r_dict = fora_obj.calc_ppr_by_forward_push(source_node=node, alpha=0.15, walk_count=count)
    fp_self_ppr[node] = (fp_ppr[node] - alpha) / (1 - alpha)
    
fp_val_sort = []

for id in id_sort:
    fp_val_sort.append(fp_self_ppr[id])

#------------------------------------------------------------------


#------------------------------------------------------------------
# 精度比較のための前処理

tau, pval = kendalltau(val_sort, fora_val_sort)
print(f"FORA tau : {tau}")


tau, pval = kendalltau(val_sort, fp_val_sort)
print(f"FP tau : {tau}")


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

ax.scatter(x, val_sort, label = "RW")
ax.plot(x, val_sort)

ax.scatter(x, fora_val_sort, label = "FORA")
#ax.plot(x, fora_val_sort)

ax.scatter(x, fp_val_sort, label = "FP")
#ax.plot(x, fp_val_sort)



# グリッドを表示する。
ax.set_axisbelow(True)
ax.grid(True, "major", "x", linestyle="--")
ax.grid(True, "major", "y", linestyle="--")

plt.legend()
plt.tight_layout()
plt.show()


# -----------------------------------------------




