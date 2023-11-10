import matplotlib.pyplot as plt
import matplotlib as mpl
from scipy.stats import linregress
from matplotlib import rcParams as rcp
from utils import *


# /usr/bin/python3 /Users/tyama/tyama_exp/apps2/bc.py
dataset_name = input("Enter the dataset name: ")
data_loader = DataLoader(dataset_name)
data_loader.load_graph()
data_loader.load_community()
G = data_loader.get_graph()

# {所属するコミュニティ：頂点idのリスト}, {頂点id:所属するコミュニティ}
c_id, id_c = data_loader.get_communities() 


print("----------------------------")

#bc = nx.betweenness_centrality(G)
#bc = nx.closeness_centrality(G)
#bc = nx.information_centrality(G)
bc = nx.communicability_betweenness_centrality(G)

# bc 結果出力
f = open('cbc.txt', 'a', encoding='UTF-8')
for tmp_bc in sorted(bc.items(), key=lambda x:x[1], reverse=True):
    f.write(str(tmp_bc[0]))
    f.write(' ')
    f.write(str(tmp_bc[1]))
    f.write('\n')
