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
        