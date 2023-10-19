import networkx as nx
import random

# データセット読み込みのクラス (重みなし)
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

# ----------------------------------------------------------------------------

# データセット読み込みのクラス (重みあり)
class DataLoader_W:
    def __init__(self, dataset_name):
        self.dataset_name = dataset_name
        self.G = nx.Graph()
        

    def load_graph(self):
        dataset_path = "../datasets/" + self.dataset_name + ".txt"
        with open(dataset_path, 'r') as f:
            lines = f.readlines()
        for line in lines:
            data = line.split()
            self.G.add_edge(int(data[0]), int(data[1]), weight=float(data[2]))

    def get_graph(self):
        return self.G

# ----------------------------------------------------------------------------


# 周辺類似性指数 PSI エッジの重みづけ
class PSI:
    def __init__(self, G):
        self.G = G
        
        # PSI のエッジの重み {id : {id : 重み}}
        self.psi_edge_weight = {id : {} for id in list(self.G.nodes)}
        
        # PSI　逆数 のエッジの重み {id : {id : 重み}}
        self.reverse_psi_edge_weight = {id : {} for id in list(self.G.nodes)}
    
    # PSI 計算
    def calc_psi(self):
        
        # 全ノードに対して行う
        for id in list(self.G.nodes):
            
            # id の隣接に対して
            neighbors = list(self.G.neighbors(id))
            
            for neigh_id in neighbors:
                self.psi_edge_weight[id][neigh_id] = 1
            
            for neigh_id in neighbors:
                for neigh_neigh_id in neighbors:
                    
                    if (neigh_id == neigh_neigh_id): 
                        continue
                    
                    else:
                        neigh_id_neighbors = list(self.G.neighbors(neigh_id))
                        neigh_id_neighbors.append(neigh_id)
                        
                        neigh_neigh_id_neighbors = list(self.G.neighbors(neigh_neigh_id))
                        neigh_neigh_id_neighbors.append(neigh_neigh_id)
                        
                        d = len(set(neigh_id_neighbors) & set(neigh_neigh_id_neighbors))
                        n = max(len(neigh_id_neighbors), len(neigh_neigh_id_neighbors))
                        
                        self.psi_edge_weight[id][neigh_id] += round(d/n, 1)
        
        return self.psi_edge_weight
    
    # PSI の重みつきグラフを txt ファイルで出力
    def out_put_psi_graph(self, dataset_name):
        
        self.calc_psi()
        
        output_file = dataset_name + "_psi.txt"
        out_path = "../datasets/" + output_file
        
        f = open(out_path, 'w')
        
        for v in self.psi_edge_weight:
            for neigh_v in self.psi_edge_weight[v]:
                f.write(str(v) + " ")
                f.write(str(neigh_v) + " ")
                f.write(str(self.psi_edge_weight[v][neigh_v]))
                f.write('\n')
                
        f.close()
        
    
    # PSI の重みの逆数を計算
    def calc_reverse_psi(self):
        
        self.calc_psi()
        
        for v in self.psi_edge_weight:
            for neigh_v in self.psi_edge_weight[v]:
                self.reverse_psi_edge_weight[v][neigh_v] = 1 / self.psi_edge_weight[v][neigh_v]
                
        
        return self.reverse_psi_edge_weight
    
    # PSI 逆数の重みつきグラフを txt ファイルで出力
    def out_put_reverse_psi_graph(self, dataset_name):
        
        self.calc_reverse_psi()
        
        output_file = dataset_name + "_psi_reverse.txt"
        out_path = "../datasets/" + output_file
        
        f = open(out_path, 'w')
        
        for v in self.reverse_psi_edge_weight:
            for neigh_v in self.reverse_psi_edge_weight[v]:
                f.write(str(v) + " ")
                f.write(str(neigh_v) + " ")
                f.write(str(self.reverse_psi_edge_weight[v][neigh_v]))
                f.write('\n')
                
        f.close()
        
# ----------------------------------------------------------------------------
class RandomWalk:
    
    # pagerank 計算
    def pagerank(self, G, rwer_num, walk_length, d):
        
        node_list = list(G.nodes)
        node_visits = {node: 0 for node in G.nodes()}
        
        for _ in range(rwer_num):
            for v in node_visits:
                
                for _ in range(walk_length):
                    r_value = random.random()
                    
                    
                    if(r_value <= d):
                        neighbors = list(G.neighbors(v))
                        random_index = random.randrange(len(neighbors))
                        v = neighbors[random_index]
                        
                    else:
                        random_index = random.randrange(len(node_list))
                        v = node_list[random_index]
                    
                    node_visits[v] += 1    
                    
        # PageRankスコアを計算
        total_visits = sum(node_visits.values())
        pagerank = {node: (visits / total_visits) * d + (1 - d)/len(G) for node, visits in node_visits.items()}
        
        return pagerank

                    
# ----------------------------------------------------------------------------

class WeightRandomWalk:
    
    def weighted_random_walk(self, wG, start_node, walk_length):
        current_node = start_node
        walk = [current_node]
        for _ in range(walk_length - 1):
            neighbors = list(wG.neighbors(current_node))
            weights = [wG[current_node][neighbor]['weight'] for neighbor in neighbors]
            # 重みに基づいて次のノードを選択
            next_node = random.choices(neighbors, weights=weights)[0]
            walk.append(next_node)
            current_node = next_node
        return walk
    
# ----------------------------------------------------------------------------

# ----------------------------------------------------------------------------
class ComWalk:
    def __init__(self, G, c_id, id_c):
        self.G = G
        self.c_id = c_id
        self.id_c = id_c
        
    # コミュニティ単位の pagerank    
    def com_pagerank(self, rwer_num, walk_length, d, com_id):
        
        node_list = self.c_id[com_id]
        node_visits = {node: 0 for node in node_list}
        
        for _ in range(rwer_num):
            for v in node_visits:
                
                for _ in range(walk_length):
                    r_value = random.random()
                    
                    if(r_value <= d):
                        neighbors = list(self.G.neighbors(v))
                        random_index = random.randrange(len(neighbors))
                        v = neighbors[random_index]
                    else:
                        random_index = random.randrange(len(node_list))
                        v = node_list[random_index]
                        
                    if (self.id_c[v] != com_id):
                        continue
                    
                    node_visits[v] += 1    
                    
        # PageRankスコアを計算
        total_visits = sum(node_visits.values())
        pagerank = {node: (visits / total_visits) * d + (1 - d)/len(self.c_id[com_id]) for node, visits in node_visits.items()}
        
        return pagerank
    
    # 1 hop 先の ノードを返す
    def one_hop_rw(self, v):
        neighbors = list(self.G.neighbors(v))
        random_index = random.randrange(len(neighbors))
        v = neighbors[random_index]
        
        return v
                
    def stay_ratio(self, rwer_num, walklength, com_id):
        
        hop_stay_ratio_list = []
        node_list = self.c_id[com_id]   
        next_hop_dic = {node: [] for node in node_list}
        
        for v in next_hop_dic:
            for _ in range(rwer_num):
                next_hop_dic[v].append(v)
            
        stay_rwer_num = {node: rwer_num for node in node_list}
        initial_rwer_num = rwer_num * len(node_list)
        
        for _ in range(walklength):
            for node in next_hop_dic:
                new_node_list = []
                for v in next_hop_dic[node]:
                    
                    prev_v = v
                    stay_rwer_num[v] -= 1
                    
                    v = self.one_hop_rw(v)
                    
                    if(self.id_c[v] != com_id):
                        v = prev_v
                        continue
                    
                    stay_rwer_num[v] += 1
                    
                    new_node_list.append(v)
                    
                next_hop_dic[node] = new_node_list
                
            stay_walker_num = 0
            for id in stay_rwer_num:
                stay_walker_num += stay_rwer_num[id]
                
            stay_ratio = stay_walker_num / initial_rwer_num
            
            hop_stay_ratio_list.append(stay_ratio)
        
        return hop_stay_ratio_list                
                
        
# ----------------------------------------------------------------------------

class ComWalkWeighted:
    def __init__(self, wG, c_id, id_c):
        self.wG = wG
        self.c_id = c_id
        self.id_c = id_c
        
    # コミュニティ単位の pagerank    
    def com_pagerank_weighted(self, rwer_num, walk_length, d, com_id):
        
        node_list = self.c_id[com_id]
        node_visits = {node: 0 for node in node_list}
        
        for _ in range(rwer_num):
            for v in node_visits:
                
                for _ in range(walk_length):
                    r_value = random.random()
                    
                    if(r_value <= d):
                        neighbors = list(self.wG.neighbors(v))
                        weights = [self.wG[v][neighbor]['weight'] for neighbor in neighbors]
                        v = random.choices(neighbors, weights=weights)[0]
                        
                    else:
                        random_index = random.randrange(len(node_list))
                        v = node_list[random_index]
                        
                    if (self.id_c[v] != com_id):
                        continue
                    
                    node_visits[v] += 1    
                    
        # PageRankスコアを計算
        total_visits = sum(node_visits.values())
        pagerank = {node: (visits / total_visits) * d + (1 - d)/len(self.c_id[com_id]) for node, visits in node_visits.items()}
        
        return pagerank
    
    
    
    # 1 hop 先の ノードを返す
    def one_hop_rw(self, v):
        neighbors = list(self.wG.neighbors(v))
        weights = [self.wG[v][neighbor]['weight'] for neighbor in neighbors]
        v = random.choices(neighbors, weights=weights)[0]
        
        return v
    
    def stay_ratio_w(self, rwer_num, walklength, com_id):
        
        hop_stay_ratio_list = []
        node_list = self.c_id[com_id]   
        next_hop_dic = {node: [] for node in node_list}
        
        for v in next_hop_dic:
            for _ in range(rwer_num):
                next_hop_dic[v].append(v)
            
        stay_rwer_num = {node: rwer_num for node in node_list}
        initial_rwer_num = rwer_num * len(node_list)
        
        for _ in range(walklength):
            for node in next_hop_dic:
                new_node_list = []
                for v in next_hop_dic[node]:
                    
                    prev_v = v
                    stay_rwer_num[v] -= 1
                    
                    v = self.one_hop_rw(v)
                    
                    if(self.id_c[v] != com_id):
                        v = prev_v
                        continue
                    
                    stay_rwer_num[v] += 1
                    
                    new_node_list.append(v)
                    
                next_hop_dic[node] = new_node_list
                
            stay_walker_num = 0
            for id in stay_rwer_num:
                stay_walker_num += stay_rwer_num[id]
                
            stay_ratio = stay_walker_num / initial_rwer_num
            
            hop_stay_ratio_list.append(stay_ratio)
        
        return hop_stay_ratio_list    
            
# ----------------------------------------------------------------------------


                    
                    
    


                    
                    
    

