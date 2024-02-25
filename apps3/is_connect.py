from utils import *
import sys
import networkx as nx 

# /usr/bin/python3 /Users/tyama/tyama_exp/apps3/is_connect.py

dataset_name = input("Enter the dataset name: ")
data_loader = DataLoader(dataset_name, is_directed=True)
G = data_loader.get_graph()

print(G)
print("----------------------------")

print(nx.is_weakly_connected(G))

