from StandAloneGraph import *
from utils import *
import networkx as nx
import pickle

import matplotlib.pyplot as plt
import matplotlib as mpl
from scipy.stats import linregress
from matplotlib import rcParams as rcp


# /usr/bin/python3 /Users/tyama/tyama_exp/apps2/plot_traffic_ppr_val.py

dataset_name = input("Enter the dataset name: ")
data_loader = DataLoader(dataset_name)
data_loader.load_graph()
data_loader.load_community()
G = data_loader.get_graph()

# {所属するコミュニティ：頂点idのリスト}, {頂点id:所属するコミュニティ}
c_id, id_c = data_loader.get_communities() 


print("----------------------------")

nodes_list = list(G.nodes())
n = len(nodes_list)
#print(nodes_list)

with open('../alpha_dir/facebook/alpha_5.pkl', 'rb') as f:
    ppr_dic_5 = pickle.load(f)
    
with open('../alpha_dir/facebook/alpha_15.pkl', 'rb') as f:
    ppr_dic_15 = pickle.load(f)


# alpha 0.05 で PR が max となるノードを取得
pr_nodes_of_best_alpha_5_list = []

with open('../nodes_list_per_a/facebook_nodes_of_best_alpha_5.txt', 'r', encoding='utf-8') as fin:
    for line in fin.readlines():
        try:
            num = int(line)
        except ValueError as e:
            print(e, file=sys.stderr)
            continue
        pr_nodes_of_best_alpha_5_list.append(num)
        

# alpha 0.15 で PR が max となるノードを取得
pr_nodes_of_best_alpha_15_list = []

with open('../nodes_list_per_a/facebook_nodes_of_best_alpha_15.txt', 'r', encoding='utf-8') as fin:
    for line in fin.readlines():
        try:
            num = int(line)
        except ValueError as e:
            print(e, file=sys.stderr)
            continue
        pr_nodes_of_best_alpha_15_list.append(num)

#points = []
ppr_val_list = []

ppr_val_list_5 = []

for tnode in pr_nodes_of_best_alpha_5_list:  
    
    #short_path_hop_list = []
    
    for src_node in nodes_list:
        if src_node == tnode:
            continue
        
        if (tnode in ppr_dic_5[src_node]):
            val = ppr_dic_5[src_node][tnode]
            ppr_val_list_5.append(val)
    
    #points.append(short_path_hop_list)

#print(len(short_path_hop_list))

ppr_val_list_15 = []

for tnode in pr_nodes_of_best_alpha_15_list:  
    
    #short_path_hop_list = []
    
    for src_node in nodes_list:
        if src_node == tnode:
            continue
        
        if (tnode in ppr_dic_15[src_node]):
            val = ppr_dic_15[src_node][tnode]
            ppr_val_list_15.append(val)
            
ppr_val_list.append(ppr_val_list_5)
ppr_val_list.append(ppr_val_list_15)
        
# ------------------ Plot ------------------------

# 箱ひげ図
fig, ax = plt.subplots()
bp = ax.boxplot(ppr_val_list, labels=['0.05', '0.15'], sym="")

# x軸とy軸のラベルを設定する。
ax.set_xlabel("alpha", fontsize=14)
ax.set_ylabel("PPR value", fontsize=14)

#plt.grid() # 横線ラインを入れることができます。
# 描画
plt.show()