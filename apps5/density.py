# RW の経路から部分グラフを作成し、密度を見てみるコード

from utils import *
import pickle
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib import rcParams as rcp
import numpy as np

# /usr/bin/python3 /Users/tyama/tyama_exp/apps5/density.py

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

# 密度の計算
# {ノードID : 密度}
# 密度： (RW の経路から生成した部分グラフのエッジ数) / (完全グラフのエッジ数 nC2)
density_dic = {}

# {src_node : RW の経路数}
subgraph_node_num = {}

for src_node in self_ppr:
    
    # 経路にいたノード
    target_node_list = []
    for target_node in self_ppr[src_node]:
        # 自身の周辺よりもあまりにも遠いものは消す (self PPR １０倍以上に設定)
        if self_ppr[src_node][target_node] > (1/10)*self_ppr[src_node][src_node]:
            target_node_list.append(target_node)
    
    # 経路から部分グラフを生成
    H = G.subgraph(target_node_list)
    n_H = len(target_node_list)
    
    density = 2*(H.number_of_edges()) / (n_H*(n_H-1))
    
    density_dic[src_node] = density
    subgraph_node_num[src_node] = n_H
        


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
    
#------------------------------------------------------------------

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

