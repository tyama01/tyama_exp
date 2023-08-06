from community import community_louvain
import networkx as nx
import networkx.algorithms.community as nx_comm
from collections import Counter

FILE_PARH = "../datasets"
#FILE_NAME = "karate"
# FILE_NAME = "web-Google"
FILE_NAME = "facebook"


def main():
    # Input File Path (Source_nodeID    Target_nodeID)
    input_file = "{}/{}.txt".format(FILE_PARH, FILE_NAME)
    # Output File Path (nodeID    CommunityID?)
    output_file = "{}/{}_louvain.txt".format(FILE_PARH, FILE_NAME)

    G = nx.Graph()
    # Reading Graph
    with open(input_file, "r") as f:
        lines = f.readlines()
        for line in lines:
            l = line.split()
            G.add_edge(int(l[0]), int(l[1]))

    # Louvain (dict)
    partition = community_louvain.best_partition(G)
    # partition = nx_comm.louvain_communities(G)
    # print(partition)
    c = Counter(partition.values())
    print(f"{FILE_NAME} count:", len(c))

    # Output (nodeID    CommunityID?)
    with open(output_file, "w") as f:
        for v_id, c_id in partition.items():
            f.write("{}\t{}\n".format(c_id, v_id))


if __name__ == "__main__":
    main()
