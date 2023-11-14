from StandAloneGraph import *
from utils import *
import networkx as nx
import pickle

import matplotlib.pyplot as plt
import matplotlib as mpl
from scipy.stats import linregress
from matplotlib import rcParams as rcp




# /usr/bin/python3 /Users/tyama/tyama_exp/apps2/plot_rwbc_re.py


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
    
# rwbc 読み込み
rwbc = {}
with open("../bc_result/rwbc.txt") as f:
    for line in f:
        (id, val) = line.split()
        rwbc[int(id)] = float(val)
        
rwbc_sort = sorted(rwbc.items(), key=lambda x:x[1], reverse=True)
labels_data2 = []
for item in rwbc_sort:
    labels_data2.append(item[0])
    
rwbc_value = []    
for id in labels_data2:
    rwbc_value.append(rwbc[id])
    
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

# {com_id : [top 3 nodes]}
com_top3_nodes_dic = {com_id : [] for com_id in c_id}

for id in com_top3_nodes_list:
    com_top3_nodes_dic[id_c[id]].append(id)
    
del com_top3_nodes_dic[7][:3]
        
    
# ------------------------- Plot ------------------------

# フォントを設定する。
rcp['font.family'] = 'sans-serif'
rcp['font.sans-serif'] = ['Hiragino Maru Gothic Pro', 'Yu Gothic', 'Meirio', 'Takao', 'IPAexGothic', 'IPAPGothic', 'VL PGothic', 'Noto Sans CJK JP']

# カラーマップを用意する。
cmap = plt.get_cmap("tab10")

# Figureを作成する。
fig = plt.figure(figsize=(14,8))
# Axesを作成する。
ax = fig.add_subplot(111)

# Figureの解像度と色を設定する。
fig.set_dpi(150)
fig.set_facecolor("white")

# Axesのタイトルと色を設定する。
#ax.set_title("物品の所有率")
ax.set_facecolor("white")

# x軸とy軸のラベルを設定する。
ax.set_xlabel("Node ID (PR sort alpha=15%)", fontsize=14)
ax.set_ylabel("RWBC value", fontsize=14)

x = np.arange(len(labels_data))

alpha_5_30_nodes_list = best_alpha_dic[5] + best_alpha_dic[10] + best_alpha_dic[15] + best_alpha_dic[20] + best_alpha_dic[25] + best_alpha_dic[30]

alpha_10_30_nodes_list = best_alpha_dic[10] + best_alpha_dic[15] + best_alpha_dic[20] + best_alpha_dic[25] + best_alpha_dic[30]

other_list = np.array([])
alpha_5_list = np.array([])
com_7_list = np.array([])
com_10_list = np.array([])
com_12_list = np.array([])


alpha_10_30_list = np.array([])

for id in labels_data:
    if(id not in alpha_5_30_nodes_list):
        other_list = np.append(other_list, np.nan)
    else:
        other_list = np.append(other_list, np.nan)

for id in labels_data:
    if(id in best_alpha_dic[5]):
        alpha_5_list = np.append(alpha_5_list, np.nan)
    else:
        alpha_5_list = np.append(alpha_5_list, np.nan)
        
for id in labels_data:
    if(id in alpha_10_30_nodes_list):
        alpha_10_30_list = np.append(alpha_10_30_list, rwbc[id])
    else:
        alpha_10_30_list = np.append(alpha_10_30_list, np.nan)
        
for id in labels_data:
    if (id in com_top3_nodes_dic[7]):
        com_7_list = np.append(com_7_list, rwbc[id])
    else:
        com_7_list = np.append(com_7_list, np.nan)        

for id in labels_data:
    if (id in com_top3_nodes_dic[10]):
        com_10_list = np.append(com_10_list, rwbc[id])
    else:
        com_10_list = np.append(com_10_list, np.nan)    
        
for id in labels_data:
    if (id in com_top3_nodes_dic[12]):
        com_12_list = np.append(com_12_list, rwbc[id])
    else:
        com_12_list = np.append(com_12_list, np.nan)              

#ax.set_ylim(0, 0.05)

ax.set_yscale('log')

ax.scatter(x[:3000], other_list[:3000], label="max alpha 35%~95%", s=10)
ax.scatter(x[:3000], alpha_5_list[:3000], label="max alpha 5%", s=10)
ax.scatter(x[:3000], alpha_10_30_list[:3000], label="max alpha 10% ~ 30%", s=10)
ax.scatter(x[:3000], com_7_list[:3000], label="community : 7 top 3 nodes", s=20)
ax.scatter(x[:3000], com_10_list[:3000], label="community : 10 top 3 nodes", s=20)
ax.scatter(x[:3000], com_12_list[:3000], label="community : 12 top 3 nodes", s=20)


#ax.scatter(x, other_list, label="max alpha not 5%", s=10)

plt.legend()
plt.show()

#plt.savefig("rwbc_1.pdf")


# ---------------------------------------------------------------