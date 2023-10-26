from StandAloneGraph import *
from utils import *
import pickle

# /usr/bin/python3 /Users/tyama/tyama_exp/apps/save_ppr_calpha.py

# ---------------- データ読み込み ------------------
dataset_name = input("Enter the dataset name: ")
data_loader = DataLoader(dataset_name)
data_loader.load_graph()
data_loader.load_community()
G = data_loader.get_graph()

# {所属するコミュニティ：頂点idのリスト}, {頂点id:所属するコミュニティ}
c_id, id_c = data_loader.get_communities() 

# ---------------------------------------------------

file_path = "../datasets/facebook.txt"
is_directed = False

ppr_obj = StandAloneGraph(file_path, is_directed)

nodes_dic = ppr_obj.get_nodes_dic()

ppr_dic = {}

for com_id in c_id:
    if(len(c_id[com_id]) > 200):
        for v in c_id[com_id]:
            ppr = ppr_obj.calc_ppr_by_random_walk(source_id=v, count=10000, alpha=0.999)
            ppr_dic[v] = ppr
    else:
        for v in c_id[com_id]:
            ppr = ppr_obj.calc_ppr_by_random_walk(source_id=v, count=10000, alpha=0.10)
            ppr_dic[v] = ppr

with open('alpha_999_10.pkl', 'wb') as f:
    pickle.dump(ppr_dic, f)
        