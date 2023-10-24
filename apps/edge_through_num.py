import numpy as np
import matplotlib.pyplot as plt 
import matplotlib as mpl
from scipy.stats import linregress
from matplotlib import rcParams as rcp
import random
from graph import*

# /usr/bin/python3 /Users/tyama/tyama_exp/apps/edge_through_num.py

# ---------------- データ読み込み ------------------
print("-----------------------------------")
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

# ------------------ 境界エッジを取得 -------------------
community_graph_obj = CommunityGraph(G, c_id, id_c)
c_G = community_graph_obj.generate_community_graph()
boundary_edge_list = community_graph_obj.get_boundary_edge_hash()
# ---------------------------------------------------

# -------------- RW で通過したエッジの回数 ----------------
random_walk_obj = RandomWalk()
hash_e_dic = random_walk_obj.get_edge_through_cnt(G)
hash_e_dic_sort = sorted(hash_e_dic.items(), key=lambda x:x[1], reverse=True)

labels_data = []
values_data = []

for item in hash_e_dic_sort:
    labels_data.append(item[0])
    values_data.append(item[1])
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
ax.set_xlabel("Edges", fontsize=14)
ax.set_ylabel("Edge through times", fontsize=14)

x = np.arange(len(labels_data))

# x軸の目盛の位置を設定する。
ax.xaxis.set_major_locator(mpl.ticker.FixedLocator(x))
ax.axes.xaxis.set_ticks([]) # x軸ラベル非表示

colors = []
for hash_id in labels_data:
    if hash_id in boundary_edge_list:
        colors.append((1, 0, 0, 1))
    else:
        colors.append((0, 1, 0, 0.2))
        
ax.scatter(x, values_data, c=colors, s=12)

plt.show()
# ---------------------------------------------------
