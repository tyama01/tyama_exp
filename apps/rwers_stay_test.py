import numpy as np
import matplotlib.pyplot as plt 
import pandas as pd
import matplotlib as mpl
from scipy.stats import linregress
from matplotlib import rcParams as rcp
import random
from graph import*

# /usr/bin/python3 /Users/tyama/tyama_exp/apps/rwers_stay_test.py

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

# --------------------- RW --------------------------

v1 = 0
v2 = 4
walkers_num = 20
walk_num_list = [1, 2, 3, 4, 5, 6, 7, 8]
hop = 1

# iteration ごとの RWer 数を list でもつ
v1_iteration_list = []
v2_iteration_list = []

# Walk Num ごとの　残存 PR 値
v1_remaining_pr_in_group_list = []
v1_remaining_pr_out_group_list = []

v2_remaining_pr_in_group_list = []
v2_remaining_pr_out_group_list = []



for walk_num in walk_num_list:
    rwers_obj = RandomWalkers(G)
    v1_iteration = rwers_obj.move_walkers_from_n_hop_exclude_come_back(v1, walk_num, walkers_num, hop)
    v1_iteration_list.append(v1_iteration)
    
    v1_remaining_pr = rwers_obj.get_remaining_pr()
    v1_remaining_pr_in_group_list.append(v1_remaining_pr)
    
    v1_remaining_pr_out = rwers_obj.get_next_hop_remaining_pr()
    v1_remaining_pr_out_group_list.append(v1_remaining_pr_out)
    
    rwers_obj = RandomWalkers(G)
    v2_iteration = rwers_obj.move_walkers_from_n_hop_exclude_come_back(v2, walk_num, walkers_num, hop)
    v2_iteration_list.append(v2_iteration)
    
    v2_remaining_pr = rwers_obj.get_remaining_pr()
    v2_remaining_pr_in_group_list.append(v2_remaining_pr)
    
    v2_remaining_pr_out = rwers_obj.get_next_hop_remaining_pr()
    v2_remaining_pr_out_group_list.append(v2_remaining_pr_out)
    

print(v1_remaining_pr_in_group_list[2])
print(v1_remaining_pr_out_group_list[2])

# walk_num に応じて最終的に滞在した RWer 数
v1_last_rwers_num_list = []
v2_last_rwers_num_list = []

for i in range(len(walk_num_list)):
    v1_last_rwers_num_list.append(v1_iteration_list[i][-1])
    v2_last_rwers_num_list.append(v2_iteration_list[i][-1])

# walk_num に応じた　残存 PR 値 の合計
v1_total_remaining_pr_list = []
v2_total_remaining_pr_list = []

for i in range(len(walk_num_list)):
    x = 0
    for key_v in v1_remaining_pr_in_group_list[i]:
        x += v1_remaining_pr_in_group_list[i][key_v]
    v1_total_remaining_pr_list.append(x)    

for i in range(len(walk_num_list)):
    x = 0
    for key_v in v2_remaining_pr_in_group_list[i]:
        x += v2_remaining_pr_in_group_list[i][key_v]
    v2_total_remaining_pr_list.append(x)        
    

# ---------------------------------------------------


# --------------------- プロット 1 ----------------------
# 横軸 iteration, 縦軸 残存 RWer 数

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
ax.set_xlabel("Iterations", fontsize=14)
ax.set_ylabel("RWers num in group (normalized)", fontsize=14)

x = np.arange(len(v1_iteration_list[0]))

# x軸の目盛の位置を設定する。
ax.xaxis.set_major_locator(mpl.ticker.FixedLocator(x))
#ax.axes.xaxis.set_ticks([]) # x軸ラベル非表示

# RWer の歩数
plot_walk_num = 3
ax.scatter(x, v1_iteration_list[plot_walk_num - 1], label = "group1") # walker_num = 3
ax.plot(x, v1_iteration_list[plot_walk_num - 1])


ax.scatter(x, v2_iteration_list[plot_walk_num - 1], label = "group2") # walker_num = 3
ax.plot(x, v2_iteration_list[plot_walk_num - 1])

# 凡例を表示する。
ax.legend(loc="upper right")

plt.show()

# ---------------------------------------------------
# --------------------- プロット 2 ----------------------
# 横軸 Walk Num, 縦軸 残存 RWer

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

x = np.array(walk_num_list)

# x軸の目盛の位置を設定する。
ax.xaxis.set_major_locator(mpl.ticker.FixedLocator(x))
#ax.axes.xaxis.set_ticks([]) # x軸ラベル非表示

ax.scatter(x, v1_last_rwers_num_list, label = "group1") 
ax.plot(x, v1_last_rwers_num_list)


ax.scatter(x, v2_last_rwers_num_list, label="group2") 
ax.plot(x, v2_last_rwers_num_list)

# 凡例を表示する。
ax.legend(loc="upper right")

plt.show()

# ---------------------------------------------------

# --------------------- プロット 3 ----------------------
# 横軸 Walk Num, 縦軸 残存 PR

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
ax.set_ylabel("Pass Time (normalized)", fontsize=14)

x = np.array(walk_num_list)

# x軸の目盛の位置を設定する。
ax.xaxis.set_major_locator(mpl.ticker.FixedLocator(x))
#ax.axes.xaxis.set_ticks([]) # x軸ラベル非表示

ax.scatter(x, v1_total_remaining_pr_list, label = "group1") 
ax.plot(x, v1_total_remaining_pr_list)


ax.scatter(x, v2_total_remaining_pr_list, label = "group2") 
ax.plot(x, v2_total_remaining_pr_list)

# 凡例を表示する。
ax.legend(loc="upper right")

plt.show()

# ---------------------------------------------------
