import networkx as nx
import random

def label_propagation(graph, max_iters=100):
    labels = {node: node for node in graph.nodes()}  # Initialize each node with its own label

    for _ in range(max_iters):
        nodes = list(graph.nodes())
        random.shuffle(nodes)

        for node in nodes:
            neighbors = list(graph.neighbors(node))
            if neighbors:
                neighbor_labels = [labels[n] for n in neighbors]
                most_common_label = max(neighbor_labels, key=neighbor_labels.count)
                labels[node] = most_common_label

    # Group nodes by their labels to form communities
    communities = {}
    for node, label in labels.items():
        if label in communities:
            communities[label].append(node)
        else:
            communities[label] = [node]

    return list(communities.values())

# Create a random graph for demonstration
G = nx.karate_club_graph()

# Apply the label propagation algorithm for community detection
detected_communities = label_propagation(G)

# Print detected communities
for i, community in enumerate(detected_communities):
    print(f"Community {i + 1}: {community}")
