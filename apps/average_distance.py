import numpy as np
import matplotlib.pyplot as plt 
import matplotlib as mpl
from scipy.stats import linregress
from matplotlib import rcParams as rcp
import random
from graph import*

# /usr/bin/python3 /Users/tyama/tyama_exp/apps/average_distance.py

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

# ---------------- Average Dis ----------------------

node_list = list(G.nodes())
random_index = random.randrange(len(node_list))
start_v = node_list[random_index]

print(start_v)
print(list(G.neighbors(start_v)))

community_rw_obj = CommunityRandomWalk(G, c_id, id_c)

# simple_random walk
average_distance = community_rw_obj.average_distance_RW(step_num=1000, jump_raito=0.85, v=start_v)
average_distance_sort = sorted(average_distance.items(), key=lambda x:x[1], reverse=True)
print(average_distance_sort)

# ---------------------------------------------------






