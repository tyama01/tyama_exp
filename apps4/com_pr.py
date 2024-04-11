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

#------------------------------------------------------------------
# top 100 に各コミュニティのノードがどの程度含まれているか

# 通常の PR
top_num = 100
top_pr_node_list = []

for i in range(top_num):
    top_pr_node_list.append(id_sort[i])

c_id_num_dic = {com_id : 0 for com_id in c_id}

for v in top_pr_node_list:
    c_id_num_dic[id_c[v]] += 1
    
# com pr
com_pr = com_pr_dic[1]
com_pr_sort = sorted(com_pr.items(), key=lambda x:x[1], reverse=True)

com_id_sort = []
for item in com_pr_sort:
    com_id_sort.append(item[0])
    

top_com_pr_node_list = []

for i in range(top_num):
    top_com_pr_node_list.append(com_id_sort[i])

c_id_num_dic2 = {com_id : 0 for com_id in c_id}

for v in top_com_pr_node_list:
    c_id_num_dic2[id_c[v]] += 1


#------------------------------------------------------------------

#------------------------------------------------------------------
# l を変化させた場合の順位相関 タウ をプロット

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

# x軸とy軸のラベルを設定する。
ax.set_xlabel("$\it{l}$", fontsize=14)
ax.set_ylabel("\u03c4", fontsize=14)

ax.scatter(l_list, tau_list)
ax.plot(l_list, tau_list)

plt.show()

#------------------------------------------------------------------


#------------------------------------------------------------------
# top 100 に各コミュニティの代表がどのくらい含まれているかをプロット 通常の PR ver

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

# x軸とy軸のラベルを設定する。
ax.set_xlabel("community labels", fontsize=14)
ax.set_ylabel("Num of PR top " + str(top_num) + " nodes", fontsize=14)

# x軸の目盛のラベルの位置を変数xで保持する。

ax.set_ylim(0, 30)
    
y = []
for i in range(len(c_id)):
    y.append(len(c_id[i]))

z = np.sort(y)[::-1]
labels_data = np.argsort(y)[::-1]
x = np.arange(len(labels_data))

pr_top_node_belong_c_list = []
for i in labels_data:
    pr_top_node_belong_c_list.append(c_id_num_dic[i])


# x軸の目盛の位置を設定する。
ax.xaxis.set_major_locator(mpl.ticker.FixedLocator(x))
# x軸の目盛のラベルを設定する。
ax.xaxis.set_major_formatter(mpl.ticker.FixedFormatter(labels_data))


        
#z1 = z[:11]
#z2 = z[10:]

bar = ax.bar(x, pr_top_node_belong_c_list)
        
plt.show()


#------------------------------------------------------------------

#------------------------------------------------------------------
# top 100 に各コミュニティの代表がどのくらい含まれているかをプロット com PR ver

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

# x軸とy軸のラベルを設定する。
ax.set_xlabel("community labels", fontsize=14)
ax.set_ylabel("Num of PR top " + str(top_num) + " nodes", fontsize=14)


# x軸の目盛のラベルの位置を変数xで保持する。

ax.set_ylim(0, 30)

    
y = []
for i in range(len(c_id)):
    y.append(len(c_id[i]))

z = np.sort(y)[::-1]
labels_data = np.argsort(y)[::-1]
x = np.arange(len(labels_data))

pr_top_node_belong_c_list = []
for i in labels_data:
    pr_top_node_belong_c_list.append(c_id_num_dic2[i])


# x軸の目盛の位置を設定する。
ax.xaxis.set_major_locator(mpl.ticker.FixedLocator(x))
# x軸の目盛のラベルを設定する。
ax.xaxis.set_major_formatter(mpl.ticker.FixedFormatter(labels_data))


        
#z1 = z[:11]
#z2 = z[10:]

bar = ax.bar(x, pr_top_node_belong_c_list)
        
plt.show()


#------------------------------------------------------------------


        

        
