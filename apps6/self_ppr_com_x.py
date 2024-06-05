# alpha を変化させた場合の還流度の変化を測定

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


# /usr/bin/python3 /Users/tyama/tyama_exp/apps6/self_ppr_com_x.py

# -------------------------- データ読み込み -------------------------
dataset_name = "facebook"
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

# PageRank 計算
pr = nx.pagerank(G=G, alpha=0.15)

pr_sort = sorted(pr.items(), key=lambda x:x[1], reverse=True)



pr_id_sort_dic = {com_id : [] for com_id in c_id}
pr_val_sort_dic = {com_id : [] for com_id in c_id}

    
for item in pr_sort:
    
    for com_id in c_id:
        
        if(id_c[item[0]] ==  com_id):
            pr_id_sort_dic[com_id].append(item[0])
            pr_val_sort_dic[com_id].append(item[1])
    

#------------------------------------------------------------------



#------------------------------------------------------------------
# Self PPR 読み込み　

alpha_list = [5, 15]

# self_ppr_per_dic {alpha : {ID : SelfPPR値}　}

self_ppr_per_a_dic = {}


# {alpha : [selfppr値]}

self_ppr_per_a_id_dic = {alpha : [] for alpha in alpha_list}

# {alpha : {com_id : []}}

x_dic = {alpha : {com_id : [] for com_id in c_id} for alpha in alpha_list}


for alpha in alpha_list:
    
    path = '../alpha_dir/' + dataset_name + '/self_ppr_' + str(alpha) + '_fora.pkl'
    
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
    
    
    for com_id in c_id:
        for id in pr_id_sort_dic[com_id]:
            x_dic[alpha][com_id].append(self_ppr_val[id])
             
#-----------------------------------------------------------------





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

#ax.set_xscale('log')
#ax.set_yscale('log')

# x軸とy軸のラベルを設定する。
ax.set_xlabel("PR 値", fontsize=14)
ax.set_ylabel(r"($\alpha$=0.30)/($\alpha$=0.15)", fontsize=14)


self_ppr_list_dic = {com_id : [] for com_id in c_id}
one_list_dic =  {com_id : [] for com_id in c_id}



focus_alpha_1 = 30

focus_alpha_2 = 15

y = []
for i in range(len(c_id)):
    y.append(len(c_id[i]))

z = np.sort(y)[::-1]
labels_data = np.argsort(y)[::-1]
labels_data = labels_data.tolist()

x = np.arange(len(labels_data))


for com_id in labels_data:
    
    
    
    for i in range(len(x_dic[focus_alpha_1][com_id])):
        r = x_dic[focus_alpha_1][com_id][i] / x_dic[focus_alpha_2][com_id][i]
        self_ppr_list_dic[com_id].append(r)
        one_list_dic[com_id].append(1)
        
        
    s1 = pd.Series(pr_val_sort_dic[com_id])
    s2 = pd.Series(self_ppr_list_dic[com_id])

    res = s1.corr(s2)

    print(f"{com_id} : {res}")
    
    #ax.scatter(pr_val_sort_dic[com_id], self_ppr_list_dic[com_id], label = str(com_id))
    #ax.plot(pr_val_sort_dic[com_id],  one_list_dic[com_id], linestyle="dashed", color="r")
    
com_id=6
ax.scatter(pr_val_sort_dic[com_id], self_ppr_list_dic[com_id], label = str(com_id))
ax.plot(pr_val_sort_dic[com_id],  one_list_dic[com_id], linestyle="dashed", color="r")
    

    


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

#ax.set_xscale('log')
#ax.set_yscale('log')

# x軸とy軸のラベルを設定する。
ax.set_xlabel("コミュニティサイズ", fontsize=14)
ax.set_ylabel("相関係数", fontsize=14)


self_ppr_list_dic = {com_id : [] for com_id in c_id}
one_list_dic =  {com_id : [] for com_id in c_id}



focus_alpha_1 = 5

focus_alpha_2 = 15

y = []
for i in range(len(c_id)):
    y.append(len(c_id[i]))

z = np.sort(y)[::-1]
labels_data = np.argsort(y)[::-1]
labels_data = labels_data.tolist()

x = np.arange(len(labels_data))



for com_id in labels_data:
    
    
    
    for i in range(len(x_dic[focus_alpha_1][com_id])):
        r = x_dic[focus_alpha_1][com_id][i] / x_dic[focus_alpha_2][com_id][i]
        self_ppr_list_dic[com_id].append(r)
        one_list_dic[com_id].append(1)
        
        
    s1 = pd.Series(pr_val_sort_dic[com_id])
    s2 = pd.Series(self_ppr_list_dic[com_id])

    res = s1.corr(s2)
    
    plt.plot(len(c_id[com_id]), res, marker = ".", label=str(com_id), markersize=20)

    print(f"{com_id} : {res}")
    
    #ax.scatter(pr_val_sort_dic[com_id], self_ppr_list_dic[com_id], label = str(com_id))
    #ax.plot(pr_val_sort_dic[com_id],  one_list_dic[com_id], linestyle="dashed", color="r")
    
# com_id=6
# ax.scatter(pr_val_sort_dic[com_id], self_ppr_list_dic[com_id], label = str(com_id))
# ax.plot(pr_val_sort_dic[com_id],  one_list_dic[com_id], linestyle="dashed", color="r")


    
        


#plt.xlim(0.0002, 0.0005)

#plt.xlim(0, 10**-3)


#plt.xticks(x)
plt.ylim(0,1)


# グリッドを表示する。
ax.set_axisbelow(True)
ax.grid(True, "major", "x", linestyle="--")
ax.grid(True, "major", "y", linestyle="--")

plt.legend(loc='upper left', bbox_to_anchor=(1, 1))
plt.tight_layout()
plt.show()


#------------------------------------------------------------------





