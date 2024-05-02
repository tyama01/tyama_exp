# self PPR で重みづけをした PR 演算　のランキング変化を tau で比較
# データセット複数

from utils import *
import networkx as nx
import sys
import pickle
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import math
import matplotlib as mpl
from matplotlib import rcParams as rcp
from scipy.stats import kendalltau


# /usr/bin/python3 /Users/tyama/tyama_exp/apps4/calc_tau.py

# -------------------------- データ読み込み -------------------------
# Dolphins 

dataset_name = input("Enter the dataset name (dolphins): ")
data_loader = DataLoader(dataset_name, is_directed=False)
G_dol = data_loader.get_graph()
print(G_dol) # グラフのノード数、エッジ数出力


print("-----------------------------------")

dol_node_list = list(G_dol.nodes)
dol_n = len(dol_node_list)
#------------------------------------------------------------------

# -------------------------- データ読み込み -------------------------
# email-Eu-core 

# dataset_name = input("Enter the dataset name (email): ")
# data_loader = DataLoader(dataset_name, is_directed=True)
# G_email = data_loader.get_graph()
# print(G_email) # グラフのノード数、エッジ数出力


# print("-----------------------------------")

# email_node_list = list(G_email.nodes)
# email_n = len(email_node_list)
#------------------------------------------------------------------

# -------------------------- データ読み込み -------------------------
# ego-Facebook 

dataset_name = input("Enter the dataset name (facebook): ")
data_loader = DataLoader(dataset_name, is_directed=False)
G_fb = data_loader.get_graph()
print(G_fb) # グラフのノード数、エッジ数出力


print("-----------------------------------")

fb_node_list = list(G_fb.nodes)
fb_n = len(fb_node_list)
#------------------------------------------------------------------

# -------------------------- データ読み込み -------------------------
# wiki-Vote 

dataset_name = input("Enter the dataset name (wiki-Vote_gcc): ")
data_loader = DataLoader(dataset_name, is_directed=True)
G_wiki = data_loader.get_graph()
print(G_wiki) # グラフのノード数、エッジ数出力


print("-----------------------------------")

wiki_node_list = list(G_wiki.nodes)
wiki_n = len(wiki_node_list)
#------------------------------------------------------------------

#------------------------------------------------------------------
# 事前準備

# 各データセット名のリスト
#dataset_list = ["Dolphins", "email-Eu-core", "ego-Facebook", "wiki-Vote"]
dataset_list = ["Dolphins", "ego-Facebook", "wiki-Vote"]


# 重みのリスト
w_list = [0, 1, 2, 3, 4]

# 各重みに対する PR

# Dolphins
dol_flow_pr_dic = {}

# email-Eu-core
#email_flow_pr_dic = {}

# ego-Facebook
fb_flow_pr_dic = {}

# wiki-Vote
wiki_flow_pr_dic = {}

# tau 辞書 {"データセット名"： [tau値]}
tau_dic = {dataset : [] for dataset in dataset_list}

#------------------------------------------------------------------

#------------------------------------------------------------------
# dolphins

# 通常のPR 演算

# alpha の値を設定
alpha = 15
#print(f'alpha = {alpha}')
path = '../alpha_dir/dolphins/alpha_' + str(alpha) + '.pkl'
with open(path, 'rb') as f:
    ppr_dic = pickle.load(f)

# 普通の PR を計算
pr = {target_node : 0 for target_node in ppr_dic}

for src_node in ppr_dic:
    for target_node in dol_node_list:
        if target_node in ppr_dic[src_node]:
            pr[target_node] += ppr_dic[src_node][target_node] / dol_n
            
        else:
            continue
        
# 通常の PR を降順にソート
pr_sort = sorted(pr.items(), key=lambda x:x[1], reverse=True)

id_sort = []
pr_value_sort = []
for item in pr_sort:
    id_sort.append(item[0])
    pr_value_sort.append(item[1])
    
# 提案手法
# 自ノードから見た PPR 読み込み
self_ppr_dic = dict()
with open("../alpha_dir/dolphins/self_ppr_15.txt") as f:
    for line in f:
        (id, val) = line.split()
        self_ppr_dic[int(id)] = float(val)
    
flow_pr_obj = flow_PR(G_dol)

for w in w_list:
    flow_pr = flow_pr_obj.calc_flow_rw_pr(self_ppr_dic=self_ppr_dic, alpha=0.15, w=w)
    
    dol_flow_pr_dic[w] = flow_pr
    
# dol_flow_pr の pr 値を格納

dol_flow_pr_sort_dic = {w : [] for w in w_list}

for w in w_list:
    for id in id_sort:
        dol_flow_pr_sort_dic[w].append(dol_flow_pr_dic[w][id])
        
        
# ケンドール順位相関係数を計算

for w in w_list:
    tau, pvalue = kendalltau(pr_value_sort, dol_flow_pr_sort_dic[w])
    tau_dic["Dolphins"].append(tau)
    
print("dolphins end")

#------------------------------------------------------------------

#------------------------------------------------------------------
# # email-Eu-core

# # 通常のPR 演算

# # alpha の値を設定
# alpha = 15
# #print(f'alpha = {alpha}')
# path = '../alpha_dir/email/alpha_' + str(alpha) + '.pkl'
# with open(path, 'rb') as f:
#     ppr_dic = pickle.load(f)

# # 普通の PR を計算
# pr = {target_node : 0 for target_node in ppr_dic}

# for src_node in ppr_dic:
#     for target_node in email_node_list:
#         if target_node in ppr_dic[src_node]:
#             pr[target_node] += ppr_dic[src_node][target_node] / email_n
            
#         else:
#             continue
        
# # 通常の PR を降順にソート
# pr_sort = sorted(pr.items(), key=lambda x:x[1], reverse=True)

# id_sort = []
# pr_value_sort = []
# for item in pr_sort:
#     id_sort.append(item[0])
#     pr_value_sort.append(item[1])
    
# # 提案手法
# # 自ノードから見た PPR 読み込み
# self_ppr_dic = dict()
# with open("../alpha_dir/email/self_ppr_15.txt") as f:
#     for line in f:
#         (id, val) = line.split()
#         self_ppr_dic[int(id)] = float(val)
    
# flow_pr_obj = flow_PR(G_email)

# for w in w_list:
#     flow_pr = flow_pr_obj.calc_flow_rw_pr(self_ppr_dic=self_ppr_dic, alpha=0.15, w=w)
    
#     email_flow_pr_dic[w] = flow_pr
    
# # email_flow_pr の pr 値を格納

# email_flow_pr_sort_dic = {w : [] for w in w_list}

# for w in w_list:
#     for id in id_sort:
#         email_flow_pr_sort_dic[w].append(email_flow_pr_dic[w][id])
        
        
# # ケンドール順位相関係数を計算

# for w in w_list:
#     tau, pvalue = kendalltau(pr_value_sort, email_flow_pr_sort_dic[w])
#     tau_dic["email-Eu-core"].append(tau)
    
# print("email end")


#------------------------------------------------------------------

#------------------------------------------------------------------
# ego-Facebook

# 通常のPR 演算

# alpha の値を設定
alpha = 15
#print(f'alpha = {alpha}')
path = '../alpha_dir/facebook/alpha_' + str(alpha) + '.pkl'
with open(path, 'rb') as f:
    ppr_dic = pickle.load(f)

# 普通の PR を計算
pr = {target_node : 0 for target_node in ppr_dic}

for src_node in ppr_dic:
    for target_node in fb_node_list:
        if target_node in ppr_dic[src_node]:
            pr[target_node] += ppr_dic[src_node][target_node] / fb_n
            
        else:
            continue
        
# 通常の PR を降順にソート
pr_sort = sorted(pr.items(), key=lambda x:x[1], reverse=True)

id_sort = []
pr_value_sort = []
for item in pr_sort:
    id_sort.append(item[0])
    pr_value_sort.append(item[1])

# 提案手法
# 自ノードから見た PPR 読み込み
self_ppr_dic = dict()
with open("../alpha_dir/facebook/self_ppr_15.txt") as f:
    for line in f:
        (id, val) = line.split()
        self_ppr_dic[int(id)] = float(val)
    
flow_pr_obj = flow_PR(G_fb)

for w in w_list:
    flow_pr = flow_pr_obj.calc_flow_rw_pr(self_ppr_dic=self_ppr_dic, alpha=0.15, w=w)
    
    fb_flow_pr_dic[w] = flow_pr
    
# dol_flow_pr の pr 値を格納

fb_flow_pr_sort_dic = {w : [] for w in w_list}

for w in w_list:
    for id in id_sort:
        fb_flow_pr_sort_dic[w].append(fb_flow_pr_dic[w][id])
        
        
# ケンドール順位相関係数を計算

for w in w_list:
    tau, pvalue = kendalltau(pr_value_sort, fb_flow_pr_sort_dic[w])
    tau_dic["ego-Facebook"].append(tau)

print("facebook end")
#------------------------------------------------------------------

#------------------------------------------------------------------
# wiki-Vote

# 通常のPR 演算

# alpha の値を設定
alpha = 15
#print(f'alpha = {alpha}')
path = '../alpha_dir/wiki/alpha_' + str(alpha) + '.pkl'
with open(path, 'rb') as f:
    ppr_dic = pickle.load(f)

# 普通の PR を計算
pr = {target_node : 0 for target_node in ppr_dic}

for src_node in ppr_dic:
    for target_node in wiki_node_list:
        if target_node in ppr_dic[src_node]:
            pr[target_node] += ppr_dic[src_node][target_node] / wiki_n
            
        else:
            continue
        
# 通常の PR を降順にソート
pr_sort = sorted(pr.items(), key=lambda x:x[1], reverse=True)

id_sort = []
pr_value_sort = []
for item in pr_sort:
    id_sort.append(item[0])
    pr_value_sort.append(item[1])
    
# 提案手法
# 自ノードから見た PPR 読み込み
self_ppr_dic = dict()
with open("../alpha_dir/wiki/self_ppr_15.txt") as f:
    for line in f:
        (id, val) = line.split()
        self_ppr_dic[int(id)] = float(val)
    
flow_pr_obj = flow_PR(G_wiki)

for w in w_list:
    flow_pr = flow_pr_obj.calc_flow_rw_pr(self_ppr_dic=self_ppr_dic, alpha=0.15, w=w)
    
    wiki_flow_pr_dic[w] = flow_pr
    
# wiki_flow_pr の pr 値を格納

wiki_flow_pr_sort_dic = {w : [] for w in w_list}

for w in w_list:
    for id in id_sort:
        wiki_flow_pr_sort_dic[w].append(wiki_flow_pr_dic[w][id])
        
        
# ケンドール順位相関係数を計算

for w in w_list:
    tau, pvalue = kendalltau(pr_value_sort, wiki_flow_pr_sort_dic[w])
    tau_dic["wiki-Vote"].append(tau)
    
print("wiki end")


#------------------------------------------------------------------

#------------------------------------------------------------------
# w を変化させた場合の順位相関 タウ をプロット

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
ax.set_xlabel("$\it{w}$", fontsize=14)
ax.set_ylabel("\u03c4", fontsize=14)
ax.set_xticks(w_list)


# x軸の目盛の位置を設定する。
ax.xaxis.set_major_locator(mpl.ticker.FixedLocator(w_list))

# y軸の範囲を設定する。
ax.set_ylim(0, 1.0)
# y軸の目盛の位置を設定する。
ax.yaxis.set_major_locator(mpl.ticker.MultipleLocator(0.1))

for dataset_name in dataset_list:
    ax.scatter(w_list, tau_dic[dataset_name], label=dataset_name)
    ax.plot(w_list, tau_dic[dataset_name])
    
# グリッドを表示する。
ax.set_axisbelow(True)
ax.grid(True, "major", "x", linestyle="--")
ax.grid(True, "major", "y", linestyle="--")

plt.legend()
plt.tight_layout()
plt.show()

#------------------------------------------------------------------
