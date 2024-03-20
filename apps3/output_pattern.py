# ノードが6パターンに分類し、txtファイルに出力するコード

from utils import *
import networkx as nx
import sys
import pickle
import matplotlib.pyplot as plt
import numpy as np


# /usr/bin/python3 /Users/tyama/tyama_exp/apps3/output_pattern.py

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

for focus_id in nodes_list:
    pr_value_list = []
    for alpha in alpha_list:
        pr_value_list.append(pr_alpha_dic[alpha][focus_id])
    focus_id_pr_dic[focus_id] = pr_value_list
    

#{上に凸、下に凸、単調増加、単調減少：[ノードID]}
# pattern1 : 上に凸 pr(0.05) > PR(0.95)
# pattern2 : 上に凸 pr(0.05) < PR(0.95)
# pattern3 : 下に凸
# pattern4 : 単調増加
# pattern5 : 単調減少
# pattern6 : その他

classfication_dic = {'pattern1' : [], 'pattern2' : [], 'pattern3' : [], 'pattern4' : [], 'pattern5' : [], 'pattern6' : []}
for focus_id in nodes_list:
    pr_value_list = focus_id_pr_dic[focus_id]
    
    # 単調増加
    if is_inc(pr_value_list):
        classfication_dic['pattern4'].append(focus_id)
        
    # 単調減少
    elif is_dec(pr_value_list):
        classfication_dic['pattern5'].append(focus_id)
        
    # 下に凸
    elif is_down(pr_value_list):
        classfication_dic['pattern3'].append(focus_id)
        
    # 上に凸 hub ver
    elif is_up_hub_ver(pr_value_list):
        classfication_dic['pattern1'].append(focus_id)
        
    # 上に凸 unknown ver
    elif is_up_unkown_ver(pr_value_list):
        classfication_dic['pattern2'].append(focus_id)
    
    #elif is_down(pr_value_list):
        #classfication_dic['pattern3'].append(focus_id)
    
    # その他
    else:
        classfication_dic['pattern6'].append(focus_id)
        
#------------------------------------------------------------------

#------------------------------------------------------------------
# txt ファイル出力

for pattern in classfication_dic:
    path = '../pattern_dir/facebook/' + pattern + '.txt'
    with open(path, 'w') as f:
        for id in classfication_dic[pattern]:
            f.write("%s\n" %id)            

#------------------------------------------------------------------
