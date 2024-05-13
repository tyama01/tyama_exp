# 自ノード PPR で重み付けした中心性指標

from utils import *
import networkx as nx
import sys
import pickle
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import math
import matplotlib as mpl
from matplotlib import rcParams as rcp
from scipy.stats import kendalltau


# /usr/bin/python3 /Users/tyama/tyama_exp/apps5/output_selfppr.py

# -------------------------- データ読み込み -------------------------
#dataset_name = input("Enter the dataset name: ")
dataset_name = "epinions"
data_loader = DataLoader(dataset_name, is_directed=True)
G = data_loader.get_graph()
print(G) # グラフのノード数、エッジ数出力

#data_loader.load_community()

# {所属するコミュニティ：頂点idのリスト}, {頂点id:所属するコミュニティ}
#c_id, id_c = data_loader.get_communities() 

print("-----------------------------------")

node_list = list(G.nodes)
n = len(node_list)
#------------------------------------------------------------------

#------------------------------------------------------------------
# 自ノードから見た自ノードの評価 PPR を計算
self_ppr_obj = SelfPPR(G)

self_ppr_dic = dict()

for v in node_list:
    self_ppr_value = self_ppr_obj.calc_self_ppr_by_random_walk(source_id=v, count=1000, alpha=0.15)
    self_ppr_dic[v] = self_ppr_value


# txt file に出力
f = open('../alpha_dir/' + dataset_name + '/self_ppr_15.txt', 'a', encoding='UTF-8')
for tmp_self_ppr in sorted(self_ppr_dic.items(), key=lambda x:x[1], reverse=True):
    f.write(str(tmp_self_ppr[0]))
    f.write(' ')
    f.write(str(tmp_self_ppr[1]))
    f.write('\n')

print("End")

#------------------------------------------------------------------


