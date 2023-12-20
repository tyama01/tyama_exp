import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from scipy.stats import linregress
from utils import *
import pickle
from matplotlib import cm


# /usr/bin/python3 /Users/tyama/tyama_exp/apps3/com_deg.py

# コミュニティと次数分布の関係

dataset_name = input("Enter the dataset name: ")
data_loader = DataLoader(dataset_name, is_directed=False)
data_loader.load_community()
G = data_loader.get_graph()

nodes_list = list(G.nodes())
n = len(nodes_list)

# {所属するコミュニティ：頂点idのリスト}, {頂点id:所属するコミュニティ}
c_id, id_c = data_loader.get_communities()

y = []
for i in range(len(c_id)):
    y.append(len(c_id[i]))

z = np.sort(y)[::-1]
com_size_sort_data = np.argsort(y)[::-1] # コミュニティサイズが大きいラベル
#print(labels_data) 

print("----------------------------")

# 各コミュニティの次数分布を計算
gamma_list = []

for com_id in com_size_sort_data:
    sub_G = G.subgraph(c_id[com_id])
    degree = dict(sub_G.degree())
    pos_degree_vals = list(filter(lambda val:val>0, degree.values()))
    uq_pos_degree_vals = sorted(set(pos_degree_vals))
    in_hist = [pos_degree_vals.count(x) for x in uq_pos_degree_vals]

    x = np.asarray(uq_pos_degree_vals, dtype = float)
    y = np.asarray(in_hist, dtype = float)

    logx = np.log10(x)
    logy = np.log10(y)

    a, b = np.polyfit(logx, logy, 1)
    gamma_list.append(a)

"""    
sub_G = G.subgraph(c_id[15])
degree = dict(sub_G.degree())
pos_degree_vals = list(filter(lambda val:val>0, degree.values()))
uq_pos_degree_vals = sorted(set(pos_degree_vals))
in_hist = [pos_degree_vals.count(x) for x in uq_pos_degree_vals]

x = np.asarray(uq_pos_degree_vals, dtype = float)
y = np.asarray(in_hist, dtype = float)

logx = np.log10(x)
logy = np.log10(y)

a, b = np.polyfit(logx, logy, 1)
"""

# 各コミュニティ内ノードのベスト alpha の分布を計算
per_com_dest_a_dic = {com_id : [] for com_id in com_size_sort_data} # {コミュニティラベル : [ノードのベスト alpha の分布]}

alpha_list = [alpha for alpha in range(5, 100, 5)]

# {alpha : {node_id : PR 値}}
pr_alpha_dic = {com_id : [] for com_id in com_size_sort_data}

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


for com_id in com_size_sort_data:
    
    # 各ノードのベスト α を保持
    best_alpha_dic = {id : 0 for id in c_id[com_id]}
        
    for id in c_id[com_id]:
        alpha_dic = {a1 : 0 for a1 in alpha_list}
        for a2 in alpha_list:
            alpha_dic[a2] = pr_alpha_dic[a2][id]
        best_alpha_dic[id] = max(alpha_dic, key=alpha_dic.get)
    
    for id in best_alpha_dic:
         per_com_dest_a_dic[com_id].append(best_alpha_dic[id]/100)

boxplot_list = []

for com_id in com_size_sort_data:
    boxplot_list.append(per_com_dest_a_dic[com_id])
    
#print(per_com_dest_a_dic[6])

"""
plt.figure(figsize=(10,10))
#plt.xlim(min(logx), max(logx))
plt.xlabel('log10 (Degree)')
plt.ylabel('log10 (Number of nodes)')
#plt.title('Degree Distribution')
scatter_plot = plt.plot(logx, logy, 'o')
scatter_plot_regression = plt.plot(logx, a*logx + b)

plt.tight_layout()
#plt.show()
plt.savefig("../fig/deg_com15.pdf")


#print("a: " + str(a))
#print("b: " + str(b))
"""

# 箱ひげ図
fig, ax1 = plt.subplots()
ax2 = ax1.twinx()

color_2 = cm.Set1.colors[1]

ax1.boxplot(boxplot_list, labels=com_size_sort_data)
ax1.set_yticks(np.arange(0, 1, 0.1))


x = [i for i in range(1, len(com_size_sort_data) + 1)]
ax2.scatter(x, gamma_list, c=color_2)
ax2.plot(x, gamma_list, c=color_2)
ax2.tick_params(axis='y', colors=color_2)

y2_list = []
for _ in com_size_sort_data:
    y2_list.append(0)
    
ax2.plot(x, y2_list, c=color_2, linestyle = "dashed")

# x軸とy軸のラベルを設定する。
ax1.set_xlabel("Community labels", fontsize=14)
ax1.set_ylabel("PR max alpha", fontsize=14)
ax2.set_ylabel("gamma", fontsize=14, c=color_2)

ax2.spines['right'].set_color(color_2)
ax2.tick_params(axis='y', colors=color_2)

#plt.grid() # 横線ラインを入れることができます。

plt.tight_layout()

# 描画
#plt.show()
plt.savefig("../fig/com_gamma.pdf")


"""
i = 0
for com_id in com_size_sort_data:
    print(f"Com ID: {com_id} | gamma: {gamma_list[i]}")
    i+=1
"""