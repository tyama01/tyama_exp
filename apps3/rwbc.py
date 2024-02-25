from utils import *
import networkx as nx
import pickle

import matplotlib.pyplot as plt
import matplotlib as mpl
from scipy.stats import linregress
from matplotlib import rcParams as rcp
from utils import *


# /usr/bin/python3 /Users/tyama/tyama_exp/apps3/rwbc.py

dataset_name = input("Enter the dataset name: ")
data_loader = DataLoader(dataset_name, is_directed=True)
data_loader.load_community()
G = data_loader.get_graph()

# {所属するコミュニティ：頂点idのリスト}, {頂点id:所属するコミュニティ}
c_id, id_c = data_loader.get_communities() 


print("----------------------------")

rwbc = nx.current_flow_betweenness_centrality(G)

# bc 結果出力
f = open('wiki_rwbc.txt', 'a', encoding='UTF-8')
for tmp_rwbc in sorted(rwbc.items(), key=lambda x:x[1], reverse=True):
    f.write(str(tmp_rwbc[0]))
    f.write(' ')
    f.write(str(tmp_rwbc[1]))
    f.write('\n')
