from utils import *
import networkx as nx

# /usr/bin/python3 /Users/tyama/tyama_exp/apps4/test.py


# ---------------- データ読み込み ------------------
dataset_name = input("Enter the dataset name: ")
data_loader = DataLoader(dataset_name, is_directed=False)
G = data_loader.get_graph()
print(G) # グラフのノード数、エッジ数出力
print("-----------------------------------")

node_list = list(G.nodes)
n = len(node_list)

# -----------------------------------------------

levyppr_obj = LevyPPR(G)

ppr_dic = {}

ppr = levyppr_obj.calc_levy_ppr_by_random_walk(source_id=1, count=10000, alpha=0.15, r=2)

sum = 0
for key in ppr:
    sum += ppr[key]
    
print(sum)