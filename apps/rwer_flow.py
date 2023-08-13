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
# ---------------------------------------------------
