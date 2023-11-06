from StandAloneGraph import *
from utils import *
import networkx as nx
import pickle

import matplotlib.pyplot as plt
import matplotlib as mpl
from scipy.stats import linregress
from matplotlib import rcParams as rcp


# /usr/bin/python3 /Users/tyama/tyama_exp/apps2/get_com_best_node.py

dataset_name = input("Enter the dataset name: ")
data_loader = DataLoader(dataset_name)
data_loader.load_graph()
data_loader.load_community()
G = data_loader.get_graph()

# {所属するコミュニティ：頂点idのリスト}, {頂点id:所属するコミュニティ}
c_id, id_c = data_loader.get_communities() 


print("----------------------------")

com_label_size = []
for i in range((len(c_id))):
    com_label_size.append(len(c_id[i]))

com_label_size_sort = np.argsort(com_label_size)[::-1]
common_com_list = com_label_size_sort[:11]
small_com_list = com_label_size_sort[10:]

print(common_com_list)
print("----------------------------")
print(small_com_list)
print("----------------------------")

# 各コミュニティ内で重要なノード top3 を取得
common_com_top3_nodes_list = []
small_com_top3_nodes_list = []


for com_id in common_com_list:
    H = G.subgraph(c_id[com_id])
    pr = nx.pagerank(H, alpha=0.85)
    pr_sort = sorted(pr.items(), key=lambda x:x[1], reverse=True)

    x_data = []
    for item in pr_sort:
        x_data.append(item[0])
        
    for top_num in range(3):
        common_com_top3_nodes_list.append(x_data[top_num])
        
for com_id in small_com_list:
    H = G.subgraph(c_id[com_id])
    pr = nx.pagerank(H, alpha=0.85)
    pr_sort = sorted(pr.items(), key=lambda x:x[1], reverse=True)

    x_data = []
    for item in pr_sort:
        x_data.append(item[0])
        
    for top_num in range(3):
        small_com_top3_nodes_list.append(x_data[top_num])
        
#--------------------- txt ファイル出力 ---------------------------

with open('common_com_top3_nodes.txt', 'w') as f:
    for id in common_com_top3_nodes_list:
        f.write("%s\n" %id)
        
with open('small_com_top3_nodes.txt', 'w') as f:
    for id in small_com_top3_nodes_list:
        f.write("%s\n" %id)
        
    