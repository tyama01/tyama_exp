# 人工グラフ SBM 生成

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


# /usr/bin/python3 /Users/tyama/tyama_exp/apps8/generate_sbm_graph.py

#------------------------------------------------------------------

# パラメータ設定
## 対角成分（クラスタ内）を密に、他を疎にしています。
sizes = [100, 200, 300]
probs = [
    [0.3, 0.003, 0.003], 
    [0.003, 0.3, 0.003],
    [0.003, 0.003, 0.3]
]
G = nx.stochastic_block_model(sizes, probs, seed=0)

print(G)

# 出力
nx.write_edgelist(G, "../datasets/sbm03.txt", data=False)

#------------------------------------------------------------------
