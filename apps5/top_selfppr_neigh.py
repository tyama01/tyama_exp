# Self PPR 上位 top 10 の隣接の SelfPPR値を箱ひげ図でプロット

from utils import *
import pickle
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib import rcParams as rcp
import numpy as np
import networkx as nx

# /usr/bin/python3 /Users/tyama/tyama_exp/apps5/top_selfppr_neigh.py

# -------------------------- データ読み込み -------------------------
dataset_name = input("Enter the dataset name: ")
is_directed = False
data_loader = DataLoader(dataset_name, is_directed)
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
    
    
    
# top 10 の self PPR 値を取得
top_id_list = []
top_val_list = []

for top_num in range(10):
    top_id_list.append(self_ppr_id_sort[top_num])
    top_val_list.append(self_ppr_value_sort[top_num])

#print(top_val_list)

# self PPR 上位ノード の隣接
top_neigbors_id_dic = {id : [] for id in top_id_list}

for id in top_id_list:
    if is_directed == False:
        neighbors = list(G.neighbors(id))
        
        for neigh_id in neighbors: 
            if self_ppr_val[neigh_id] > ((1/10) * self_ppr_val[id]):
                top_neigbors_id_dic[id].append(neigh_id)
                
# 隣接の SelfPPR 値
top_neigbors_val_dic = {id : [] for id in top_id_list}

for id in top_id_list:
    for neigh in top_neigbors_id_dic[id]:
        top_neigbors_val_dic[id].append(self_ppr_val[neigh])
        
y = []

for id in top_neigbors_val_dic:
    y.append(top_neigbors_val_dic[id])

neigbors_num_list = []

for id in top_neigbors_id_dic:
    neigbors_num_list.append(len(top_neigbors_id_dic[id]))

    
#------------------------------------------------------------------

#------------------------------------------------------------------
# 箱ひげ図プロット

fig, ax = plt.subplots()


x = [i for i in range(1, 11)]

ax.boxplot(y)
ax.set_xlabel("Rank")
ax.set_ylabel("self ppr")
ax.scatter(x, top_val_list, label="self ppr val (focus node)")
ax.plot(x, top_val_list)

# グリッドを表示する。
ax.set_axisbelow(True)
ax.grid(True, "major", "x", linestyle="--")
ax.grid(True, "major", "y", linestyle="--")

plt.legend()
plt.tight_layout()

plt.show()

#------------------------------------------------------------------

#------------------------------------------------------------------
# 隣接ノード数を棒グラフで表示

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
ax.set_xlabel("Rank", fontsize=14)
ax.set_ylabel("Neighbors Num", fontsize=14)
plt.xticks(x)

ax.bar(x, neigbors_num_list)

# グリッドを表示する。
ax.set_axisbelow(True)
ax.grid(True, "major", "x", linestyle="--")
ax.grid(True, "major", "y", linestyle="--")

#plt.legend()
plt.tight_layout()
plt.show()



#------------------------------------------------------------------

