# コミュニティサイズに応じて PPR を正規化した　PR 演算

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


# /usr/bin/python3 /Users/tyama/tyama_exp/apps4/rank_change_per_com.py

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
l_list = [0, 0.1, 2, 3, 4, 5] 
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

# pr 順位を格納    
pr_rank_dic = {com_id : [] for com_id in c_id}

for rank_num in range(n):
    pr_rank_dic[id_c[id_sort[rank_num]]].append(rank_num) 


# com_pr の pr値を格納
com_pr_value_sort_dic = {l : [] for l in l_list}

for l in l_list:
    for id in id_sort:
        com_pr_value_sort_dic[l].append(com_pr_dic[l][id])
        
# com pr  を降順にソート
com_pr = com_pr_dic[0.1]
com_pr_sort = sorted(com_pr.items(), key=lambda x:x[1], reverse=True)

com_id_sort = []
for item in com_pr_sort:
    com_id_sort.append(item[0])
    
# com_pr 順位を格納
com_pr_rank_dic = {com_id : [] for com_id in c_id}

for rank_num in range(n):
    com_pr_rank_dic[id_c[com_id_sort[rank_num]]].append(rank_num)
        
#------------------------------------------------------------------

#------------------------------------------------------------------
# 箱ひげ図　プロット 通常 PR ver

y = []
for i in range(len(c_id)):
    y.append(len(c_id[i]))

z = np.sort(y)[::-1]
labels_data = np.argsort(y)[::-1]
labels_data = labels_data.tolist()
labels_data.reverse()
x = np.arange(len(labels_data))


y1 = []
for com_id in labels_data:
    y1.append(pr_rank_dic[com_id])

fig, ax = plt.subplots()

ax.boxplot(y1, vert=False)
ax.set_yticklabels(labels_data)
ax.set_xlabel("Rank")
ax.set_ylabel("Community label")
plt.show()

#------------------------------------------------------------------

#------------------------------------------------------------------
# 箱ひげ図　プロット 通常 com_PR ver

y = []
for i in range(len(c_id)):
    y.append(len(c_id[i]))

z = np.sort(y)[::-1]
labels_data = np.argsort(y)[::-1]
labels_data = labels_data.tolist()
labels_data.reverse()
x = np.arange(len(labels_data))


y1 = []
for com_id in labels_data:
    y1.append(com_pr_rank_dic[com_id])

fig, ax = plt.subplots()

ax.boxplot(y1, vert=False)
ax.set_yticklabels(labels_data)
ax.set_xlabel("Rank")
ax.set_ylabel("Community label")
plt.show()

#------------------------------------------------------------------