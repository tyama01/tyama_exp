import numpy as np
import matplotlib.pyplot as plt 
import matplotlib as mpl
import pickle
from scipy.stats import linregress
from matplotlib import rcParams as rcp
from utils import*

# /usr/bin/python3 /Users/tyama/tyama_exp/apps3/spreadhubs_alpha.py

# ---------------- データ読み込み ------------------
dataset_name = input("Enter the dataset name: ")
data_loader = DataLoader(dataset_name, is_directed=False)
data_loader.load_community()
G = data_loader.get_graph()

# {所属するコミュニティ：頂点idのリスト}, {頂点id:所属するコミュニティ}
c_id, id_c = data_loader.get_communities() 

print(G) # グラフのノード数、エッジ数出力
print("-----------------------------------")
# ---------------------------------------------------

# ------------------ seed ノード取得 -------------------
get_seed_obj = GetSeed()
S = get_seed_obj.spread_hub(G, 20)


# ---------------------------------------------------

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

for id in S:
    alpha_dic = {a1 : 0 for a1 in alpha_list}
    for a2 in alpha_list:
        alpha_dic[a2] = pr_alpha_dic[a2][id]
    best_alpha_dic[max(alpha_dic, key=alpha_dic.get)].append(id)
    
num_nodes_alpha_list = []

for alpha in alpha_list:
    num_nodes_alpha_list.append(len(best_alpha_dic[alpha]))
    
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
ax.set_xlabel("alpha", fontsize=14)
ax.set_ylabel("Num of nodes", fontsize=14)

x = np.arange(5, 100, 5)

#ax.scatter(x, pr_value_list, s=10)
#ax.plot(x, pr_value_list)


ax.bar(x, num_nodes_alpha_list, tick_label=[x/100 for x in range(5, 100, 5)])

plt.xticks(rotation=90)
plt.tight_layout()

#plt.show()
plt.savefig("../fig/alpha_SHnodes_num_20.pdf")



