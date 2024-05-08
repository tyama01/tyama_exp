from StandAloneGraph import *
from func import *

file_path = "dataset/indexed_edges.txt"
is_directed = True
alpha = 0.15
walk_count = 10 ** 6
k = 12

graph = StandAloneGraph(file_path, is_directed)

node_count = len(graph.nodes)
print("Input Graph has {} nodes\n\n".format(node_count))

graph.set_index_for_fora_plus(alpha)

source_id_list = random.sample(list(range(node_count)), 5)

for source_id in source_id_list:
    approx_ppr = graph.calc_PPR_by_fora(source_id, alpha, walk_count, True)
    exact_ppr = graph.calc_ppr_by_power_iteration(source_id, alpha, 10 ** (-9))

    approx_ranking = get_ranking(approx_ppr, k)
    exact_ranking = get_ranking(exact_ppr, k)

    print("source_id: {}, NDCG: {}\n".format(source_id, calc_ndcg(approx_ranking, exact_ppr, k)))
    print("ranking\tnode_id\texact ppr\tapprox. ppr")
    for ranking, node_id in enumerate(exact_ranking):
        print(ranking+1, node_id, exact_ppr.get(node_id, 0), approx_ppr.get(node_id, 0))
    print()