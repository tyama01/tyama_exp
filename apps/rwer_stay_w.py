import numpy as np
import matplotlib.pyplot as plt 
import pandas as pd
import matplotlib as mpl
from scipy.stats import linregress
from matplotlib import rcParams as rcp
import random
from utils import*

# /usr/bin/python3 /Users/tyama/tyama_exp/apps/rwer_stay_w.py

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

# 滞在RWer を計算

rwer_num = 100
walk_length = 5 # 5 hop
com_id = 0

cwalk_obj = ComWalk(G, c_id, id_c)
hop_stay_ratio_list = cwalk_obj.walker_stay_com_ratio(rwer_num, walk_length, com_id)

hop_stay_ratio_list.insert(0, 1)
print(len(hop_stay_ratio_list))
#print("-----------------------------------")


cwalk_obj = ComWalkWeighted(Gw1, c_id, id_c)
hop_stay_ratio_list_w1 = cwalk_obj.walker_stay_com_ratio_w(rwer_num, walk_length, com_id)

hop_stay_ratio_list_w1.insert(0, 1)
#print(hop_stay_ratio_list_w1)
#print("-----------------------------------")

cwalk_obj = ComWalkWeighted(Gw2, c_id, id_c)
hop_stay_ratio_list_w2 = cwalk_obj.walker_stay_com_ratio_w(rwer_num, walk_length, com_id)

hop_stay_ratio_list_w2.insert(0, 1)
#print(hop_stay_ratio_list_w2)
#print("-----------------------------------")
# ---------------------------------------------------
# プロット
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
ax.set_xlabel("Walk Num", fontsize=14)
ax.set_ylabel("RWers num in group (normalized)", fontsize=14)

x = [i for i in range(len(hop_stay_ratio_list))]

# x軸の目盛の位置を設定する。
ax.xaxis.set_major_locator(mpl.ticker.FixedLocator(x))
#ax.axes.xaxis.set_ticks([]) # x軸ラベル非表示

ax.scatter(x, hop_stay_ratio_list, label = "original") 
ax.plot(x, hop_stay_ratio_list)

ax.scatter(x, hop_stay_ratio_list_w1, label = "PSI") 
ax.plot(x, hop_stay_ratio_list_w1)

ax.scatter(x, hop_stay_ratio_list_w2, label = "PSI_reverse") 
ax.plot(x, hop_stay_ratio_list_w2)

# 凡例を表示する。
ax.legend(loc="upper right")

plt.show()

# ---------------------------------------------------