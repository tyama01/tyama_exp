from utils import *
import pickle
import numpy as np
import sys
import matplotlib.pyplot as plt
import matplotlib as mpl
from scipy.stats import linregress
from matplotlib import rcParams as rcp

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
   
    down = down and (array[3] <= array[0] and array[3] <= array[len(array) - 1])
    
    return down

# 上に凸 hub ver
def is_up_hub_ver(array):
    up = True
    
    up = up and (array[0] >= array[len(array) - 1])
    up = up and array[0] <= array[3]
    
    return up

# 上に凸　unkowon ver
def is_up_unkown_ver(array):
    up =True
    
    up = up and (array[0] <= array[len(array) - 1])
    up = up and array[len(array) - 1] <= array[len(array) - 4]
    
    return up
     


# /usr/bin/python3 /Users/tyama/tyama_exp/apps3/classfication.py

dataset_name = input("Enter the dataset name: ")
data_loader = DataLoader(dataset_name, is_directed=False)
data_loader.load_community()
G = data_loader.get_graph()

# {所属するコミュニティ：頂点idのリスト}, {頂点id:所属するコミュニティ}
c_id, id_c = data_loader.get_communities() 

print(G)
print("----------------------------")

nodes_list = list(G.nodes())
n = len(nodes_list)

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

# {node_id : [alpha ごとのPR値]}
focus_id_pr_dic = {}

for focus_id in nodes_list:
    pr_value_list = []
    for alpha in alpha_list:
        pr_value_list.append(pr_alpha_dic[alpha][focus_id])
    focus_id_pr_dic[focus_id] = pr_value_list
    

#{上に凸、下に凸、単調増加、単調減少：[ノードID]}
classfication_dic = {'c_up_hub' : [], 'c_up_unknown' : [], 'c_down' : [], 'm_inc' : [], 'm_dec' : [], 'unknown' : []}
for focus_id in nodes_list:
    pr_value_list = focus_id_pr_dic[focus_id]
    
    # 単調増加
    if is_inc(pr_value_list):
        classfication_dic['m_inc'].append(focus_id)
        
    # 単調減少
    elif is_dec(pr_value_list):
        classfication_dic['m_dec'].append(focus_id)
        
    # 下に凸
    elif is_down(pr_value_list):
        classfication_dic['c_down'].append(focus_id)
        
    # 上に凸 hub ver
    elif is_up_hub_ver(pr_value_list):
        classfication_dic['c_up_hub'].append(focus_id)
        
    # 上に凸 unknown ver
    elif is_up_unkown_ver(pr_value_list):
        classfication_dic['c_up_unknown'].append(focus_id)
    
    # その他
    else:
        classfication_dic['unknown'].append(focus_id)
        
n_2 = 0
for key in classfication_dic:
    n_2 += len(classfication_dic[key])
    print(len(classfication_dic[key]))

print("-------------------------")    
print(n_2)
     