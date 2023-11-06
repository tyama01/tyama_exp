from StandAloneGraph import *
from utils import *
import networkx as nx
import pickle
import sys

import matplotlib.pyplot as plt
import matplotlib as mpl
from scipy.stats import linregress
from matplotlib import rcParams as rcp


# /usr/bin/python3 /Users/tyama/tyama_exp/apps2/plot_best_a.py

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
    
    
# 各ノードのベスト α を保持
best_alpha_dic = {id : 0 for id in labels_data}

for id in labels_data:
    alpha_dic = {a1 : 0 for a1 in alpha_list}
    for a2 in alpha_list:
        alpha_dic[a2] = pr_alpha_dic[a2][id]
    best_alpha_dic[id] = max(alpha_dic, key=alpha_dic.get)
    
# 各コミュニティ内で重要なノード top3 を取得
common_com_top3_nodes_list = []
small_com_top3_nodes_list = []

with open('../com_top_nodes/facebook/common_com_top3_nodes.txt', 'r', encoding='utf-8') as fin:
    for line in fin.readlines():
        try:
            num = int(line)
        except ValueError as e:
            print(e, file=sys.stderr)
            continue
        common_com_top3_nodes_list.append(num)
        

with open('../com_top_nodes/facebook/small_com_top3_nodes.txt', 'r', encoding='utf-8') as fin:
    for line in fin.readlines():
        try:
            num = int(line)
        except ValueError as e:
            print(e, file=sys.stderr)
            continue
        small_com_top3_nodes_list.append(num)
        


com_top3_nodes_list = common_com_top3_nodes_list + small_com_top3_nodes_list


    
# ------------------------- Plot ------------------------

# フォントを設定する。
rcp['font.family'] = 'sans-serif'
rcp['font.sans-serif'] = ['Hiragino Maru Gothic Pro', 'Yu Gothic', 'Meirio', 'Takao', 'IPAexGothic', 'IPAPGothic', 'VL PGothic', 'Noto Sans CJK JP']

# カラーマップを用意する。
cmap = plt.get_cmap("tab10")

# Figureを作成する。
fig = plt.figure()
# Axesを作成する。
ax = fig.add_subplot(111)

# Figureの解像度と色を設定する。
fig.set_dpi(150)
fig.set_facecolor("white")

# Axesのタイトルと色を設定する。
#ax.set_title("物品の所有率")
ax.set_facecolor("white")

# x軸とy軸のラベルを設定する。
ax.set_xlabel("Node ID (PR sort)", fontsize=14)
ax.set_ylabel("alpha_value", fontsize=14)

x = np.arange(len(labels_data))

#ax.scatter(x, best_alpha_list, s=10)
#ax.plot(x, best_alpha_list)

general_bnode_list = np.array([])
common_bnode_list = np.array([])
small_bnode_list = np.array([])

for id in labels_data:
    if(id not in com_top3_nodes_list):
        general_bnode_list = np.append(general_bnode_list, best_alpha_dic[id])
    else:
        general_bnode_list = np.append(general_bnode_list, np.nan)
        
for id in labels_data:
    if(id in common_com_top3_nodes_list):
        common_bnode_list = np.append(common_bnode_list, best_alpha_dic[id])
    else:
        common_bnode_list = np.append(common_bnode_list, np.nan)

for id in labels_data:
    if(id in small_com_top3_nodes_list):
        small_bnode_list = np.append(small_bnode_list, best_alpha_dic[id])
    else:
        small_bnode_list = np.append(small_bnode_list, np.nan)

ax.scatter(x, general_bnode_list, label="normal nodes", s=10)
ax.scatter(x, common_bnode_list, label="common community top3 nodes", s=10)
ax.scatter(x, small_bnode_list, label="small community top3 nodes", s=10)


ax.minorticks_on()
ax.set_yticks([y for y in range(5, 100, 5)])
ax.grid(which="major", color="gray", linestyle="solid")
#ax.grid(which="minor", color="lightgray", linestyle="dotted")


plt.legend()
plt.show()
    