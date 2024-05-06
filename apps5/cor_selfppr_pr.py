# self PPR と PR の相関を見るコード

from utils import *
import pickle
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib import rcParams as rcp


# /usr/bin/python3 /Users/tyama/tyama_exp/apps5/cor_selfppr_pr.py

# -------------------------- データ読み込み -------------------------

# データセットの 名前　と 有向か無向か
datasets = {"dolphins" : False, "facebook" : False}

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
# self PPR を計算

# {データセット名：{ノードID : selfPPR}}
self_ppr_dic = {dataset_name : {} for dataset_name in datasets}

# self PPR の合計値
self_ppr_sum_dic = {dataset_name : 0 for dataset_name in datasets}

# alpha の設定
alpha = 15


for dataset_name in datasets:
    path = '../alpha_dir/' + dataset_name + '/self_ppr_' + str(alpha) + '.txt'
    with open(path) as f:
         for line in f:
             (id, val) = line.split()
             self_ppr_dic[dataset_name][int(id)] = float(val)
             self_ppr_sum_dic[dataset_name] += float(val)
             
# self PPR 値を正規化

for dataset_name in datasets:
    node_list = G_dic[dataset_name].nodes
    
    for node in node_list:
        self_ppr_dic[dataset_name][node] /= self_ppr_sum_dic[dataset_name]
    
#------------------------------------------------------------------

#------------------------------------------------------------------
# PPR から PR 演算

# # alpha の設定
# alpha = 15

# # {データセット名：{source_node : [ppr値]}}
# ppr_dic = {}

# for dataset_name in datasets:
#     path = '../alpha_dir/' + dataset_name + '/alpha_' + str(alpha) + '.pkl'
#     with open(path, 'rb') as f:
#         ppr_dic[dataset_name] = pickle.load(f)

# # PR 計算
# pr_by_ppr_dic = {}

# for dataset_name in datasets:
#     pr_obj = PR(G_dic[dataset_name])
#     node_list = G_dic[dataset_name].nodes
#     pr = pr_obj.calc_pr_by_ppr(ppr_dic[dataset_name], node_list)
            
#     pr_by_ppr_dic[dataset_name] = pr

# networkx で計算
pr_by_ppr_dic = {}
for dataset_name in datasets:
    pr_by_ppr_dic[dataset_name] = nx.pagerank(G_dic[dataset_name], alpha=0.85)
    
print("End calc")

#------------------------------------------------------------------

#------------------------------------------------------------------
# self PPR と PPR の関係をプロット

for dataset_name in datasets:
    
    # フォントを設定する。
    rcp['font.family'] = 'sans-serif'
    rcp['font.sans-serif'] = ['Hiragino Maru Gothic Pro', 'Yu Gothic', 'Meirio', 'Takao', 'IPAexGothic', 'IPAPGothic', 'VL PGothic', 'Noto Sans CJK JP']

    # カラーマップを用意する。
    cmap = plt.get_cmap("tab10")

    # Figureを作成する。
    fig = plt.figure()
    # Axesを作成する。
    ax = fig.add_subplot(111)

    # Figureの解像度と色を設定する。
    fig.set_dpi(150)
    fig.set_facecolor("white")

    # Axesのタイトルと色を設定する。
    #ax.set_title("物品の所有率")
    ax.set_facecolor("white")

    ax.set_xscale('log')
    ax.set_yscale('log')

    # x軸とy軸のラベルを設定する。
    ax.set_xlabel("Normalized Self PPR value", fontsize=14)
    ax.set_ylabel("PR value", fontsize=14)


    node_list = G_dic[dataset_name].nodes

    #for node in node_list:
        #ax.scatter(self_ppr_dic[dataset_name][node], pr_by_ppr_dic[dataset_name][node], c="blue")
    
    self_ppr_val = []
    pr_val = []    
    for node in node_list:
        self_ppr_val.append(self_ppr_dic[dataset_name][node])
        pr_val.append(pr_by_ppr_dic[dataset_name][node])
        
    ax.scatter(self_ppr_val, pr_val)

    # グリッドを表示する。
    ax.set_axisbelow(True)
    ax.grid(True, "major", "x", linestyle="--")
    ax.grid(True, "major", "y", linestyle="--")

    #plt.legend()
    plt.tight_layout()
    plt.show()

#------------------------------------------------------------------




