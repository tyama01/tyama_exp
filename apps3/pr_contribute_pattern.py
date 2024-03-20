# PR の貢献度合いを調査するコード パターン別

from utils import *
import networkx as nx
import sys
import pickle
import matplotlib.pyplot as plt
import numpy as np


# /usr/bin/python3 /Users/tyama/tyama_exp/apps3/pr_contribute_pattern.py


# ---------------- データ読み込み ------------------
dataset_name = input("Enter the dataset name: ")
data_loader = DataLoader(dataset_name, is_directed=False)
G = data_loader.get_graph()
print(G) # グラフのノード数、エッジ数出力

data_loader.load_community()

# {所属するコミュニティ：頂点idのリスト}, {頂点id:所属するコミュニティ}
c_id, id_c = data_loader.get_communities() 

print("-----------------------------------")

node_list = list(G.nodes)
n = len(node_list)

# -------------------- 6パターン定義 ---------------------------

# 単調増加
def is_inc(array):
    c = True
    for i in range(len(array) - 1):
        # 配列内の要素を順番に比較し、単調増加かどうかを判定
        c = c and array[i] <= array[i + 1]
        
    return c

# 単調減少
def is_dec(array):
    d = True  # 単調減少を示すフラグ
    for i in range(len(array) - 1):
        d = d and array[i] >= array[i + 1]
    
    return d

# 下に凸　
def is_down(array):
    down = True
   
    max_val = max(array)
    max_val_index = array.index(max_val)
    
    min_val = min(array)
    min_val_index = array.index(min_val)
    
    if (min_val_index != 0) and (min_val_index != (len(array) - 1)):
        if (max_val_index == 0) or (max_val_index == (len(array) - 1)):
            down = True
        else:
            down = False
    
    else:
        down = False
            
    return down

# 上に凸 hub ver
def is_up_hub_ver(array):
    up = True
    
    if(array[0] <= array[len(array) - 1]):
        up = False
        return up
    
    max_val = max(array)
    max_val_index = array.index(max_val)
    
    min_val = min(array)
    min_val_index = array.index(min_val)
    
    if (max_val_index != 0) and (max_val_index != (len(array) - 1)):
        if (min_val_index == 0) or (min_val_index == (len(array) - 1)):
            up = True
        else:
            up = False
    
    else:
        up = False
   
    return up

# 上に凸　unkowon ver
def is_up_unkown_ver(array):
    up =True
    
    if(array[0] >= array[len(array) - 1]):
        up = False
        return up
    
    max_val = max(array)
    max_val_index = array.index(max_val)
    
    min_val = min(array)
    min_val_index = array.index(min_val)
    
    if (max_val_index != 0) and (max_val_index != (len(array) - 1)):
        if (min_val_index == 0) or (min_val_index == (len(array) - 1)):
            up = True
        else:
            up = False
    
    else:
        up = False
    
    
    return up
     
#------------------------------------------------------------------
#------------------------------------------------------------------

# 6パターンごとに分類したリスト
pattern_list = []
pattern_num = 1
print(f'pattern : {pattern_num}')
path = '../pattern_dir/facebook/pattern' + str(pattern_num) + '.txt'

with open(path, 'r', encoding='utf-8') as fin:
    for line in fin.readlines():
        try:
            num = int(line)
        except ValueError as e:
            print(e, file=sys.stderr)
            continue
        pattern_list.append(num)
        
#------------------------------------------------------------------

#------------------------- PR 読み込み------------------------------

nodes_list = list(G.nodes())
n = len(nodes_list)

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

# {node_id : [alpha ごとのPR値]}
focus_id_pr_dic = {}

for focus_id in pattern_list:
    pr_value_list = []
    for alpha in alpha_list:
        pr_value_list.append(pr_alpha_dic[alpha][focus_id])
    focus_id_pr_dic[focus_id] = pr_value_list
    
#------------------------------------------------------------------

#------------------------------------------------------------------
# 着目しているノードについての詳細な分析

# 着目しているノード
focus_id = pattern_list[0]

# 着目しているノードの所属コミュニティ
com_id = id_c[focus_id]

# 着目してるノードの次数
focus_id_degree = G.degree(focus_id)

print(f'focus_id = {focus_id}, com_id = {com_id}, degree = {focus_id_degree}')

# PR の貢献度

# alpha の値を設定
alpha = 15
print(f'alpha = {alpha}')
path = '../alpha_dir/facebook/alpha_' + str(alpha) + '.pkl'
with open(path, 'rb') as f:
    ppr_dic = pickle.load(f)

# {ノードID : ppr 値 を正規化した値}　自身は除く
pr_of_ppr_dic = {}

for node in node_list:
    
    if node == focus_id: # 自身は除く
        continue
    
    else:
        if focus_id in ppr_dic[node]:
            pr_of_ppr_dic[node] = ppr_dic[node][focus_id] / n

print(f'contribute nodes num : {len(pr_of_ppr_dic)}')

# 着目ノードとの最短距離を分類

# {最短距離 : [node id]}
shortest_path_dic = {}

# {最短距離 : [ppr 値]}
shortest_path_ppr_val_dic = {}      
  

for src_node in pr_of_ppr_dic:
    
    shortest_path_length = nx.shortest_path_length(G, source=src_node, target=focus_id)
    
    if shortest_path_length not in shortest_path_dic:
        shortest_path_dic[shortest_path_length] = [src_node]
        shortest_path_ppr_val_dic[shortest_path_length] = [pr_of_ppr_dic[src_node]]
        
    else:
        shortest_path_dic[shortest_path_length].append(src_node)
        shortest_path_ppr_val_dic[shortest_path_length].append(pr_of_ppr_dic[src_node])
        
        
print(len(shortest_path_dic))
print(shortest_path_ppr_val_dic[6][0])


# 着目しているノードのPRに貢献しているノードの次数を最短距離で分類
#{最短距離： [次数]}
contribute_nodes_degree_dic = {}

for path_length in shortest_path_dic:
    
    degree_list = []
    for src_node in shortest_path_dic[path_length]:
        degree = G.degree(src_node)
        degree_list.append(degree)
    
    contribute_nodes_degree_dic[path_length] = degree_list
        
        
# 所属コミュニティの関係
# {所属コミュニティ : ノード数}
belong_com_dic = {com_id : 0 for com_id in c_id}

for node in pr_of_ppr_dic:
    belong_com_dic[id_c[node]] += 1
    
print(belong_com_dic)

#------------------------------------------------------------------

#------------------------------------------------------------------
# プロット

# 最小距離の最大値を取り出す
shortest_path_list = [path for path in shortest_path_dic]
shortest_path_max = max(shortest_path_list)

# 横軸　１つ目　着目ノードとの距離
x1 = np.arange(1, shortest_path_max+1, 1)

fig = plt.figure()

#------------------------------------------------------------------


ax1 = fig.add_subplot(2, 2, 1)

# 距離と PR 貢献度
y1 = []

for key in x1:
    if key in shortest_path_ppr_val_dic:
        y1.append(shortest_path_ppr_val_dic[key])
    else:
        y1.append([])

print(type(shortest_path_ppr_val_dic[1]))

ax1.boxplot(y1)
ax1.set_xlabel("shortest path length")
ax1.set_ylabel("ppr value")

#------------------------------------------------------------------


ax2 = fig.add_subplot(2, 2, 2)

# 距離とノード数の関係
y2 = []


for key in x1:
    if key in shortest_path_ppr_val_dic:
        y2.append(len(shortest_path_ppr_val_dic[key]))
    else:
        y2.append(0)

ax2.bar(x1, y2, align="center")
ax2.set_xlabel("shortest path length")
ax2.set_ylabel("num of nodes")

#------------------------------------------------------------------


ax3 = fig.add_subplot(2, 2, 3)


# 距離と次数の関係
y3 = []

for key in x1:
    if key in contribute_nodes_degree_dic:
        y3.append(contribute_nodes_degree_dic[key])
    else:
        y3.append([])
        
        
ax3.boxplot(y3)

focus_id_degree_list = []
for _ in x1:
    focus_id_degree_list.append(focus_id_degree)

ax3.plot(x1, focus_id_degree_list, c="r", linestyle = "dashed")
ax3.set_xlabel("shortest path length")
ax3.set_ylabel("degree")


#------------------------------------------------------------------

ax4 = fig.add_subplot(2, 2, 4)
# 所属コミュニティとの関係

y = []
for i in range(len(c_id)):
    y.append(len(c_id[i]))

z = np.sort(y)[::-1]
com_size_sort_data = np.argsort(y)[::-1] # コミュニティサイズが大きいラベル

x2 = np.arange(len(com_size_sort_data))

y4 = []


for com_id in com_size_sort_data:
    y4.append(belong_com_dic[com_id])
    
ax4.bar(x2, y4, align="center", tick_label=com_size_sort_data)
ax4.set_xlabel("community labels")
ax4.set_ylabel("num of nodes")

fig.tight_layout()
plt.show()

#------------------------------------------------------------------




