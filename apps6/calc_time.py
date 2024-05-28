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

# /usr/bin/python3 /Users/tyama/tyama_exp/apps6/calc_time.py


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

time_list = []

#------------------------------------------------------------------

#------------------------------------------------------------------
# RW で PPR 演算

ppr_obj = PPR(G)

start_time = time.perf_counter()
for node in focus_id_list:
    rw_ppr = ppr_obj.calc_ppr_by_random_walk(source_id=node, alpha=alpha, count=count)

execution_time = time.perf_counter() - start_time

print(f"RW PPR time : {execution_time} sec")    
print("-----------------------------------")
time_list.append(execution_time)

#------------------------------------------------------------------


#------------------------------------------------------------------
# tullys PPR
fora_obj = FORA(G)

start_time = time.perf_counter()
for node in focus_id_list:
    fora_ppr = fora_obj.calc_PPR_by_fora(source_node=node, alpha=0.15, walk_count=count, has_index=False)
    
execution_time = time.perf_counter() - start_time

print(f"FORA PPR time : {execution_time} sec")
print("-----------------------------------")

time_list.append(execution_time) 


#------------------------------------------------------------------

#------------------------------------------------------------------
fora_obj_fp = FORA(G)

start_time = time.perf_counter()
for node in focus_id_list:
    fp_ppr, r_dict = fora_obj_fp.calc_ppr_by_forward_push(source_node=node, alpha=0.15, walk_count=count)
    
execution_time = time.perf_counter() - start_time

print(f"FP PPR time : {execution_time} sec")
print("-----------------------------------")

time_list.append(execution_time) 

#------------------------------------------------------------------



# -----------------------------------------------
# プロット

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
#ax.set_yscale('log')

# x軸とy軸のラベルを設定する。
ax.set_xlabel(" Methods", fontsize=14)
ax.set_ylabel("Time (sec)", fontsize=14)


x = [1, 2, 3]
#x = [1, 2]

labels = ["RW", "FORA", "FP"]
#labels = ["RW", "FP"]


plt.xticks(x)
plt.ylim(0,25)

ax.bar(x, time_list, width=0.5, tick_label = labels)


# グリッドを表示する。
ax.set_axisbelow(True)
ax.grid(True, "major", "x", linestyle="--")
ax.grid(True, "major", "y", linestyle="--")

#plt.legend()
plt.tight_layout()
plt.show()


# -----------------------------------------------






