# α を変えた場合、コミュニティ内/間でエッジ還流度の値は減少/増加のチェック

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

# /usr/bin/python3 /Users/tyama/tyama_exp/apps9/main_change_alpha_check_edge.py

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

print("-----------------------------------")

node_list = list(G.nodes)
n = len(node_list)

edge_list = list(G.edges())

#print(edge_list)

#------------------------------------------------------------------

#------------------------------------------------------------------

# ノード還流度読み込み
#{alpha : {node_id : ノード還流度}}
node_selfppr = {'5': {}, '10':{}, '15':{}}

for alpha in node_selfppr:
    path = '../alpha_dir/' + dataset_name + '/selfppr_' + alpha + '_01_n.txt'
    with open(path) as f:
        for line in f:
            (id, val) = line.split()
            node_selfppr[alpha][int(id)] = float(val)
            
print("END Reading txt file.")
#print(len(node_selfppr['5']))

# print(node_selfppr['5'][33])
# print(node_selfppr['10'][33])


print("-----------------------------------")

#------------------------------------------------------------------

#------------------------------------------------------------------
# エッジ還流度の計算

eppr_obj = EPPR(G)

edge_selfppr = dict()

for alpha in node_selfppr:
    edge_selfppr[alpha] = eppr_obj.calc_edge_selfppr(node_selfppr=node_selfppr[alpha])
    

print("End Calc Edge_selfPPR")
print("-----------------------------------")
# print(edge_selfppr['5'][(0, 4)])
# print(edge_selfppr['10'][(0, 4)])


#------------------------------------------------------------------

#------------------------------------------------------------------
# 隣接行列取得

# 隣接行列を取得
A = data_loader.get_adj_matrix(is_directed=False)
B = data_loader.get_adj_matrix(is_directed=False)
C = data_loader.get_adj_matrix(is_directed=False)

print("Complete convert G to A")
print("-----------------------------------")


S_dic = {'5':A, '10':B, '15':C}

for alpha in node_selfppr:
    for tmp in sorted(edge_selfppr[alpha].items(), key=lambda x:x[1], reverse=False):
        S_dic[alpha][tmp[0][0]][tmp[0][1]] = tmp[1]
        S_dic[alpha][tmp[0][1]][tmp[0][0]] = tmp[1]
        
        # if(tmp[0] == (0,4)):
        #     print(tmp[1])
        #     print(f"{alpha} : {S_dic[alpha][0][4]}")

# print(S_dic['5'][0][4])

# print(S_dic['10'][0][4])

print("Complete convert G to S")
print("-----------------------------------")

# 増減率を見るために割り算する際の 0 要素を 1 に変換しとく
# 基準の alppha = 0.1     
Base_M = data_loader.get_adj_matrix(is_directed=False)

for i in range(n):
    for j in range(n):
        if(S_dic['10'][i][j] != 0):
            Base_M[i][j] = S_dic['10'][i][j]
        else:
            Base_M[i][j] = 1

print("Complete convert G to B")
print("-----------------------------------")
print(Base_M[0][4])


#------------------------------------------------------------------

#------------------------------------------------------------------
# α が異なる還流度行列演算

# 比較対象の α
comp_alpha = '5'

rate_matrix = data_loader.get_adj_matrix(is_directed=False)

for i in range(n):
    for j in range(n):
        rate_matrix[i][j] = ((S_dic[comp_alpha][i][j] - S_dic['10'][i][j])/(Base_M[i][j]))*100
        
        # if(S_dic[comp_alpha][i][j] != S_dic['10'][i][j]):
        #     print("Hiiiiiiiiiii")
            
print(rate_matrix)

#------------------------------------------------------------------

#------------------------------------------------------------------
# ヒートマッププロット

plt.figure()
sns.heatmap(rate_matrix, square=True, cmap='coolwarm', center=0)
plt.show()

#------------------------------------------------------------------




