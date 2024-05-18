# APPR で検出したコミュニテイから部分グラフを作成し、密度を見てみるコード

from utils import *
import pickle
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib import rcParams as rcp
import numpy as np

# /usr/bin/python3 /Users/tyama/tyama_exp/apps5/appr_density.py

# -------------------------- データ読み込み -------------------------
dataset_name = input("Enter the dataset name: ")
data_loader = DataLoader(dataset_name, is_directed=False)
G = data_loader.get_graph()
print(G) # グラフのノード数、エッジ数出力

print("-----------------------------------")

node_list = list(G.nodes)
n = len(node_list)
#------------------------------------------------------------------

#------------------------------------------------------------------
# selfPPR の結果読み込み
alpha = 15

# self_ppr {src_node : {node_id : ppr 値}}

path = '../alpha_dir/' + dataset_name + '/self_ppr_' + str(alpha) + '.pkl'
with open(path, 'rb') as f:
    self_ppr = pickle.load(f)
    
#------------------------------------------------------------------

#------------------------------------------------------------------
# APPR で検出されたコミュニティの読み込み

# {シードノード ID : [同じコミュニティと判定されたノードID のリスト]}
appr_dic = {}

path = '../appr_dir/' + dataset_name + '_appr.pkl'
with open(path, 'rb') as f:
    appr_dic = pickle.load(f)
    
#------------------------------------------------------------------

#------------------------------------------------------------------
# 密度の計算
# {ノードID : 密度}
# 密度： (APPR から検出したコミュニティの部分グラフのエッジ数) / (完全グラフのエッジ数 nC2)
density_dic = {}

# {src_node : コミュニティサイズ}
subgraph_node_num = {}

# 部分グラフを格納
subgraph_dic = {}

for src_node in self_ppr:
    
    H = G.subgraph(appr_dic[src_node])
    n_H = len(list(H.nodes))
    
    if n_H == 1:
        density = 0

    else:
        density = 2*(H.number_of_edges()) / (n_H*(n_H-1))
        
        
    density_dic[src_node] = density
    subgraph_node_num[src_node] = n_H
    subgraph_dic[src_node] = H
    
    
    
#------------------------------------------------------------------

#------------------------------------------------------------------
# Plot するためのその他諸々の処理

# self PPR 値を取得 {ノードID : Self PPR 値}
self_ppr_val = {}

for src_node in self_ppr:
    self_ppr_val[src_node] = self_ppr[src_node][src_node]
    
    
    
# Self PPR を降順にソート
self_ppr_sort = sorted(self_ppr_val.items(), key=lambda x:x[1], reverse=True)
        
self_ppr_id_sort = []
self_ppr_value_sort = []

for item in self_ppr_sort:
    self_ppr_id_sort.append(item[0])
    self_ppr_value_sort.append(item[1])

# Self PPR 値が大きい順に格納    
density_list = []
subgraph_node_num_list = []

for id in self_ppr_id_sort:
    density_list.append(density_dic[id])
    subgraph_node_num_list.append(subgraph_node_num[id])


    
print("End")

# 上位 5% のサブグラフの PR 順位を計算
top_x = int(n * 0.1)
rank_m = 0
top_pr = {}


for src in self_ppr_id_sort[:top_x]:
    sub_pr = nx.pagerank(subgraph_dic[src])
    top_pr[src] = sub_pr
    
        


top_pr_sort = {}
ture_num = 0
total_num = 0

for src in top_pr:
    top_pr_sort[src] = sorted(top_pr[src].items(), key=lambda x : x[1], reverse=True)

id_sort_dic = {src : [] for src in top_pr_sort}


for src in top_pr_sort:
    for item in top_pr_sort[src]:
        id_sort_dic[src].append(item[0])
    
for src in id_sort_dic:
    if src == id_sort_dic[src][0]:
        ture_num += 1
        total_num += 1
    else:
        total_num += 1

# print(ture_num)
# print(total_num)    
print(ture_num/total_num)

#------------------------------------------------------------------

#------------------------------------------------------------------

# 正規化
self_ppr_sum = 0

for i in range(len(self_ppr_value_sort)):
    self_ppr_sum += self_ppr_value_sort[i]
    
for i in range(len(self_ppr_value_sort)):
    self_ppr_value_sort[i] /= n


for i in range(len(subgraph_node_num_list)):
    subgraph_node_num_list[i] /= n
    
#------------------------------------------------------------------

"""
#------------------------------------------------------------------
# 横軸：ノードID (selfPPR値ソート), 縦軸：密度

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
ax.set_xlabel("Self PPR val", fontsize=14)
ax.set_ylabel("density", fontsize=14)



ax.scatter(self_ppr_value_sort, density_list)
#ax.plot(self_ppr_id_sort, density_list)



# グリッドを表示する。
ax.set_axisbelow(True)
ax.grid(True, "major", "x", linestyle="--")
ax.grid(True, "major", "y", linestyle="--")

#plt.legend()
plt.tight_layout()
plt.show()

#------------------------------------------------------------------

#------------------------------------------------------------------
# 横軸：ノードID (selfPPR値ソート), 縦軸：サブグラフのサイズ

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
ax.set_xlabel("Self PPR val", fontsize=14)
ax.set_ylabel("Node num", fontsize=14)



#ax.scatter(self_ppr_value_sort, density_list)
#ax.plot(self_ppr_id_sort, density_list)
ax.scatter(self_ppr_value_sort, subgraph_node_num_list)



# グリッドを表示する。
ax.set_axisbelow(True)
ax.grid(True, "major", "x", linestyle="--")
ax.grid(True, "major", "y", linestyle="--")

#plt.legend()
plt.tight_layout()
plt.show()

#------------------------------------------------------------------

#------------------------------------------------------------------
# 横軸： 密度, 縦軸: PR関係をプロット

# netwrokx で PRを計算
pr = nx.pagerank(G, alpha=0.85)

pr_value_sort = []


for id in self_ppr_id_sort:
    pr_value_sort.append(pr[id])
    
# 横軸：PR , 縦軸：密度

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
ax.set_yscale('log')

# x軸とy軸のラベルを設定する。
ax.set_xlabel("density", fontsize=14)
ax.set_ylabel("PR", fontsize=14)



#ax.scatter(self_ppr_value_sort, density_list)
#ax.plot(self_ppr_id_sort, density_list)
ax.scatter(density_list, pr_value_sort)



# グリッドを表示する。
ax.set_axisbelow(True)
ax.grid(True, "major", "x", linestyle="--")
ax.grid(True, "major", "y", linestyle="--")

#plt.legend()
plt.tight_layout()
plt.show()



#------------------------------------------------------------------

#------------------------------------------------------------------
# クラスタリング係数と密度の関係をプロット

# Clustering 係数　読み込み

clustering_dic = {}
path = '../clustering_dir/' + dataset_name + '_clustering.txt'

with open(path) as f:
    for line in f:
        (id, val) = line.split()
        clustering_dic[int(id)] = float(val)

clustering_sort = []


for id in self_ppr_id_sort:
    clustering_sort.append(clustering_dic[id])
    
# 横軸： 密度, 縦軸: クラスタリング


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
ax.set_yscale('log')

# x軸とy軸のラベルを設定する。
ax.set_xlabel("density", fontsize=14)
ax.set_ylabel("Clustering", fontsize=14)



#ax.scatter(self_ppr_value_sort, density_list)
#ax.plot(self_ppr_id_sort, density_list)
ax.scatter(density_list, clustering_sort)



# グリッドを表示する。
ax.set_axisbelow(True)
ax.grid(True, "major", "x", linestyle="--")
ax.grid(True, "major", "y", linestyle="--")

#plt.legend()
plt.tight_layout()
plt.show()


#------------------------------------------------------------------
"""







