from StandAloneGraph import *
import pickle

# /usr/bin/python3 /Users/tyama/tyama_exp/apps/save_ppr.py

file_path = "../datasets/facebook.txt"
is_directed = False

ppr_obj = StandAloneGraph(file_path, is_directed)

nodes_dic = ppr_obj.get_nodes_dic()

ppr_dic = {}

for v in nodes_dic:
    ppr = ppr_obj.calc_ppr_by_random_walk(source_id=v, count=10000, alpha=0.95)
    ppr_dic[v] = ppr
    
with open('alpha_95.pkl', 'wb') as f:
    pickle.dump(ppr_dic, f)

