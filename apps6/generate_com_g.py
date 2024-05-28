# Louvain で検出したコミュニティの部分グラフを出力するコード

from utils import *
import networkx as nx
import sys

# /usr/bin/python3 /Users/tyama/tyama_exp/apps6/generate_com_g.py

# -------------------------- データ読み込み -------------------------
dataset_name = input("Enter the dataset name: ")
data_loader = DataLoader(dataset_name, is_directed=False)
G = data_loader.get_graph()
print(G) # グラフのノード数、エッジ数出力

data_loader.load_community()

# {所属するコミュニティ：頂点idのリスト}, {頂点id:所属するコミュニティ}
c_id, id_c = data_loader.get_communities() 

print("-----------------------------------")

node_list = list(G.nodes)
n = len(node_list)
#------------------------------------------------------------------

#------------------------------------------------------------------
# コミュニティの部分グラフを生成

com_id = 1

H = G.subgraph(c_id[com_id])

path = "../datasets/" + dataset_name + "_com_" + str(com_id) + ".txt"

# 出力
nx.write_edgelist(H, path, data=False)

#------------------------------------------------------------------


