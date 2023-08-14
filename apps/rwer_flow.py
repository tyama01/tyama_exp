import numpy as np
import matplotlib.pyplot as plt 
import matplotlib as mpl
from scipy.stats import linregress
from matplotlib import rcParams as rcp
import random
from graph import*

# /usr/bin/python3 /Users/tyama/tyama_exp/apps/rwer_flow.py

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

# --------------- コミュニティグラフ生成 ------------------
community_graph_obj = CommunityGraph(G, c_id, id_c)
c_G = community_graph_obj.generate_community_graph()
community_size = community_graph_obj.get_community_size()
print(c_G)
#print(community_size)
print("-----------------------------------")

"""
# プロット
node_size = []
node_color = []

# カラーコード選択
color_util_obj = ColorUtil()
num_colors = 100
label2color = color_util_obj.choose_colors(num_colors)


for i in range(len(community_size)):
    node_size.append(community_size[i])
    node_color.append(label2color[i+ int((i+5)/2)])

pos = nx.circular_layout(c_G)
nx.draw(c_G, pos, node_color=node_color, node_size=node_size, with_labels=True)
plt.show()
"""
# ---------------------------------------------------

# ----------------- RWer 遷移を分析 -------------------


community_rw_obj = CommunityRandomWalk(G, id_c)
# (RWerが最後に到達した頂点, 元の所属コミュニティ, 最後にいたコミュニティ)
rwer_info = community_rw_obj.get_last_node_RW_n(10000)
print(rwer_info[0])

last_community = {}
for k in range(len(rwer_info)):
    if rwer_info[k][2] in last_community:
        last_community[rwer_info[k][2]] += 1
    else:
        last_community[rwer_info[k][2]] = 1
    

print("-----------------------------------")

# ---------------------------------------------------

# ----------------- データプロット ----------------------

# Figureを作成する。
fig = plt.figure()
# Axesを作成する。
ax = fig.add_subplot(111)

# Figureの解像度と色を設定する。
fig.set_dpi(150)
fig.set_facecolor("white")

# Axesのタ色を設定する。
ax.set_facecolor("white")

# x軸とy軸のラベルを設定する。
ax.set_xlabel("community labels", fontsize=14)
ax.set_ylabel("RWer nums", fontsize=14)

y = []
for i in range(len(c_id)):
    y.append(len(c_id[i]))
    
g = []
for i in range(len(c_id)):
    g.append(last_community[i])
    
z = np.sort(y)[::-1]
labels_data = np.argsort(y)[::-1]
#print(labels_data)
x = np.arange(len(labels_data))

# x軸の目盛の位置を設定する。
ax.xaxis.set_major_locator(mpl.ticker.FixedLocator(x))
# x軸の目盛のラベルを設定する。
ax.xaxis.set_major_formatter(mpl.ticker.FixedFormatter(labels_data))

"""
color_map = []

for X in list(labels_data):
    color_map.append(node_color[X])
    
print(node_color)
print(color_map)
    
bar = ax.bar(x, z, color=node_color, hatch = 'x')
    
plt.show()
"""

bar = ax.bar(x, g)
plt.show()