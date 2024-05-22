# 完全グラフを生成するコード
import networkx as nx 

# /usr/bin/python3 /Users/tyama/tyama_exp/apps6/generate_comp_graph.py

# 完全グラフ生成

G = nx.complete_graph(100, create_using=None)

# 出力
nx.write_edgelist(G, "../datasets/dbl.txt", data=False)