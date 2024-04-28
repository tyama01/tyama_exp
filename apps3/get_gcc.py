from utils import *
import sys
import networkx as nx 

# /usr/bin/python3 /Users/tyama/tyama_exp/apps3/get_gcc.py

dataset_name = input("Enter the dataset name: ")
data_loader = DataLoader(dataset_name, is_directed=True)
Gd = data_loader.get_graph()

print(Gd)
print("----------------------------")

data_loader = DataLoader(dataset_name, is_directed=False)
Gu = data_loader.get_graph()

Gcc = sorted(nx.connected_components(Gu), key=len, reverse=True)

G0 = Gcc[0]

H = Gd.subgraph(G0)

nx.write_edgelist(H, "email.txt", data=False)


