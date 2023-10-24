from StandAloneGraph import *
from utils import *
import networkx as nx

# /usr/bin/python3 /Users/tyama/tyama_exp/apps/test.py

dataset_name = input("Enter the dataset name: ")
data_loader = DataLoader(dataset_name)
data_loader.load_graph()
G = data_loader.get_graph()

pr = nx.pagerank(G, alpha=0.85)
#print(pr)
pr_sort = sorted(pr.items(), key=lambda x:x[1], reverse=True)

x_data = []
for item in pr_sort:
    x_data.append(item[0])

for i in range(5):
    print(pr[x_data[i]])
print("----------------------------")

nodes_list = list(G.nodes())
#print(nodes_list)
file_path = "../datasets/facebook.txt"
is_directed = False

ppr_obj = StandAloneGraph(file_path, is_directed)

ppr_list = []

for v in nodes_list:
    ppr = ppr_obj.calc_ppr_by_random_walk(source_id=v, count=10000, alpha=0.15)
    ppr_list.append(ppr)
#print(ppr)

ppr_sum_dic = {node : 0 for node in nodes_list}
n = len(nodes_list)

for i in range(len(ppr_list)):
    for node in nodes_list:
        if node in ppr_list[i]:
            ppr_sum_dic[node] += ppr_list[i][node]/n
        else:
            continue
        
ppr_sum_dic_sort = sorted(ppr_sum_dic.items(), key=lambda x:x[1], reverse=True)
y_data = []
for item in ppr_sum_dic_sort:
    y_data.append(item[0])

for i in range(5):
    print(ppr_sum_dic[y_data[i]])
print("----------------------------")
        
#print(ppr_sum_dic)
    
#print(val)
