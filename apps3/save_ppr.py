from utils import *
import networkx as nx 
import pickle


# /usr/bin/python3 /Users/tyama/tyama_exp/apps3/save_ppr.py


# ---------------- データ読み込み ------------------
dataset_name = input("Enter the dataset name: ")
data_loader = DataLoader(dataset_name, is_directed=True)
G = data_loader.get_graph()
print(G) # グラフのノード数、エッジ数出力
print("-----------------------------------")

node_list = list(G.nodes)
n = len(node_list)

# -----------------------------------------------

# ------------------- PPR -----------------------
ppr_obj = PPR(G)

ppr_dic = {}

for v in node_list:
    ppr = ppr_obj.calc_ppr_by_random_walk(source_id=v, count=10000, alpha=0.95)
    ppr_dic[v] = ppr
    
with open('../alpha_dir/wiki/alpha_95.pkl', 'wb') as f:
    pickle.dump(ppr_dic, f)