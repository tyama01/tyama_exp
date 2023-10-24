import numpy as np
import matplotlib.pyplot as plt 
import matplotlib as mpl
from scipy.stats import linregress
from matplotlib import rcParams as rcp
import random
from graph import*

# /usr/bin/python3 /Users/tyama/tyama_exp/apps/rw_com_detec.py
# RW ベースでのコミュニティ検出　始点の依存性が強い,,,

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


#print(start_v)
#print(list(G.neighbors(start_v)))

community_rw_obj = CommunityRandomWalk(G, c_id, id_c)

G_node_list = list(G.nodes())
random_index = random.randrange(len(G_node_list))
start_v = G_node_list[random_index]
print(f"{start_v} belong to community : {id_c[start_v]}")

# simple_random walk
average_distance = community_rw_obj.average_distance_RW(step_num=10000, jump_raito=0.99, v=start_v)
original_average_distance = community_rw_obj.get_oritinal_average_distance()

node_list = []

for id in original_average_distance:
    if original_average_distance[id] < 5:
        node_list.append(id)

pass_time = community_rw_obj.get_pass_time()
#print(len(pass_time))

rw_pr_result = community_rw_obj.rw_pr()
rw_pr_result_sort = sorted(rw_pr_result.items(), key=lambda x:x[1], reverse=True)

labels_data2 = []
for item in rw_pr_result_sort:
    labels_data2.append(item[0])
    
# コミュニティを１つとってくる
# 取ってくるのはコミュニティ id 9 一番大きいコミュニティ
Gs = G.subgraph(node_list)
print(Gs) # diameter : 9

pr = nx.pagerank(Gs, alpha=0.85)
pr_sort = sorted(pr.items(), key=lambda x:x[1], reverse=True)

labels_data = []
for item in pr_sort:
    labels_data.append(item[0])

    
for i in range(1, 11):
    print(f"pr ranking {i} : {labels_data[i]}    rw_pr ranking {i} : {labels_data2[i]}")
    #print(f"pass ranking {i} : {labels_data2[i]}")
    

original_average_distance = community_rw_obj.get_oritinal_average_distance()


# ---------------------------------------------------