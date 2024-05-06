from utils import *
import networkx as nx 
import pickle


# /usr/bin/python3 /Users/tyama/tyama_exp/apps5/calc_outdeg_centrality.py


# ---------------- データ読み込み ------------------
dataset_name = input("Enter the dataset name: ")
data_loader = DataLoader(dataset_name, is_directed=True)
G = data_loader.get_graph()
print(G) # グラフのノード数、エッジ数出力
print("-----------------------------------")

node_list = list(G.nodes)
n = len(node_list)

# -----------------------------------------------

# -----------------------------------------------
out_centlarity = nx.out_degree_centrality(G)

deg_list = []
for node in out_centlarity:
    if(out_centlarity[node] == 0):
        deg_list.append(node)
        
print(len(deg_list))

# -----------------------------------------------
