from utils import *
import networkx as nx 
import pickle
import math



# /usr/bin/python3 /Users/tyama/tyama_exp/apps6/save_self_ppr_fora.py

#------------------------------------------------------------------
# RWer 数決定

def calc_omega(delta, n):
    
    # 各種パラメータ
    Pf = 1/n
    eps = 0.01
    
    omega = (4 * math.log(1/Pf)) / ((eps**2) * delta)
    
    return math.ceil(omega)
    


#------------------------------------------------------------------


# ---------------- データ読み込み ------------------
dataset_name = "facebook"
data_loader = DataLoader(dataset_name, is_directed=False)
G = data_loader.get_graph()
print(G) # グラフのノード数、エッジ数出力
print("-----------------------------------")

node_list = list(G.nodes)
n = len(node_list)

# -----------------------------------------------

# Proposed
self_ppr_dic = {}

self_obj = FORA(G)

alpha = 0.15

for node in node_list:
    omega = calc_omega(delta=alpha, n=n)
    tyama_self_ppr = self_obj.calc_PPR_by_fora(source_node=node, alpha=0.15, walk_count=omega, has_index=False)
    tyama_self_ppr[node] = (tyama_self_ppr[node] - alpha) / (1 - alpha)
    self_ppr_dic[node] = tyama_self_ppr
    
    

# -----------------------------------------------
# 結果出力

with open('../alpha_dir/' + dataset_name + '/self_ppr_15_fora.pkl', 'wb') as f:
    pickle.dump(self_ppr_dic, f)
    
print("End")

# -----------------------------------------------