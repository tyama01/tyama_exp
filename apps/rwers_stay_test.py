import numpy as np
import matplotlib.pyplot as plt 
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
rwers_obj = RandomWalkers(G)

v = 0
walk_num = 3
walkers_num = 20
hop = 1

group_rwers_num_per_iteration = rwers_obj.move_walkers_from_n_hop(v, walk_num, walkers_num, hop)


# ---------------------------------------------------


# --------------------- プロット -----------------------

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
ax.set_ylabel("RWers num in group", fontsize=14)

x = np.arange(len(group_rwers_num_per_iteration))

# x軸の目盛の位置を設定する。
ax.xaxis.set_major_locator(mpl.ticker.FixedLocator(x))
#ax.axes.xaxis.set_ticks([]) # x軸ラベル非表示

ax.scatter(x, group_rwers_num_per_iteration)
ax.plot(x, group_rwers_num_per_iteration)

plt.show()

# ---------------------------------------------------
