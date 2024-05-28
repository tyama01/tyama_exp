# FORA で求めた ppr との 実行時間や精度を比較

# コミュニティごとでの SelfPPR の相関を見るコード

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

# /usr/bin/python3 /Users/tyama/tyama_exp/apps6/test_ppr.py

# -------------------------- データ読み込み -------------------------
#dataset_name = input("Enter the dataset name: ")
dataset_name = "digraph_toy"
data_loader = DataLoader(dataset_name, is_directed=False)
G = data_loader.get_graph()
print(G) # グラフのノード数、エッジ数出力


print("-----------------------------------")

node_list = list(G.nodes)
n = len(node_list)
#------------------------------------------------------------------

#------------------------------------------------------------------

# RW で PR 演算
ppr_obj = PPR(G)

# Node ID 0 の PPR

rw_ppr = ppr_obj.calc_ppr_by_random_walk(source_id=1, count=10**6, alpha=0.15)


#print(rw_ppr)

#------------------------------------------------------------------

#------------------------------------------------------------------
# # FORA

# fora_obj = FORA(G)


# fora_ppr = fora_obj.calc_PPR_by_fora(source_node=1, alpha=0.15, walk_count=10**6, has_index=False)


# print(fora_ppr)

#------------------------------------------------------------------
# thenter FP

fp_obj = FP(G)

source_node = 1
alpha = 0.15
eps = 10 ** -6
fp_ppr = fp_obj.calc_ppr_by_forward_push(source_node, alpha, eps)

print(fp_ppr[source_node])

#------------------------------------------------------------------

#------------------------------------------------------------------
# self PPR

#------------------------------------------------------------------
selfppr_obj = SelfPPR(G)
self_ppr = selfppr_obj.calc_self_ppr_by_random_walk(source_node, count=10**6, alpha=0.15)


#------------------------------------------------------------------
# 比較


sort_list = sorted(rw_ppr.items(), key=lambda x:x[1], reverse=True)

for item in sort_list:
    print(f"ID {item[0]} {rw_ppr[item[0]]}  {fp_ppr[item[0]]} {self_ppr[item[0]]}")

#print(f"ID 0 : {rw_ppr[0]}  {fora_ppr[0]}")

#------------------------------------------------------------------



# # NDCG
# ndcg_obj = NDCG(n)
# ndcg = ndcg_obj.calc_ndcg(rw_ppr, fora_ppr, x_ratio=0.5)

# print(f"NDCG : {ndcg}")

# # tau






