from utils import *
import networkx as nx 
import pickle


# /usr/bin/python3 /Users/tyama/tyama_exp/apps5/save_self_ppr.py


# ---------------- データ読み込み ------------------
dataset_name = "facebook_com_1"
data_loader = DataLoader(dataset_name, is_directed=False)
G = data_loader.get_graph()
print(G) # グラフのノード数、エッジ数出力
print("-----------------------------------")

node_list = list(G.nodes)
n = len(node_list)

# -----------------------------------------------

# -----------------------------------------------
# self PPR を計算
self_ppr_obj = SelfPPR(G)
self_ppr_dic = {}
for v in node_list:
    self_ppr = self_ppr_obj.calc_self_ppr_by_random_walk(source_id=v, count=1000, alpha=0.15)
    self_ppr_dic[v] = self_ppr

# -----------------------------------------------
# 結果出力

with open('../alpha_dir/' + dataset_name + '/self_ppr_15.pkl', 'wb') as f:
    pickle.dump(self_ppr_dic, f)
    
print("End")

# -----------------------------------------------
