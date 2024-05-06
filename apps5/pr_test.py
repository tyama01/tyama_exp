# ppr から PR を求めるのと networkx からPR を求める際の順位比較

from utils import *
import networkx as nx
import pickle
from scipy.stats import kendalltau

# /usr/bin/python3 /Users/tyama/tyama_exp/apps5/pr_test.py

# -------------------------- データ読み込み -------------------------

# データセットの 名前　と 有向か無向か
datasets = {"dolphins" : False, "email" : True, "facebook" : False, "wiki" : True}
#datasets = {"dolphins" : False, "facebook" : False, "twitter" : True, "Google" : True}


# グラフ G_dic[dataset名]
G_dic = {}

print("-----------------------------------")

for dataset_name in datasets:
    data_loader = DataLoader(dataset_name=dataset_name, is_directed=datasets[dataset_name])
    G_dic[dataset_name] = data_loader.get_graph()
    print(f"{dataset_name} : {G_dic[dataset_name]}")
    print("-----------------------------------")
     

#------------------------------------------------------------------

#------------------------------------------------------------------
# networkx の PR を計算
nx_pr_dic = {}
nx_pr_sort_dic = {}

for dataset_name in datasets:
    nx_pr_dic[dataset_name] = nx.pagerank(G_dic[dataset_name], alpha=0.85)
    nx_pr_sort_dic[dataset_name] = sorted(nx_pr_dic[dataset_name].items(), key=lambda x : x[1], reverse=True)

# PR をソートした ID と値を格納
id_sort_dic = {dataset_name : [] for dataset_name in datasets}
pr_value_sort_dic = {dataset_name : [] for dataset_name in datasets}

for dataset_name in datasets:
    for item in nx_pr_sort_dic[dataset_name]:
        id_sort_dic[dataset_name].append(item[0])
        pr_value_sort_dic[dataset_name].append(item[1])
        
#------------------------------------------------------------------

#------------------------------------------------------------------
# PPR からの PR を計算

# alpha の設定
alpha = 15

# {データセット名：{source_node : [ppr値]}}
ppr_dic = {}

for dataset_name in datasets:
    path = '../alpha_dir/' + dataset_name + '/alpha_' + str(alpha) + '.pkl'
    with open(path, 'rb') as f:
        ppr_dic[dataset_name] = pickle.load(f)

# PR 計算
pr_by_ppr_dic = {}

for dataset_name in datasets:
    pr_obj = PR(G_dic[dataset_name])
    node_list = G_dic[dataset_name].nodes
    n = len(node_list)
    pr = pr_obj.calc_pr_by_ppr(ppr_dic[dataset_name], node_list)
    
    # pr = {target_node : 0 for target_node in ppr_dic[dataset_name]}
    # for src_node in ppr_dic[dataset_name]:
    #     for target_node in node_list:
    #         if target_node in ppr_dic[dataset_name][src_node]:
    #             pr[target_node] += ppr_dic[dataset_name][src_node][target_node] / n
                
    #         else:
    #             continue
            
    pr_by_ppr_dic[dataset_name] = pr
                
                
pr_by_ppr_value_sort_dic = {dataset_name : [] for dataset_name in datasets}

for dataset_name in datasets:
    for id in id_sort_dic[dataset_name]:
        pr_by_ppr_value_sort_dic[dataset_name].append(pr_by_ppr_dic[dataset_name][id])



#------------------------------------------------------------------

#------------------------------------------------------------------
# ケンドール順位相関係数の計算

for dataset_name in datasets:
    tau, pvalue = kendalltau(pr_value_sort_dic[dataset_name], pr_by_ppr_value_sort_dic[dataset_name])
    print(f"{dataset_name} tau : {tau}")
    
print("-----------------------------------")


#------------------------------------------------------------------

#------------------------------------------------------------------
# NDCG を計算

for dataset_name in datasets:
    n = len(G_dic[dataset_name].nodes)
    ndcg_obj = NDCG(n)
    ndcg = ndcg_obj.calc_ndcg(nx_pr_dic[dataset_name], pr_by_ppr_dic[dataset_name], x_ratio=0.1)
    print(f"{dataset_name} NDCG : {ndcg}")
    
print("-----------------------------------")


#------------------------------------------------------------------




