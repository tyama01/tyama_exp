import networkx as nx
import random

class DataLoader:
    def __init__(self, dataset_name):
        self.dataset_name = dataset_name
        self.G = nx.Graph()
        self.c_id = {}
        self.id_c = {}

    def load_graph(self):
        dataset_path = "../datasets/" + self.dataset_name + ".txt"
        with open(dataset_path, 'r') as f:
            lines = f.readlines()
        for line in lines:
            data = line.split()
            if data[0] == data[1]:
                continue
            self.G.add_edge(int(data[0]), int(data[1]))

    def load_community(self):
        community_path = "../datasets/" + self.dataset_name + "_louvain.txt"
        with open(community_path, 'r') as f:
            lines = f.readlines()
        for line in lines:
            data = line.split()
            self.c_id.setdefault(int(data[0]), []).append(int(data[1]))
            self.id_c[int(data[1])] = int(data[0])

    def get_graph(self):
        return self.G

    def get_communities(self):
        return self.c_id, self.id_c

class RandomWalk:
    def random_walk(self, G, v, walk_num, v_walk_num_cnt):
        for i in range(walk_num + 1):
            if v in v_walk_num_cnt:
                v_walk_num_cnt[v] += 1
            else:
                v_walk_num_cnt[v] = 1

            neighbors = list(G.neighbors(v))
            random_index = random.randrange(len(neighbors))
            v = neighbors[random_index]

        return v_walk_num_cnt

    def pr_random_walk(self, G, v, walk_num, v_walk_num_cnt, d):
        node_list = list(G.nodes)

        for i in range(walk_num + 1):
            if v in v_walk_num_cnt:
                v_walk_num_cnt[v] += 1
            else:
                v_walk_num_cnt[v] = 1

            r_value = random.random()

            if r_value <= d:
                neighbors = list(G.neighbors(v))
                random_index = random.randrange(len(neighbors))
                v = neighbors[random_index]
            else:
                random_index = random.randrange(len(node_list))
                v = node_list[random_index]

        return v_walk_num_cnt
    
    def random_walk_betweenness_centrality(self, G, num_walks=10000, walk_length=1000):
        betweenness_centrality = {node: 0.0 for node in G.nodes()}

        for _ in range(num_walks):
            start_node = random.choice(list(G.nodes()))
            visited_nodes = set([start_node])
            
            
            for _ in range(walk_length - 1):
                neighbors = list(G.neighbors(start_node))
                if not neighbors:
                    break
                next_node = random.choice(neighbors)
                visited_nodes.add(next_node)
                start_node = next_node

            for node in visited_nodes:
                betweenness_centrality[node] += 1.0

        total_walks = num_walks * walk_length
        for node in G.nodes():
            betweenness_centrality[node] /= total_walks

        return betweenness_centrality
