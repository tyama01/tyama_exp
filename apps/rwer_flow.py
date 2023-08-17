import numpy as np
import matplotlib.pyplot as plt 
import matplotlib as mpl
from scipy.stats import linregress
from matplotlib import rcParams as rcp
import random
from graph import*

# /usr/bin/python3 /Users/tyama/tyama_exp/apps/rwer_flow.py

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
nx.draw(c_G, pos, node_size=node_size, with_labels=True)
plt.show()
"""

node_size = []
for i in range(len(community_size)):
    node_size.append(community_size[i])
   
pos = nx.circular_layout(c_G)
nx.draw(c_G, pos, node_size=node_size, with_labels=True)
plt.show()

# ---------------------------------------------------

# ----------------- RWer 遷移を分析 -------------------

last_community_list = []
hop_num_list = [10, 50, 100, 500]

for hop_num in hop_num_list:
    community_rw_obj = CommunityRandomWalk(G, c_id, id_c)
    last_community = community_rw_obj.get_last_node_belong_community(hop_num)
    last_community_list.append(last_community)

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

    
    
z = np.sort(y)[::-1]
labels_data = np.argsort(y)[::-1]
#print(labels_data)
x = np.arange(len(labels_data))



# x軸の目盛の位置を設定する。
ax.xaxis.set_major_locator(mpl.ticker.FixedLocator(x))
# x軸の目盛のラベルを設定する。
ax.xaxis.set_major_formatter(mpl.ticker.FixedFormatter(labels_data))

data = []

data.append(z)
g = []

for i in range(len(hop_num_list)):
    for j in labels_data:
        g.append(last_community_list[i][j])
    data.append(g)
    g = []

# 棒の幅を変数widthで保持する。
width = (1 - .2) / len(data)
# 棒グラフのオブジェクトのリストを変数barsで保持する。
bars = []

labels_series = ['hop=0', 'hop=10', 'hop=50', 'hop=100', 'hop=500']

# データを描画する。
for i in range(len(data)):
    bars.append(ax.bar(x + (i - .5 * (len(data) - 1)) * width, data[i], width, label = labels_series[i]))



# グリッドを表示する。
ax.set_axisbelow(True)
ax.grid(True, "major", "y", linestyle="--")

# 凡例を表示する。
ax.legend(loc="upper right")

# グラフを表示する。
plt.show()
# ---------------------------------------------------
