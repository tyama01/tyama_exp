# コミュニティごとでの SelfPPR の相関を見るコード

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


# /usr/bin/python3 /Users/tyama/tyama_exp/apps6/com_change_fc.py
 

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
# 前準備

# 着目ノード
seed_node = 0

focus_id_list = list(G.neighbors(seed_node))
print(f"seed node ID : {seed_node}, degree : {len(focus_id_list)}")
print("-----------------------------------")


# 着目ノードとその隣接を含めたノード群
focus_id_list.append(seed_node)

#------------------------------------------------------------------

#------------------------------------------------------------------

# PageRank 計算
pr = nx.pagerank(G=G, alpha=0.15)

pr_sort = sorted(pr.items(), key=lambda x:x[1], reverse=True)

pr_id_sort = []
pr_val_sort = []

for item in pr_sort:
    if item[0] in focus_id_list:
        pr_id_sort.append(item[0])
        pr_val_sort.append(item[1])
    

#------------------------------------------------------------------



#------------------------------------------------------------------
# Self PPR 読み込み　

alpha_list = [5, 15, 30, 50]

# self_ppr_per_dic {alpha : {ID : SelfPPR値}　}

self_ppr_per_a_dic = {}

# {alpha : [selfppr値]}
self_ppr_per_a_id_dic = {alpha : [] for alpha in alpha_list}

for alpha in alpha_list:
    
    path = '../alpha_dir/' + dataset_name + '/self_ppr_' + str(alpha) + '.pkl'
    
    with open(path, 'rb') as f:
        self_ppr = pickle.load(f)
        
    self_ppr_val = {}
    
    for src_node in self_ppr:
        self_ppr_val[src_node] = self_ppr[src_node][src_node]
        
    # 正規化
    self_ppr_sum = 0 
    
    for src_node in self_ppr_val:
        self_ppr_sum += self_ppr_val[src_node]
        
    
    for src_node in self_ppr_val:
        self_ppr_val[src_node] /=  self_ppr_sum
        
    self_ppr_per_a_dic[alpha] = self_ppr_val
    
    for id in pr_id_sort:
       
        self_ppr_per_a_id_dic[alpha].append(self_ppr_val[id])
        
    
     
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
ax.set_xlabel("PR 値", fontsize=14)
ax.set_ylabel("(alpha=0.05)/(alpha=0.15)", fontsize=14)


self_ppr_list = []
one_list = []


focus_alpha_1 = 5

focus_alpha_2 = 15

for i in range(len(self_ppr_per_a_id_dic[15])):
    
    r = self_ppr_per_a_id_dic[focus_alpha_1][i] / self_ppr_per_a_id_dic[focus_alpha_2][i]
    self_ppr_list.append(r)
    one_list.append(1)
    


ax.scatter(pr_val_sort,  self_ppr_list)
ax.plot(pr_val_sort,  one_list, linestyle="dashed", color="r")

s1 = pd.Series(pr_val_sort)
s2 = pd.Series(self_ppr_list)

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

#plt.legend()
plt.tight_layout()
plt.show()


#------------------------------------------------------------------


# #------------------------------------------------------------------

# # plot 順位変動度合い

# # フォントを設定する。
# rcp['font.family'] = 'sans-serif'
# rcp['font.sans-serif'] = ['Hiragino Maru Gothic Pro', 'Yu Gothic', 'Meirio', 'Takao', 'IPAexGothic', 'IPAPGothic', 'VL PGothic', 'Noto Sans CJK JP']

# # カラーマップを用意する。
# cmap = plt.get_cmap("tab10")

# # Figureを作成する。
# fig = plt.figure()
# # Axesを作成する。
# ax = fig.add_subplot(111)

# # Figureの解像度と色を設定する。
# fig.set_dpi(150)
# fig.set_facecolor("white")

# # Axesのタイトルと色を設定する。
# #ax.set_title("物品の所有率")
# ax.set_facecolor("white")

# ax.set_xscale('log')
# #ax.set_yscale('log')

# # x軸とy軸のラベルを設定する。
# ax.set_xlabel("PR 値", fontsize=14)
# ax.set_ylabel("還流度 順位変動 (alpha = 0.05) - (alpha = 0.15)", fontsize=14)


# self_ppr_list = []


# # self_ppr_per_a_dic[alpha] {id : self ppr値}

# focus_alpha_1 = 50

# focus_alpha_2 = 15

# focus_alpha_list = [focus_alpha_1, focus_alpha_2]

# # {alpha : [self ppr 値が高い順 ID]}
# focus_alpha_per_a_dic_id_sort = {alpha : [] for alpha in focus_alpha_list}


# for alpha in focus_alpha_list:
    
#     self_ppr_sort = sorted(self_ppr_per_a_dic[alpha].items(), key=lambda x:x[1], reverse=True)
    
#     for item in self_ppr_sort:
#         focus_alpha_per_a_dic_id_sort[alpha].append(item[0])
    

# # {ノード ID : 順位変動度合い}
# rank_change_dic = {}

# for id in node_list:
#     rank_change_dic[id] = (focus_alpha_per_a_dic_id_sort[focus_alpha_1].index(id) - focus_alpha_per_a_dic_id_sort[focus_alpha_2].index(id)) / n
    
# rank_change_list = []
# zero_list = []

# for id in pr_id_sort:
#     rank_change_list.append(rank_change_dic[id])
#     zero_list.append(0)


# ax.scatter(pr_val_sort,  rank_change_list)
# ax.plot(pr_val_sort,  zero_list, linestyle="dashed", color="r")



# #plt.xticks(x)
# #plt.ylim(0,1)
# plt.xlim(0, 0.0005)


# # グリッドを表示する。
# ax.set_axisbelow(True)
# ax.grid(True, "major", "x", linestyle="--")
# ax.grid(True, "major", "y", linestyle="--")

# #plt.legend()
# plt.tight_layout()
# plt.show()





# #------------------------------------------------------------------

