# あるノードをシードとするコミュニティを検出して、pklファイルに出力して保存するコード
# {シードノード ID : [同じコミュニティと判定されたノードID のリスト]}

from utils import *
import networkx as nx 
import pickle
import appr


# /usr/bin/python3 /Users/tyama/tyama_exp/apps5/save_appr.py


# ---------------- データ読み込み ------------------
dataset_name = input("Enter the dataset name: ")
data_loader = DataLoader(dataset_name, is_directed=True)
G = data_loader.get_graph()
print(G) # グラフのノード数、エッジ数出力
print("-----------------------------------")

node_list = list(G.nodes)
n = len(node_list)

# -----------------------------------------------

# -----------------------------------------------
model = appr.APPR(G)

# community = model.compute_appr(seed_node=2)

# print(community)
# print("calc End")

# {シードノード ID : [同じコミュニティと判定されたノードID のリスト]}
appr_dic = {}

for seed in node_list:
    appr_dic[seed] = model.compute_appr(seed_node=seed)

print("calc End")

# 出力
with open('../appr_dir/' + dataset_name + '_appr.pkl', 'wb') as f:
    pickle.dump(appr_dic, f)

# -----------------------------------------------


