from StandAloneGraph import *
from utils import *
import networkx as nx
import pickle

import matplotlib.pyplot as plt
import matplotlib as mpl
from scipy.stats import linregress
from matplotlib import rcParams as rcp


# /usr/bin/python3 /Users/tyama/tyama_exp/apps2/get_nodes_of_best_alpha_5.py

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

with open('../alpha_dir/facebook/alpha_15.pkl', 'rb') as f:
    ppr_dic = pickle.load(f)

    
ppr_sum_dic_a = {node : 0 for node in ppr_dic}

for src_node in ppr_dic:
    for node in nodes_list:
        if node in ppr_dic[src_node]:
            ppr_sum_dic_a[node] += ppr_dic[src_node][node] / n
        else:
            continue
ppr_sum_dic_sort_a = sorted(ppr_sum_dic_a.items(), key=lambda x:x[1], reverse=True)
labels_data = []
for item in ppr_sum_dic_sort_a:
    labels_data.append(item[0])

alpha_list = [alpha for alpha in range(5, 100, 5)]
#print(alpha_list)

# {alpha : {node_id : PR 値}}
pr_alpha_dic = {}
for alpha in alpha_list:
    path = '../alpha_dir/facebook/alpha_' + str(alpha) + '.pkl'
    with open(path, 'rb') as f:
        ppr_dic = pickle.load(f)
        
    ppr_sum_dic = {node : 0 for node in ppr_dic}
    
    for src_node in ppr_dic:
        for node in nodes_list:
            if node in ppr_dic[src_node]:
                ppr_sum_dic[node] += ppr_dic[src_node][node] / n
            else:
                continue
            
    pr_alpha_dic[alpha] = ppr_sum_dic

# {alpha : [node id]}
best_alpha_dic = {a : [] for a in alpha_list}

for id in labels_data:
    alpha_dic = {a1 : 0 for a1 in alpha_list}
    for a2 in alpha_list:
        alpha_dic[a2] = pr_alpha_dic[a2][id]
    best_alpha_dic[max(alpha_dic, key=alpha_dic.get)].append(id)
    
print(len(best_alpha_dic[15]))
    
#--------------------- txt ファイル出力 ---------------------------

with open('facebook_nodes_of_best_alpha_15.txt', 'w') as f:
    for id in best_alpha_dic[15]:
        f.write("%s\n" %id)
        
