from utils import *
import networkx as nx 
import pickle
from StandAloneGraph import *

# /usr/bin/python3 /Users/tyama/tyama_exp/apps/calc_pr_by_ppr_digver.py

G = nx.read_edgelist("../datasets/digraph_toy.txt", nodetype=int)

node_list = list(G.nodes)
n = len(node_list)

pr = nx.pagerank(G, alpha=0.85)
#print(pr)
pr_sort = sorted(pr.items(), key=lambda x:x[1], reverse=True)

x_data = []
for item in pr_sort:
    x_data.append(item[0])

print("Networkx")
for i in range(n):
    print(f"Node ID : {x_data[i]} | PR value : {pr[x_data[i]]}")
print("----------------------------")

#nodes_list = list(G.nodes())
#n = len(nodes_list)
#print(nodes_list)

file_path = "../datasets/digraph_toy.txt"
is_directed = False

ppr_obj = StandAloneGraph(file_path, is_directed)

nodes_dic = ppr_obj.get_nodes_dic()
print(nodes_dic)

ppr_dic = {}

for v in nodes_dic:
    ppr = ppr_obj.calc_ppr_by_random_walk(source_id=v, count=10000, alpha=0.15)
    ppr_dic[v] = ppr
    
ppr_sum_dic = {node : 0 for node in ppr_dic}

for src_node in ppr_dic:
    for node in node_list:
        if node in ppr_dic[src_node]:
            ppr_sum_dic[node] += ppr_dic[src_node][node] / n
        else:
            continue
        
ppr_sum_dic_sort = sorted(ppr_sum_dic.items(), key=lambda x:x[1], reverse=True)
y_data = []
for item in ppr_sum_dic_sort:
    y_data.append(item[0])

print("use PPR")
for i in range(n):
    print(f"Node ID : {y_data[i]} | PR value : {ppr_sum_dic[y_data[i]]}")
print("----------------------------")