# 人工グラフ LFR 生成

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

import pandas as pd


# /usr/bin/python3 /Users/tyama/tyama_exp/apps8/generate_lfr_graph.py

#------------------------------------------------------------------

# LFR 生成

# ノード数
n = 250

# 全体の次数分布のべき指数
tau1 = 3

# コミュニティ内の冪指数
tau2 = 1.5

# コミュニティ外エッジの割合
mu = 0.1

# LFR ベンチマーク生成
G = nx.LFR_benchmark_graph(n=n, tau1=tau1, tau2=tau2, mu=mu, average_degree=5, min_community=20, seed=10)

print(G)

# 出力
nx.write_edgelist(G, "../datasets/LFR.txt", data=False)

communities = list({frozenset(G.nodes[v]["community"]) for v in G})

print(type((communities)))

# コミュニティラベル出力

FILE_PARH = "../datasets"
#FILE_NAME = "karate"
# FILE_NAME = "web-Google"
FILE_NAME = "LFR"

output_file = "{}/{}_louvain.txt".format(FILE_PARH, FILE_NAME)

#{com_id : v_id}
com_list = list()

for com_id in range(len(communities)):
    #print(len(communities[com_id]))
    for v_id in list(communities[com_id]):
        com_list.append((com_id, v_id))
        
        
with open(output_file, "w") as f:
    
    for tmp in com_list:
        f.write("{}\t{}\n".format(tmp[0], tmp[1]))
        
     
        



#------------------------------------------------------------------
