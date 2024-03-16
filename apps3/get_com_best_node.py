from utils import *
import networkx as nx 

# /usr/bin/python3 /Users/tyama/tyama_exp/apps3/get_com_best_node.py

# ---------------- データ読み込み ------------------
dataset_name = input("Enter the dataset name: ")
data_loader = DataLoader(dataset_name, is_directed=False)
G = data_loader.get_graph()
print(G) # グラフのノード数、エッジ数出力

# {所属するコミュニティ：頂点idのリスト}, {頂点id:所属するコミュニティ}
data_loader.load_community()
c_id, id_c = data_loader.get_communities() 

print("-----------------------------------")

node_list = list(G.nodes)
n = len(node_list)
print(len(c_id))

# -----------------------------------------------

# 各コミュニティで最も重要なノードを検出 α = 0.15
# コミュニティの代表ノードを格納するリスト
com_best_node_list = []

for com_id in c_id:
    H = G.subgraph(c_id[com_id])
    pr = nx.pagerank(H, alpha=0.85)
    pr_sort = sorted(pr.items(), key=lambda x:x[1], reverse=True)
    
    x_data = []
    for item in pr_sort:
        x_data.append(item[0])
        
    com_best_node_list.append(x_data[0])

print(len(com_best_node_list))    
print(com_best_node_list)
    
    
with open('com_best_nodes_list.txt', 'w') as f:
    for id in com_best_node_list:
        f.write("%s\n" %id)