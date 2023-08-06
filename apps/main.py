import numpy as np
import matplotlib.pyplot as plt 
import matplotlib as mpl
from scipy.stats import linregress
from matplotlib import rcParams as rcp
import random
from graph import*

# /usr/bin/python3 /Users/tyama/tyama_exp/apps/main.py

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

# ---------------- Random Walk ----------------------

# RandomWalkクラスのインスタンスを作成
random_walk_obj = RandomWalk()

# ランダムウォークに基づく媒介中心性を計算
betweenness_centrality = random_walk_obj.random_walk_betweenness_centrality(G)

# 結果を表示
c = 0
for node, centrality in betweenness_centrality.items():
    print(f"Node {node}: {centrality}")
    c += 1
    
    if(c > 10):
        break
# ---------------------------------------------------
