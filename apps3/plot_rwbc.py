from utils import *
import numpy as np
import pickle

import matplotlib.pyplot as plt
import matplotlib as mpl
from scipy.stats import linregress
from matplotlib import rcParams as rcp




# /usr/bin/python3 /Users/tyama/tyama_exp/apps3/plot_rwbc.py


dataset_name = input("Enter the dataset name: ")
data_loader = DataLoader(dataset_name, is_directed=False)
data_loader.load_community()
G = data_loader.get_graph()

# {所属するコミュニティ：頂点idのリスト}, {頂点id:所属するコミュニティ}
c_id, id_c = data_loader.get_communities() 


print("----------------------------")

nodes_list = list(G.nodes())
n = len(nodes_list)

with open('../alpha_dir/facebook_re/alpha_15.pkl', 'rb') as f:
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
    path = '../alpha_dir/facebook_re/alpha_' + str(alpha) + '.pkl'
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
ax.set_xlabel("Node ID (PR sort alpha=0.15)", fontsize=14)
ax.set_ylabel("RWBC value", fontsize=14)

x = np.arange(len(labels_data))

alpha_5_30_nodes_list = best_alpha_dic[5] + best_alpha_dic[10] + best_alpha_dic[15] + best_alpha_dic[20] + best_alpha_dic[25] + best_alpha_dic[30]

other_list = np.array([])
alpha_5_list = np.array([])
alpha_10_list = np.array([])
alpha_15_list = np.array([])
alpha_20_list = np.array([])
alpha_25_list = np.array([])
alpha_30_list = np.array([])




for id in labels_data:
    if(id not in alpha_5_30_nodes_list):
        other_list = np.append(other_list, rwbc[id])
    else:
        other_list = np.append(other_list, np.nan)
        
for id in labels_data:
    if(id in best_alpha_dic[5]):
        alpha_5_list = np.append(alpha_5_list, rwbc[id])
    else:
        alpha_5_list = np.append(alpha_5_list, np.nan)
        
for id in labels_data:
    if(id in best_alpha_dic[10]):
        alpha_10_list = np.append(alpha_10_list, rwbc[id])
    else:
        alpha_10_list = np.append(alpha_10_list, np.nan)

for id in labels_data:
    if(id in best_alpha_dic[15]):
        alpha_15_list = np.append(alpha_15_list, rwbc[id])
    else:
        alpha_15_list = np.append(alpha_15_list, np.nan)

for id in labels_data:
    if(id in best_alpha_dic[20]):
        alpha_20_list = np.append(alpha_20_list, rwbc[id])
    else:
        alpha_20_list = np.append(alpha_20_list, np.nan)
        
for id in labels_data:
    if(id in best_alpha_dic[25]):
        alpha_25_list = np.append(alpha_25_list, rwbc[id])
    else:
        alpha_25_list = np.append(alpha_25_list, np.nan)
        
for id in labels_data:
    if(id in best_alpha_dic[30]):
        alpha_30_list = np.append(alpha_30_list, rwbc[id])
    else:
        alpha_30_list = np.append(alpha_30_list, np.nan)
        
#ax.set_ylim(0, 0.05)

ax.set_yscale('log')

ax.scatter(x[:3000], other_list[:3000], label="PR max alpha 0.35~0.95", s=10)
ax.scatter(x[:3000], alpha_5_list[:3000], label="PR max alpha 0.05", s=10)
ax.scatter(x[:3000], alpha_10_list[:3000], label="PR max alpha 0.10", s=10)
ax.scatter(x[:3000], alpha_15_list[:3000], label="PR max alpha 0.15", s=10)
ax.scatter(x[:3000], alpha_20_list[:3000], label="PR max alpha 0.20", s=10)
ax.scatter(x[:3000], alpha_25_list[:3000], label="PR max alpha 0.25", s=10)
ax.scatter(x[:3000], alpha_30_list[:3000], label="PR max alpha 0.30", s=10)


#ax.scatter(x, other_list, label="max alpha not 5%", s=10)

plt.legend()
plt.tight_layout()
plt.show()

#plt.savefig("../fig/rwbc_re.pdf")


# ---------------------------------------------------------------