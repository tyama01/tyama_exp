from utils import *
import networkx as nx 
import pickle

# /usr/bin/python3 /Users/tyama/tyama_exp/apps/calc_pr_by_ppr.py

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
n = len(nodes_list)
#print(nodes_list)

with open('../alpha_dir/facebook/alpha_15.pkl', 'rb') as f:
    ppr_dic = pickle.load(f)
    
ppr_sum_dic = {node : 0 for node in ppr_dic}

for src_node in ppr_dic:
    for node in nodes_list:
        if node in ppr_dic[src_node]:
            ppr_sum_dic[node] += ppr_dic[src_node][node] / n
        else:
            continue
ppr_sum_dic_sort = sorted(ppr_sum_dic.items(), key=lambda x:x[1], reverse=True)
y_data = []
for item in ppr_sum_dic_sort:
    y_data.append(item[0])

for i in range(5):
    print(ppr_sum_dic[y_data[i]])
print("----------------------------")