import numpy as np
import matplotlib.pyplot as plt 
import matplotlib as mpl
from scipy.stats import linregress
from matplotlib import rcParams as rcp
import random
import pickle
from utils import*
import networkx as nx

# /usr/bin/python3 /Users/tyama/tyama_exp/apps/pr_rw2.py

# ---------------- データ読み込み ------------------
dataset_name = input("Enter the dataset name: ")
data_loader = DataLoader(dataset_name)
data_loader.load_graph()
data_loader.load_community()
G = data_loader.get_graph()

# {所属するコミュニティ：頂点idのリスト}, {頂点id:所属するコミュニティ}
c_id, id_c = data_loader.get_communities() 
# ---------------------------------------------------

# networkx で PR を計算
pr = nx.pagerank(G, alpha=0.85)

pr_sort = sorted(pr.items(), key=lambda x:x[1], reverse=True)

labels_data = []
for item in pr_sort:
    labels_data.append(item[0])
    


    
# ---------------------------------------------------

nodes_list = list(G.nodes())
n = len(nodes_list)

with open('../alpha_dir/facebook/alpha_999_10.pkl', 'rb') as f:
    ppr_dic = pickle.load(f)
    
ppr_sum_dic = {node : 0 for node in ppr_dic}

for src_node in ppr_dic:
    for node in nodes_list:
        if node in ppr_dic[src_node]:
            ppr_sum_dic[node] += ppr_dic[src_node][node] / n
        else:
            continue
        
ppr_sum_dic_sort = sorted(ppr_sum_dic.items(), key=lambda x:x[1], reverse=True)
x_data = []
for item in ppr_sum_dic_sort:
    x_data.append(item[0])

# ---------------------------------------------------

# PR 上位ノードの所属コミュニティを知る
top_num = 100    
top_pr_node_list = []

for i in range(top_num):
    top_pr_node_list.append(labels_data[i])

c_id_pr_top_dic = {i: 0 for i in c_id}

for v in top_pr_node_list:
    c_id_pr_top_dic[id_c[v]] += 1
    
# ---------------------------------------------------
# alpha を変更

top_num = 100    
top_pr_node_list2 = []

for i in range(top_num):
    top_pr_node_list2.append(x_data[i])

c_id_pr_top_dic2 = {i: 0 for i in c_id}

for v in top_pr_node_list2:
    c_id_pr_top_dic2[id_c[v]] += 1


# ---------------------------------------------------



# pagerank 上位にあるノードが所属しているコミュニティ

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
ax.set_xlabel("community labels", fontsize=14)
ax.set_ylabel("Num of PR top nodes", fontsize=14)

# x軸の目盛のラベルの位置を変数xで保持する。

ax.set_ylim(0, 25)

    
y = []
for i in range(len(c_id)):
    y.append(len(c_id[i]))

z = np.sort(y)[::-1]
labels_data = np.argsort(y)[::-1]
x = np.arange(len(labels_data))

pr_top_node_belong_c_list = []
for i in labels_data:
    pr_top_node_belong_c_list.append(c_id_pr_top_dic[i])


# x軸の目盛の位置を設定する。
ax.xaxis.set_major_locator(mpl.ticker.FixedLocator(x))
# x軸の目盛のラベルを設定する。
ax.xaxis.set_major_formatter(mpl.ticker.FixedFormatter(labels_data))

x1 = x[:11]
x2 = x[10:]

z1 = pr_top_node_belong_c_list[:11]
z2 = pr_top_node_belong_c_list[10:]
        
#z1 = z[:11]
#z2 = z[10:]

bar1 = ax.bar(x1, z1, label="common community")
bar2 = ax.bar(x2, z2, label="small community")
        
plt.legend()
plt.show()

# ---------------------------------------------------

# ---------------------------------------------------



# pagerank 上位にあるノードが所属しているコミュニティ

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
ax.set_xlabel("community labels", fontsize=14)
ax.set_ylabel("Num of PR top nodes", fontsize=14)

# x軸の目盛のラベルの位置を変数xで保持する。

ax.set_ylim(0, 25)

    
y = []
for i in range(len(c_id)):
    y.append(len(c_id[i]))

z = np.sort(y)[::-1]
labels_data = np.argsort(y)[::-1]
x = np.arange(len(labels_data))

pr_top_node_belong_c_list = []
for i in labels_data:
    pr_top_node_belong_c_list.append(c_id_pr_top_dic2[i])


# x軸の目盛の位置を設定する。
ax.xaxis.set_major_locator(mpl.ticker.FixedLocator(x))
# x軸の目盛のラベルを設定する。
ax.xaxis.set_major_formatter(mpl.ticker.FixedFormatter(labels_data))

x1 = x[:11]
x2 = x[10:]

z1 = pr_top_node_belong_c_list[:11]
z2 = pr_top_node_belong_c_list[10:]
        
#z1 = z[:11]
#z2 = z[10:]

bar1 = ax.bar(x1, z1, label="common community")
bar2 = ax.bar(x2, z2, label="small community")
        
plt.legend()
plt.show()

# ---------------------------------------------------
