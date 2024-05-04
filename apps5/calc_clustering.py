# 各ノードのクラスタリング係数を計算

# /usr/bin/python3 /Users/tyama/tyama_exp/apps5/calc_clustering.py

from utils import *
import networkx as nx

# -------------------------- データ読み込み -------------------------
dataset_name = input("Enter the dataset name: ")
data_loader = DataLoader(dataset_name, is_directed=True)
G = data_loader.get_graph()
print(G) # グラフのノード数、エッジ数出力

print("-----------------------------------")

node_list = list(G.nodes)
n = len(node_list)
#------------------------------------------------------------------

# 全ノードのクラスタリング係数を計算
clustering = nx.clustering(G)

# 正規化
c_sum = 0

for node in node_list:
    c_sum += clustering[node]
    
for node in node_list:
    clustering[node] /= c_sum
    
# 検算
c_sum = 0

for node in node_list:
    c_sum += clustering[node]

print(c_sum)

#------------------------------------------------------------------

#------------------------------------------------------------------
# txt ファイルに出力
path = '../clustering_dir/' + str(dataset_name) + '_clustering.txt'
f = open(path,'a', encoding='UTF-8')
for tmp_clustering in sorted(clustering.items(), key=lambda x:x[1], reverse=True):
    f.write(str(tmp_clustering[0]))
    f.write(' ')
    f.write(str(tmp_clustering[1]))
    f.write('\n')
    
print("End")

#------------------------------------------------------------------

  
    