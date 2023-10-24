import numpy as np
import matplotlib.pyplot as plt 
import pandas as pd
import matplotlib as mpl
from scipy.stats import linregress
from matplotlib import rcParams as rcp
import random
from utils import*

# /usr/bin/python3 /Users/tyama/tyama_exp/apps/com_pr.py

# ---------------- データ読み込み ------------------
# 重みなし
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

# 重みあり
dataset_name = input("Enter the Weight dataset name: ")
data_loader = DataLoader_W(dataset_name)
data_loader.load_graph()
Gw1 = data_loader.get_graph()
print("-----------------------------------")

dataset_name = input("Enter the Weight dataset name: ")
data_loader = DataLoader_W(dataset_name)
data_loader.load_graph()
Gw2 = data_loader.get_graph()

# ---------------------------------------------------

rwer_num = 100
walk_length = 100
d = 0.85
com_id = 13

# コミュニティ単位で PageRank を計算
com_walk_obj = ComWalk(G, c_id, id_c)
pr = com_walk_obj.com_pagerank(rwer_num, walk_length, d, com_id)
pr_sort = sorted(pr.items(), key=lambda x:x[1], reverse=True)

x_data = []
for item in pr_sort:
    x_data.append(item[0])

for i in range(5):
    print(x_data[i])
print("---------")


com_walk_obj_w1 = ComWalkWeighted(Gw1, c_id, id_c)
pr_w1 = com_walk_obj_w1.com_pagerank_weighted(rwer_num, walk_length, d, com_id)
pr_w1_sort = sorted(pr_w1.items(), key=lambda x:x[1], reverse=True)

y1_data = []
for item in pr_w1_sort:
    y1_data.append(item[0])
    
for i in range(5):
    print(y1_data[i])
print("---------")

com_walk_obj_w2 = ComWalkWeighted(Gw2, c_id, id_c)
pr_w2 = com_walk_obj_w2.com_pagerank_weighted(rwer_num, walk_length, d, com_id)
pr_w2_sort = sorted(pr_w2.items(), key=lambda x:x[1], reverse=True)

y2_data = []
for item in pr_w2_sort:
    y2_data.append(item[0])
    
for i in range(5):
    print(y2_data[i])
print("---------")

print("End")


# ---------------------------------------------------
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
ax.set_xlabel("Original Rank", fontsize=14)
ax.set_ylabel("PSI Rank", fontsize=14)

i = 0
for x in x_data:
    ax.plot(i, y1_data.index(x), marker='.', color="b")
    i += 1
    
plt.show()
# ---------------------------------------------------

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
ax.set_xlabel("Original Rank", fontsize=14)
ax.set_ylabel("PSI_reverse Rank", fontsize=14)

i = 0
for x in x_data:
    ax.plot(i, y2_data.index(x), marker='.', color="b")
    i += 1
    
plt.show()
# ---------------------------------------------------
