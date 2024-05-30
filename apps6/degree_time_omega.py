# 提案手法の delta の使い分けを考えるためにとる評価
# 横軸：次数, 縦軸： time, omega

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

# /usr/bin/python3 /Users/tyama/tyama_exp/apps6/degree_time_omega.py

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

# 次数のリスト
degree_list = []

for node in focus_id_list:
    degree_list.append(G.degree[node])

#------------------------------------------------------------------

#------------------------------------------------------------------
# Proposed 1 delata = alpha
self_ppr_obj = FORA(G)

self_ppr_time_list = list()
self_ppr_omega_list = list()

for node in focus_id_list:
    
    # 計測開始
    start_time = time.perf_counter()
    
    omega = calc_omega(delta=alpha, n=n)
    self_ppr_omega_list.append(omega)
    self_ppr = self_ppr_obj.calc_PPR_by_fora(source_node=node, alpha=0.15, walk_count=omega, has_index=False)
    
    # 計測終了
    execution_time = time.perf_counter() - start_time
    
    self_ppr_time_list.append(execution_time)

#------------------------------------------------------------------

#------------------------------------------------------------------
# Proposed 2 delata = X
self_ppr_x_obj = FORA(G)

self_ppr_x_time_list = list()
self_ppr_x_omega_list = list()


for node in focus_id_list:
    
    # 計測開始
    start_time = time.perf_counter()
    
    delta = self_ppr_x_obj.determine_delta(source_node=node, alpha=alpha)
    omega = calc_omega(delta=delta, n=n)
    self_ppr_x_omega_list.append(omega)
    self_ppr_x = self_ppr_x_obj.calc_PPR_by_fora(source_node=node, alpha=0.15, walk_count=omega, has_index=False)
    
    # 計測終了
    execution_time = time.perf_counter() - start_time
    
    self_ppr_x_time_list.append(execution_time)


#------------------------------------------------------------------

# -----------------------------------------------
# プロット 計測時間

s1 = 100
s2 = 30

alpha = 0.4

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
ax.set_xlabel(" degree", fontsize=14)
ax.set_ylabel("Time (sec)", fontsize=14)

ax.scatter(degree_list, self_ppr_time_list, label="Proposed_1", marker="_", s=s1)
ax.scatter(degree_list, self_ppr_x_time_list, label="Proposed_2", s=s2, alpha=alpha)



# グリッドを表示する。
ax.set_axisbelow(True)
ax.grid(True, "major", "x", linestyle="--")
ax.grid(True, "major", "y", linestyle="--")

plt.legend()
plt.tight_layout()
plt.show()


# -----------------------------------------------

# -----------------------------------------------
# プロット 計測時間

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
ax.set_xlabel("degree", fontsize=14)
ax.set_ylabel("omega", fontsize=14)

ax.scatter(degree_list, self_ppr_omega_list, label="Proposed_1", marker="_", s=s1)
ax.scatter(degree_list, self_ppr_x_omega_list, label="Proposed_2", s=s2, alpha=alpha)



# グリッドを表示する。
ax.set_axisbelow(True)
ax.grid(True, "major", "x", linestyle="--")
ax.grid(True, "major", "y", linestyle="--")

plt.legend()
plt.tight_layout()
plt.show()


# -----------------------------------------------