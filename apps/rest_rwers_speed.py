import numpy as np
import matplotlib.pyplot as plt 
import pandas as pd
import matplotlib as mpl
from scipy.stats import linregress
from matplotlib import rcParams as rcp
import random
from graph import*

# /usr/bin/python3 /Users/tyama/tyama_exp/apps/rest_rwers_speed.py

# ---------------- データ読み込み ------------------
dataset_name = input("Enter the dataset name: ")
data_loader = DataLoader(dataset_name)
data_loader.load_graph()
#data_loader.load_community()
G = data_loader.get_graph()

# {所属するコミュニティ：頂点idのリスト}, {頂点id:所属するコミュニティ}
#c_id, id_c = data_loader.get_communities() 

print(G) # グラフのノード数、エッジ数出力
#print(f"community_num : {len(c_id)}") # コミュニティ数出力
print("-----------------------------------")
# ---------------------------------------------------

# ノード単位でみた RWer の残存
v1 = 0
v2 = 4
walkers_num = 100
max_walk_num = 8
hop = 1        

rwers_obj = RandomWalkers(G)
rest_rwers_list, leak_speed_list = rwers_obj.move_walkers_to_get_leak_speed(v1, max_walk_num, walkers_num, hop)
rest_rwers_list2, leak_speed_list2 = rwers_obj.move_walkers_to_get_leak_speed(v2, max_walk_num, walkers_num, hop)
print(len(rest_rwers_list))
# ---------------------------------------------------


# --------------------- プロット 残存RWer ----------------------
# 横軸 Walk Num, 縦軸 残存 RWer
# ノード毎にみた残存 RWer 数

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

x = np.arange(max_walk_num + 1)
print(len(x))


# x軸の目盛の位置を設定する。
ax.xaxis.set_major_locator(mpl.ticker.FixedLocator(x))
#ax.axes.xaxis.set_ticks([]) # x軸ラベル非表示

#ax.set_ylim(0.75, 1.01)

#ax.scatter(x, v1_last_rwers_num_list, label = "group1") 
#ax.plot(x, v1_last_rwers_num_list)

ax.scatter(x, rest_rwers_list, label = "group1") 
ax.plot(x, rest_rwers_list)

ax.scatter(x, rest_rwers_list2, label = "group2") 
ax.plot(x, rest_rwers_list2)

    
#ax.scatter(x, v2_last_rwers_num_list, label="group2") 
#ax.plot(x, v2_last_rwers_num_list)

# 凡例を表示する。
ax.legend(loc="upper right")

plt.show()

# ---------------------------------------------------

# --------------------- プロット 残存RWer ----------------------
# 横軸 Walk Num, 縦軸 速度
# ノード毎にみた残存 RWer 数

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
ax.set_ylabel("Leak Speed in group (normalized)", fontsize=14)

x = np.arange(max_walk_num)
print(len(x))


# x軸の目盛の位置を設定する。
ax.xaxis.set_major_locator(mpl.ticker.FixedLocator(x))
#ax.axes.xaxis.set_ticks([]) # x軸ラベル非表示

#ax.set_ylim(0.75, 1.01)

#ax.scatter(x, v1_last_rwers_num_list, label = "group1") 
#ax.plot(x, v1_last_rwers_num_list)

ax.scatter(x, leak_speed_list, label = "group1") 
ax.plot(x, leak_speed_list)

ax.scatter(x, leak_speed_list2, label = "group2") 
ax.plot(x, leak_speed_list2)

    
#ax.scatter(x, v2_last_rwers_num_list, label="group2") 
#ax.plot(x, v2_last_rwers_num_list)

# 凡例を表示する。
ax.legend(loc="upper right")

plt.show()

# ---------------------------------------------------