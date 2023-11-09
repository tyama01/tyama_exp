from StandAloneGraph import *
from utils import *
import networkx as nx
import pickle

import matplotlib.pyplot as plt
import matplotlib as mpl
from scipy.stats import linregress
from matplotlib import rcParams as rcp


# /usr/bin/python3 /Users/tyama/tyama_exp/apps2/pr_ppr_plot.py

dataset_name = input("Enter the dataset name: ")
data_loader = DataLoader(dataset_name)
data_loader.load_graph()
G = data_loader.get_graph()

pr = nx.pagerank(G, alpha=0.85)
#print(pr)
pr_sort = sorted(pr.items(), key=lambda x:x[1], reverse=True)

labels_data = []
for item in pr_sort:
    labels_data.append(item[0])

pr_value = []    
for id in labels_data:
    pr_value.append(pr[id])

#for i in range(5):
    #print(pr[x_data[i]])
print("----------------------------")

nodes_list = list(G.nodes())
n = len(nodes_list)
#print(nodes_list)

with open('../alpha_dir/facebook/alpha_15.pkl', 'rb') as f:
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
    
pr_value_15 = []

for id in labels_data:
    pr_value_15.append(ppr_sum_dic[id])

#for i in range(10):
    #print(y_data[i])
print("----------------------------")

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
ax.set_ylabel("PR value", fontsize=14)

x = np.arange(len(labels_data))

ax.set_xscale('log')
ax.set_yscale('log')

ax.scatter(x, pr_value, label="original", s=10)
ax.scatter(x, pr_value_15, label="alpha=75~10%", s=10)


plt.legend()
plt.show()