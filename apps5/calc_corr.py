# self PPR の α を変更させた場合と clustering 係数の相関係数をプロットするコード

from utils import *
import pickle
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib import rcParams as rcp


# /usr/bin/python3 /Users/tyama/tyama_exp/apps5/calc_corr.py

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
# self PPR を読み込む

# alpha を 0.5 ~ 0.95 まで変化させる
alpha_list = [alpha for alpha in range(5, 100, 5)]

# {データセット名：{alpha : {Node ID : selfPPR}}}
self_ppr_dic = {dataset_name : {alpha : {} for alpha in alpha_list} for dataset_name in datasets}

for dataset_name in datasets:
    for alpha in alpha_list:
        # self PPR の合計値
        self_ppr_sum_dic = {dataset_name : 0 for dataset_name in datasets}
        
        path = '../alpha_dir/' + dataset_name + '/self_ppr_' + str(alpha) + '.txt'
        with open(path) as f:
            for line in f:
                (id, val) = line.split()
                self_ppr_dic[dataset_name][alpha][int(id)] = float(val)
                self_ppr_sum_dic[dataset_name] += float(val)        
                
        # 正規化
        node_list = G_dic[dataset_name].nodes
        for node in node_list:
            self_ppr_dic[dataset_name][alpha][node] /= self_ppr_sum_dic[dataset_name]
        
#------------------------------------------------------------------

#------------------------------------------------------------------
# Clustering 係数　読み込み

clustering_dic = {dataset_name : {} for dataset_name in datasets}

for dataset_name in datasets:
    path = '../clustering_dir/' + dataset_name + '_clustering.txt'
    with open(path) as f:
        for line in f:
            (id, val) = line.split()
            clustering_dic[dataset_name][int(id)] = float(val)


#------------------------------------------------------------------

#------------------------------------------------------------------
# 相関係数の計算

corr_dic = {}

for dataset_name in ["dolphins", "facebook"]:
    
    #print(dataset_name)
    corr_list = []
    
    for alpha in alpha_list:
        
        ppr_list = []
        c_list = []
        
        for node in clustering_dic[dataset_name]:
            ppr_list.append(self_ppr_dic[dataset_name][alpha][node])
            c_list.append(clustering_dic[dataset_name][node])
    
        
        s1 = pd.Series(ppr_list)
        s2 = pd.Series(c_list)
        
        res = s1.corr(s2)
        #print(res)
    
        corr_list.append(res)
        
    #print(dataset_name)
    corr_dic[dataset_name] = corr_list
    
        
print(len(alpha_list))

#print(len(corr_dic["dolphins"]))
        
#------------------------------------------------------------------

#------------------------------------------------------------------
# self PPR と clustering係数 の関係をプロット

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
    
    # x軸とy軸のラベルを設定する。
    ax.set_xlabel(r"$\alpha$", fontsize=14)
    ax.set_ylabel("corr", fontsize=14)

    
    alpha_list2 = []
    for alpha in alpha_list:
        alpha_list2.append(alpha/100)
        
    ax.scatter(alpha_list2, corr_dic[dataset_name])
    ax.plot(alpha_list2, corr_dic[dataset_name])
    
    
    # グリッドを表示する。
    ax.set_axisbelow(True)
    ax.grid(True, "major", "x", linestyle="--")
    ax.grid(True, "major", "y", linestyle="--")

    #plt.legend()
    plt.tight_layout()
    plt.show()


#------------------------------------------------------------------



