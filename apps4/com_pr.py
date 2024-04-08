# コミュニティサイズに応じて PPR を正規化した　PR 演算

from utils import *
import networkx as nx
import sys
import pickle
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import math
from scipy.stats import kendalltau


# /usr/bin/python3 /Users/tyama/tyama_exp/apps4/com_pr.py


# -------------------------- データ読み込み -------------------------
dataset_name = input("Enter the dataset name: ")
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

#------------------------------------------------------------------
# PR 演算

# alpha の値を設定
alpha = 15
print(f'alpha = {alpha}')
path = '../alpha_dir/facebook/alpha_' + str(alpha) + '.pkl'
with open(path, 'rb') as f:
    ppr_dic = pickle.load(f)

# 普通の PR を計算
pr = {target_node : 0 for target_node in ppr_dic}

for src_node in ppr_dic:
    for target_node in node_list:
        if target_node in ppr_dic[src_node]:
            pr[target_node] += ppr_dic[src_node][target_node] / n
            
        else:
            continue
        

# コミュニティサイズで重みづけした PR を計算

# コミュニティサイズの -l 乗　で重みづけ
l_list = [0, 1, 2, 3, 4, 5] 
com_pr_dic = {}


for l in l_list:
    com_pr = {target_node : 0 for target_node in ppr_dic}
    for src_node in ppr_dic:
        for target_node in node_list:
            if target_node in ppr_dic[src_node]:
                c_size = len(c_id[id_c[src_node]])
                com_pr[target_node] += ppr_dic[src_node][target_node] / (c_size**l)
                
            else:
                continue
    
    # 正規化
    pr_sum = 0
    for id in com_pr:
        pr_sum += com_pr[id]
        
    for id in com_pr:
        com_pr[id] = com_pr[id] / pr_sum
        
    com_pr_dic[l] = com_pr

#------------------------------------------------------------------

#------------------------------------------------------------------

# 通常の PR を降順にソート
pr_sort = sorted(pr.items(), key=lambda x:x[1], reverse=True)

id_sort = []
pr_value_sort = []
for item in pr_sort:
    id_sort.append(item[0])
    pr_value_sort.append(item[1])


# com_pr の pr値を格納
com_pr_value_sort_dic = {l : [] for l in l_list}

for l in l_list:
    for id in id_sort:
        com_pr_value_sort_dic[l].append(com_pr_dic[l][id])
        

    
        
#------------------------------------------------------------------

#------------------------------------------------------------------
# ケンドール順位相関係数を計算

tau_list = []

for l in l_list:
    tau, pvalue = kendalltau(pr_value_sort, com_pr_value_sort_dic[l])
    tau_list.append(tau)
    
print(tau_list)


#------------------------------------------------------------------

        
