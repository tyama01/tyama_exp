# self ループがあるかをチェック

from utils import *
import sys
import networkx as nx 

# /usr/bin/python3 /Users/tyama/tyama_exp/apps5/check_self_loop.py

#------------------------------------------------------------------
# データセット読み込み

dataset_name = input("Enter the dataset name: ")
data_loader = DataLoader(dataset_name, is_directed=False)
G = data_loader.get_graph()

#------------------------------------------------------------------

#------------------------------------------------------------------

# セルフループがあるかをチェック

for edge in G.edges():
    if edge[0] == edge[1]:
        print("There is a self loop!!")
        break

print("End")

#------------------------------------------------------------------

