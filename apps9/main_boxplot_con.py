# 各手法のコンダクタンスを箱ひげ図でプロット

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

# /usr/bin/python3 /Users/tyama/tyama_exp/apps9/main_boxplot_con.py

# -------------------------- データ読み込み -------------------------
dataset_name = "facebook"
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
# self PPR 値を取得 {ノードID : Self PPR 値}
node_selfppr = {}
path = '../alpha_dir/' + dataset_name + '/selfppr_10_01_n.txt' # n の場合は正規化されている
with open(path) as f:
    for line in f:
        (id, val) = line.split()
        node_selfppr[int(id)] = float(val)

#------------------------------------------------------------------

#------------------------------------------------------------------
# PR 演算
pr = nx.pagerank(G=G, alpha=0.9)

#------------------------------------------------------------------

#------------------------------------------------------------------

# エッジ還流度計算

eppr_obj = EPPR(G)

edge_pr = eppr_obj.calc_edge_selfppr(node_selfppr=pr)

edge_selfppr = eppr_obj.calc_edge_selfppr(node_selfppr=node_selfppr)


print("End Calc Edge_selfPPR")

#------------------------------------------------------------------

#------------------------------------------------------------------
# 隣接行列取得

# 隣接行列を取得
A = data_loader.get_adj_matrix(is_directed=False)
print("Complete convert G to A")

# PR 行列
P = data_loader.get_adj_matrix(is_directed=False)
for tmp in sorted(edge_pr.items(), key=lambda x:x[1], reverse=False):
    P[tmp[0][0]][tmp[0][1]] = tmp[1]
    P[tmp[0][1]][tmp[0][0]] = tmp[1]

# 還流度行列
S = data_loader.get_adj_matrix(is_directed=False)
for tmp in sorted(edge_selfppr.items(), key=lambda x:x[1], reverse=False):
    S[tmp[0][0]][tmp[0][1]] = tmp[1]
    S[tmp[0][1]][tmp[0][0]] = tmp[1]

#------------------------------------------------------------------

#------------------------------------------------------------------
# NMF を適用 & コンダクタンスを計算

# 辞書型で格納
array_dict = {'A':A, 'P':P, 'S':S}
con_dict = {'A':[], 'P':[], 'S':[]}

# 分割数
k = 16

# louvain con値
louvain_con_list = []
part = []

for com_id in c_id:
    part.append(c_id[com_id])

for i in range(len(part)):
    louvain_con_list.append(nx.conductance(G, part[i]))
    

for array in array_dict:
    
    snmf_obj = SNMF(array_dict[array])
    R = snmf_obj.get_best_Rvec(k=k)
    R_normalized = normalize(R, norm='l1', axis=1)
    
    # コミュニティの抽出
    communities = np.argmax(R, axis=1)
    
    # コミュニティごとにノードをグループ化
    node_communities = {}
    for node, community in enumerate(communities):
        if community not in node_communities:
            node_communities[community] = []
        node_communities[community].append(node)
        
    part = []

    for com_id in node_communities:
        part.append(node_communities[com_id])
    
    for i in range(len(part)):
        con_dict[array].append(nx.conductance(G, part[i]))
        
    print(f"End {array}")


#------------------------------------------------------------------

#------------------------------------------------------------------
# 箱ひげ図プロット

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
ax.set_xlabel("コミュニティ抽出手法", fontsize=20)
ax.set_ylabel("Conductance", fontsize=20)

data = (louvain_con_list, con_dict['A'], con_dict['P'], con_dict['S'])

ax.boxplot(data)


# ラベル表示
ax.set_xticklabels(['Louvain', '隣接行列', 'PR行列', '還流度行列'], fontsize=20)

# グリッドを表示する。
ax.set_axisbelow(True)
ax.grid(True, "major", "x", linestyle="--")
ax.grid(True, "major", "y", linestyle="--")


plt.tight_layout()
plt.show()

#------------------------------------------------------------------
