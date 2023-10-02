import numpy as np
import matplotlib.pyplot as plt 
import matplotlib as mpl
from scipy.stats import linregress
from matplotlib import rcParams as rcp
import random
from graph import*

# /usr/bin/python3 /Users/tyama/tyama_exp/apps/seed_imp.py

# ---------------- データ読み込み ------------------
dataset_name = input("Enter the dataset name: ")
data_loader = DataLoader(dataset_name)
data_loader.load_graph()
data_loader.load_community()
G = data_loader.get_graph()

# {所属するコミュニティ：頂点idのリスト}, {頂点id:所属するコミュニティ}
c_id, id_c = data_loader.get_communities() 

print(G) # グラフのノード数、エッジ数出力
print(f"community_num : {len(c_id)}") # コミュニティ数出力
print("-----------------------------------")
# ---------------------------------------------------

# ------------------ seed ノード取得 -------------------
get_seed_obj = GetSeed()
S = get_seed_obj.spread_hub(G, 2000)

"""
#print(S)
# シードノードの所属コミュニティ
for seed_node in S:
    print(f"node ID {seed_node} : belong to community {id_c[seed_node]}")

print("-----------------------------------")
"""

# ---------------------------------------------------

"""
# ------------------ 中心性指標計算 -------------------


# PageRank 計算
pr = nx.pagerank(G, alpha=0.85)
pr_sort = sorted(pr.items(), key=lambda x:x[1], reverse=True)

pr_labels_data = []
for item in pr_sort:
    pr_labels_data.append(item[0])


# 媒介中心性 計算
bc = nx.betweenness_centrality(G)
bc_sort = sorted(bc.items(), key=lambda x:x[1], reverse=True)

bc_labels_data = []
for item in bc_sort:
    bc_labels_data.append(item[0])


# ---------------------------------------------------
"""

# ------------------ コミュニティ内でのシードノード -------------------

com_graph = CommunityGraph(G, c_id, id_c)
com_graph_dic = com_graph.get_community_graph()

# ---------------------------------------------------
# 新しいコミュニティラベル コミュニティラベルが小さいほどコミュニティサイズが大きい
re_com_id = {}

com_size = []
for i in range(len(c_id)):
    com_size.append(len(c_id[i]))

com_size_sort = np.sort(com_size)[::-1]
com_size_sort_index = np.argsort(com_size)[::-1]
#x = np.arange(len(com_size_sort_index))
print(com_size_sort)
#print(com_size_sort_index)

new_id = 0
for old_id in com_size_sort_index:
    re_com_id[old_id] = new_id
    new_id += 1    
#print(re_com_id)
# ---------------------------------------------------

# plot のために値を入れる
com_id_x = [] # シードノードが所属しているコミュニティ (re_new_id)
com_in_ratio = [] # コミュニティ内次数 / グローバル次数

for seed_node in S:
    belong_com = id_c[seed_node]
    com_id_x.append(re_com_id[belong_com])
    
    in_ratio = com_graph_dic[belong_com].degree[seed_node] / G.degree[seed_node]
    com_in_ratio.append(in_ratio)

# ---------------------------------------------------



"""
# --------------------- プロット pr ----------------------
# 横軸 頂点ID, 縦軸 PR 値

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
ax.set_xlabel("Node ID", fontsize=14)
ax.set_ylabel("PageRank Value", fontsize=14)

x = np.arange(len(pr_labels_data))

common_node_pr = np.array([])
seed_node_pr = np.array([])

for id in pr_labels_data:
    if id in S:
        seed_node_pr = np.append(seed_node_pr, pr[id])
        common_node_pr = np.append(common_node_pr, np.nan)
    else:
        seed_node_pr = np.append(seed_node_pr, np.nan)
        common_node_pr = np.append(common_node_pr, pr[id])

print(len(x))
print(len(common_node_pr))


ax.scatter(x, common_node_pr, label="common")
ax.scatter(x, seed_node_pr, label="seed")

ax.xaxis.set_major_locator(mpl.ticker.FixedLocator(x))
ax.axes.xaxis.set_ticks([]) # x軸ラベル非表示

plt.legend()
plt.show()    

# ---------------------------------------------------


# --------------------- プロット bc ----------------------
# 横軸 頂点ID, 縦軸 PR 値

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
ax.set_xlabel("Node ID", fontsize=14)
ax.set_ylabel("Betweenness Centrality Value", fontsize=14)

x = np.arange(len(bc_labels_data))

common_node_bc = np.array([])
seed_node_bc = np.array([])

for id in bc_labels_data:
    if id in S:
        seed_node_bc = np.append(seed_node_bc, bc[id])
        common_node_bc = np.append(common_node_bc, np.nan)
    else:
        seed_node_bc = np.append(seed_node_bc, np.nan)
        common_node_bc = np.append(common_node_bc, bc[id])

print(len(x))
print(len(common_node_bc))


ax.scatter(x, common_node_bc, label="common")
ax.scatter(x, seed_node_bc, label="seed")

ax.xaxis.set_major_locator(mpl.ticker.FixedLocator(x))
ax.axes.xaxis.set_ticks([]) # x軸ラベル非表示

plt.legend()
plt.show()    

# ---------------------------------------------------
"""


# --------------------- プロット 次数 ----------------------
# 横軸 コミュニティID, 縦軸 所属コミュニティエッジ率

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
ax.set_xlabel("Community ID", fontsize=14)
ax.set_ylabel("Edge in Community Ratio", fontsize=14)

ax.scatter(com_id_x, com_in_ratio, color = 'r', alpha=0.3, s=100)

ax.set_xticks([i for i in range(len(re_com_id))])

ax.grid()

plt.show()    

# ---------------------------------------------------