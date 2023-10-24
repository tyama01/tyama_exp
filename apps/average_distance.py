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

# コミュニティを１つとってくる
# 取ってくるのはコミュニティ id 9 一番大きいコミュニティ
com_num = 9
Gs_9 = G.subgraph(c_id[com_num])
print(Gs_9) # diameter : 9
#print(nx.diameter(Gs_9))

pr = nx.pagerank(Gs_9, alpha=0.85)
pr_sort = sorted(pr.items(), key=lambda x:x[1], reverse=True)

labels_data = []
for item in pr_sort:
    labels_data.append(item[0])


node_list = list(Gs_9.nodes())
random_index = random.randrange(len(node_list))
start_v = node_list[random_index]
print(f"{start_v} belong to community : {id_c[start_v]}")

#print(start_v)
#print(list(G.neighbors(start_v)))

community_rw_obj = CommunityRandomWalk(G, c_id, id_c)

# simple_random walk
average_distance = community_rw_obj.average_distance_RW(step_num=10000, jump_raito=0.85, v=start_v)


pass_time = community_rw_obj.get_pass_time()
#print(len(pass_time))

"""
pass_time_sort = sorted(pass_time.items(), key=lambda x:x[1], reverse=True)

labels_data2 = []
for item in pass_time_sort:
    labels_data2.append(item[0])
"""

rw_pr_result = community_rw_obj.rw_pr()
rw_pr_result_sort = sorted(rw_pr_result.items(), key=lambda x:x[1], reverse=True)

labels_data2 = []
for item in rw_pr_result_sort:
    labels_data2.append(item[0])
    
    
for i in range(1, 11):
    print(f"pr ranking {i} : {labels_data[i]}    rw_pr ranking {i} : {labels_data2[i]}")
    #print(f"pass ranking {i} : {labels_data2[i]}")
    

original_average_distance = community_rw_obj.get_oritinal_average_distance()


average_distance_list = []
pass_time_list = []
pass_nodes = []
original_average_distance_list = []

for key in pass_time:
    pass_time_list.append(pass_time[key])
    average_distance_list.append(average_distance[key])
    pass_nodes.append(key)
    original_average_distance_list.append(original_average_distance[key])
    

    
#average_distance_sort = sorted(average_distance.items(), key=lambda x:x[1], reverse=True)
#print(average_distance_sort)

# ---------------------------------------------------


# --------------------- プロット 1-----------------------

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
ax.set_xlabel("RWer pass time", fontsize=14)
ax.set_ylabel("average distance", fontsize=14)


same_com_y = np.array([])
dif_com_y = np.array([])

for node in pass_nodes:
    if id_c[node] == com_num:
        same_com_y = np.append(same_com_y, average_distance[node])
        dif_com_y = np.append(dif_com_y, np.nan)
    else:
        same_com_y = np.append(same_com_y, np.nan)
        dif_com_y = np.append(dif_com_y, average_distance[node])

ax.scatter(pass_time_list, same_com_y, s=5, label="same community")
ax.scatter(pass_time_list, dif_com_y, s=5, label="othter comunities")

plt.legend()
plt.show()
# ---------------------------------------------------

# --------------------- プロット 2-----------------------

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
ax.set_xlabel("RWer pass time", fontsize=14)
ax.set_ylabel("average distance", fontsize=14)


same_com_y = np.array([])
dif_com_y = np.array([])

for node in pass_nodes:
    if id_c[node] == com_num:
        same_com_y = np.append(same_com_y, original_average_distance[node])
        dif_com_y = np.append(dif_com_y, np.nan)
    else:
        same_com_y = np.append(same_com_y, np.nan)
        dif_com_y = np.append(dif_com_y, original_average_distance[node])

ax.scatter(pass_time_list, same_com_y, s=5, label="same community")
ax.scatter(pass_time_list, dif_com_y, s=5, label="other communities")

plt.legend()
plt.show()
# ---------------------------------------------------





