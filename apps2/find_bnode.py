from StandAloneGraph import *
from utils import *
import networkx as nx
import pickle
import sys

import matplotlib.pyplot as plt
import matplotlib as mpl
from scipy.stats import linregress
from matplotlib import rcParams as rcp


# /usr/bin/python3 /Users/tyama/tyama_exp/apps2/find_bnode.py

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
    
pr_value_a = []

for id in labels_data:
    pr_value_a.append(ppr_sum_dic_a[id])

#for i in range(10):
    #print(y_data[i])
print("----------------------------")

with open('../alpha_dir/facebook/alpha_5.pkl', 'rb') as f:
    ppr_dic = pickle.load(f)
    
ppr_sum_dic_b = {node : 0 for node in ppr_dic}

for src_node in ppr_dic:
    for node in nodes_list:
        if node in ppr_dic[src_node]:
            ppr_sum_dic_b[node] += ppr_dic[src_node][node] / n
        else:
            continue
ppr_sum_dic_sort_b = sorted(ppr_sum_dic_b.items(), key=lambda x:x[1], reverse=True)
x_data = []
for item in ppr_sum_dic_sort_b:
    x_data.append(item[0])
    
pr_value_b = []

for id in labels_data:
    pr_value_b.append(ppr_sum_dic_b[id])

#for i in range(10):
    #print(y_data[i])
print("----------------------------")

with open('../alpha_dir/facebook/alpha_50.pkl', 'rb') as f:
    ppr_dic = pickle.load(f)
    
ppr_sum_dic_c = {node : 0 for node in ppr_dic}

for src_node in ppr_dic:
    for node in nodes_list:
        if node in ppr_dic[src_node]:
            ppr_sum_dic_c[node] += ppr_dic[src_node][node] / n
        else:
            continue
        
ppr_sum_dic_sort_c = sorted(ppr_sum_dic_c.items(), key=lambda x:x[1], reverse=True)
x2_data = []
for item in ppr_sum_dic_sort_c:
    x2_data.append(item[0])
    
pr_value_c = []

for id in labels_data:
    pr_value_c.append(ppr_sum_dic_c[id])

#for i in range(10):
    #print(y_data[i])
print("----------------------------")

"""
bnode_list = []
for id in labels_data:
    b_value = ppr_sum_dic_b[id]/ppr_sum_dic_c[id]
    bnode_list.append(b_value)
"""

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


"""
# ------------- Plot ------------------------

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
ax.set_xlabel("node ID (PR sort)", fontsize=14)
ax.set_ylabel("(alpha=50%)/(alpha=5%)", fontsize=14)

x = np.arange(len(labels_data))

com_label_size = []
for i in range((len(c_id))):
    com_label_size.append(len(c_id[i]))

com_label_size_sort = np.argsort(com_label_size)[::-1]
common_com_list = com_label_size_sort[:11]
small_com_list = com_label_size_sort[10:]

common_bnode_list = np.array([])
small_bnode_list = np.array([])

for id in labels_data:
    if(id_c[id] in common_com_list):
        b_value = ppr_sum_dic_c[id]/ppr_sum_dic_b[id]
        common_bnode_list = np.append(common_bnode_list, b_value)
    else:
        common_bnode_list = np.append(common_bnode_list, np.nan)

for id in labels_data:
    if(id_c[id] in small_com_list):
        b_value = ppr_sum_dic_c[id]/ppr_sum_dic_b[id]
        small_bnode_list = np.append(small_bnode_list, b_value)
    else:
        small_bnode_list = np.append(small_bnode_list, np.nan)
        


#ax.set_xscale('log')
#ax.set_yscale('log')

#ax.scatter(x, bnode_list, label="(alpha=5%)/(alpha=50%)", s=10)

ax.scatter(x, common_bnode_list, label="common community", s=10)
ax.scatter(x, small_bnode_list, label="small community", s=10)

p = plt.plot([0, len(x)],[1.0, 1.0], "red", linestyle='dashed') # normal way


plt.legend()
plt.show()
"""
# ------------- Plot ------------------------

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
ax.set_xlabel("node ID (PR sort)", fontsize=14)
ax.set_ylabel("(alpha=50%)/(alpha=5%)", fontsize=14)

x = np.arange(len(labels_data))


general_bnode_list = np.array([])
common_bnode_list = np.array([])
small_bnode_list = np.array([])


for id in labels_data:
    if(id not in com_top3_nodes_list):
        b_value = ppr_sum_dic_c[id]/ppr_sum_dic_b[id]
        general_bnode_list = np.append(general_bnode_list, b_value)
    else:
        general_bnode_list = np.append(general_bnode_list, np.nan)


for id in labels_data:
    if(id in common_com_top3_nodes_list):
        b_value = ppr_sum_dic_c[id]/ppr_sum_dic_b[id]
        common_bnode_list = np.append(common_bnode_list, b_value)
    else:
        common_bnode_list = np.append(common_bnode_list, np.nan)


for id in labels_data:
    if(id in small_com_top3_nodes_list):
        b_value = ppr_sum_dic_c[id]/ppr_sum_dic_b[id]
        small_bnode_list = np.append(small_bnode_list, b_value)
    else:
        small_bnode_list = np.append(small_bnode_list, np.nan)
    

#ax.set_xscale('log')
#ax.set_yscale('log')

#ax.scatter(x, bnode_list, label="(alpha=5%)/(alpha=50%)", s=10)

ax.scatter(x, general_bnode_list, label="normal nodes", s=10)
ax.scatter(x, common_bnode_list, label="common community top3 nodes", s=15, color=cmap(6))
ax.scatter(x, small_bnode_list, label="small community top3 nodes", s=15, color=cmap(1))

p = plt.plot([0, len(x)],[1.0, 1.0], "red", linestyle='dashed') # normal way


plt.legend()
#plt.show()

plt.savefig("find_bnode.pdf")
