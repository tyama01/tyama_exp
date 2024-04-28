import networkx as nx 
import random

# データセット読み込みのクラス
class DataLoader:
    def __init__(self, dataset_name, is_directed):
        self.dataset_name = dataset_name
        self.is_directed = is_directed
        self.c_id = {}
        self.id_c = {}
        
        # 有向グラフ
        if is_directed:
            self.G = nx.DiGraph()
            dataset_path = "../datasets/" + self.dataset_name + ".txt"
            self.G = nx.read_edgelist(dataset_path, nodetype=int, create_using=nx.DiGraph)
            
            
        # 無向グラフ    
        else:
            self.G = nx.Graph()
            dataset_path = "../datasets/" + self.dataset_name + ".txt"
            self.G = nx.read_edgelist(dataset_path, nodetype=int)
            
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

# PPR 演算    
class PPR:
    def __init__(self, G):
        self.G = G    
    
    def get_paths(self, source_node, count, alpha):
        paths = list()
        node_list = list(self.G.nodes)
        
        for _ in range(count):
            current_node = source_node
            path = [source_node]
            while True:
                if random.random() < alpha:
                    break
                neighbors = list(self.G.neighbors(current_node))
                
                if(len(neighbors) == 0): # 有向エッジがない場合はランダムジャンプ
                    random_index = random.randrange(len(node_list))
                    current_node = node_list[random_index]
                    path.append(current_node)
                    
                else:   
                    random_index = random.randrange(len(neighbors))
                    current_node = neighbors[random_index]
                    path.append(current_node)
            paths.append(path)
            
        return paths

    
    def get_visited_ratio(self, paths):
        visited_count = dict()
        for path in paths:
            for node_id in path:
                visited_count[node_id] = visited_count.get(node_id, 0) + 1
        total_step = sum(visited_count.values())
        visited_ratio = dict()
        for node_id, count in visited_count.items():
            visited_ratio[node_id] = count / total_step
        return visited_ratio
    
    def calc_ppr_by_random_walk(self, source_id, count, alpha):
        paths = self.get_paths(source_id, count, alpha)
        return self.get_visited_ratio(paths)
    
# ランダム遷移が 最短距離に依存した PPR
class LevyPPR:
    def __init__(self, G):
        self.G = G
        
    def get_r_hop_neighbors(self, source_node, r):
        
        # {source ノードからの最短距離 : [そこに存在するノード達]}
        r_hop_neighbors_dic = {path_length : [] for path_length in range(1, r+1)}
        
        for path_length in range(1, r+1):
            
            r_length_nodes = nx.descendants_at_distance(self.G, source=source_node, distance=path_length)
            
            for node in r_length_nodes:
                r_hop_neighbors_dic[path_length].append(node)
                
        
        return r_hop_neighbors_dic
        
     
    def get_paths(self, source_node, count, alpha, r):
        
        r_hop_neghbors_dic = self.get_r_hop_neighbors(source_node, r)
        
        # 最短距離
        shortest_path_length_list = [path_length for path_length in r_hop_neghbors_dic]
        
        # 最短距離に応じた重み
        w_list = [1/w for w in r_hop_neghbors_dic]
        
        paths = list()
        
        for _ in range(count):
            current_node = source_node
            path = [source_node]
            while True:
                if random.random() < alpha:
                    break
                neighbors = list(self.G.neighbors(current_node))
                
            
                if(len(neighbors) == 0): # 有向エッジがない場合は最短距離に応じて遷移
                    select_path_length = random.choices(shortest_path_length_list, weights=w_list)[0]
                    random_index = random.randrange(len(r_hop_neghbors_dic[select_path_length]))
                    current_node = r_hop_neghbors_dic[select_path_length][random_index]
                    path.append(current_node)
                    
                else:
                    select_path_length = random.choices(shortest_path_length_list, weights=w_list)[0]
                    random_index = random.randrange(len(r_hop_neghbors_dic[select_path_length]))
                    current_node = r_hop_neghbors_dic[select_path_length][random_index]
                    path.append(current_node)
        
            paths.append(path)
        
    
        return paths
                
    def get_visited_ratio(self, paths):
        visited_count = dict()
        for path in paths:
            for node_id in path:
                visited_count[node_id] = visited_count.get(node_id, 0) + 1
        total_step = sum(visited_count.values())
        visited_ratio = dict()
        for node_id, count in visited_count.items():
            visited_ratio[node_id] = count / total_step
        return visited_ratio
    
    def calc_levy_ppr_by_random_walk(self, source_id, count, alpha, r):
        paths = self.get_paths(source_id, count, alpha, r)
        return self.get_visited_ratio(paths)
    
    
            
        
    

# シードノードを取得するためのクラス
class GetSeed:
    
    # Spread Hub 2 hop 以上離れた高次数ノードを取得 kはシードノードの数
    def spread_hub(self, G, k):
        
        S = []
        
        # ノード集合
        unmarked = set(G.nodes())
        
        # 次数の降順の dic {頂点ID : 次数}
        deg_rank = sorted(G.degree(), key=lambda x: x[1], reverse=True)
        
        for (candidate, deg) in deg_rank: # 次数の大きい順に候補を見ていく
            
            if candidate not in unmarked: 
                continue # candidateに既に印がついていたら飛ばす
            
            S.append(candidate) # seed集合にcandidateを追加
            unmarked.remove(candidate) # candidateをマーク
            unmarked = unmarked.difference(set(G.neighbors(candidate))) # candidateの近傍にも印
            
            if len(S) >= k: break # seed集合の数がk個以上になったら終了
            
        return S
        

# 自ノードのPPR 演算    
class SelfPPR:
    def __init__(self, G):
        self.G = G    
    
    def get_paths(self, source_node, count, alpha):
        paths = list()
        node_list = list(self.G.nodes)
        
        for _ in range(count):
            current_node = source_node
            path = []
            while True:
                if random.random() < alpha:
                    break
                neighbors = list(self.G.neighbors(current_node))
                
                if(len(neighbors) == 0): # 有向エッジがない場合はランダムジャンプ
                    random_index = random.randrange(len(node_list))
                    current_node = node_list[random_index]
                    path.append(current_node)
                    
                else:   
                    random_index = random.randrange(len(neighbors))
                    current_node = neighbors[random_index]
                    path.append(current_node)
            paths.append(path)
            
        return paths

    
    def get_visited_ratio(self, paths):
        visited_count = dict()
        for path in paths:
            for node_id in path:
                visited_count[node_id] = visited_count.get(node_id, 0) + 1
        total_step = sum(visited_count.values())
        visited_ratio = dict()
        for node_id, count in visited_count.items():
            visited_ratio[node_id] = count / total_step
        return visited_ratio
    
    def calc_self_ppr_by_random_walk(self, source_id, count, alpha):
        paths = self.get_paths(source_id, count, alpha)
        visited_ratio = self.get_visited_ratio(paths)
        
        if source_id in visited_ratio:
            return visited_ratio[source_id]
        
        else:
            return 0
    
class flow_PR:
    def __init__(self, G):
        self.G = G
    
    # ノードごとに持っている RWer 数が違うようにする
    # self_ppr_dic {Node id : self ppr}    
    def get_rwer_num(self, self_ppr_dic, w):
        
        standard_rwer_num = 1000
        
        # 自己ppr に基づいて　Rwer量を決める
        # {Node id : rwer_num}
        rwer_num_dic = {}
        
        for node in self_ppr_dic:
            rwer_num_dic[node] = int(standard_rwer_num ** ((1 + self_ppr_dic[node])**w))
            
        return rwer_num_dic
        
    
    def get_paths(self, source_node, count, alpha):
        
        paths = list()
        node_list = list(self.G.nodes)
        
        for _ in range(count):
            current_node = source_node
            path = [source_node]
            while True:
                if random.random() < alpha:
                    break
                neighbors = list(self.G.neighbors(current_node))
                
                if(len(neighbors) == 0): # 有向エッジがない場合はランダムジャンプ
                    random_index = random.randrange(len(node_list))
                    current_node = node_list[random_index]
                    path.append(current_node)
                    
                else:   
                    random_index = random.randrange(len(neighbors))
                    current_node = neighbors[random_index]
                    path.append(current_node)
            paths.append(path)
            
        return paths
    
    def calc_flow_rw_pr(self, self_ppr_dic, alpha, w):
        rwer_num_dic = self.get_rwer_num(self_ppr_dic, w)
        
        flow_rw_visited_count = {node : 0  for node in self_ppr_dic}
        
        for node in self_ppr_dic:
            
            paths = self.get_paths(source_node=node, count=rwer_num_dic[node], alpha=alpha)
            
            for path in paths:
                for id in path:
                    flow_rw_visited_count[id] += 1
                    
        
        sum_of_visited_time = 0
        for id in flow_rw_visited_count:
            sum_of_visited_time += flow_rw_visited_count[id]
            
        for id in flow_rw_visited_count:
            flow_rw_visited_count[id] /= sum_of_visited_time
            
        
        return flow_rw_visited_count
            
        
        
        