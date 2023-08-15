import networkx as nx
import random
import matplotlib.colors

# データセット読み込みのクラス
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

# コミュニティ単位で分析するためのクラス    
class CommunityGraph:
    def __init__(self, G, c_id, id_c):
        self.G = G
        self.c_id = c_id
        self.id_c = id_c
        self.c_edge = {}
        self.c_G = nx.Graph()
        self.community_size = {}
        self.bridge_node_list = []

    # コミュニティ単位でのクラス
    def generate_community_graph(self):
        for c_num in range(len(self.c_id)):
            c_num_size = len(self.c_id[c_num])
            for i in range(c_num_size):
                
                # 全頂点を1ホップ進める
                neighbors = list(self.G.neighbors(self.c_id[c_num][i]))
                
                # 頂点 i の隣接頂点を１つずつ調べる             
                for neigh in neighbors: 
                    
                    # 隣接頂点が同じコミュニティなら for ループを抜ける
                    if self.id_c[neigh] == c_num:
                        continue

                    # コミュニティ間のエッジ関係を把握    
                    key = (c_num, self.id_c[neigh])
                    if key in self.c_edge:
                        self.c_edge[key] += 1
                    else:
                        self.c_edge[key] = 1

        c_edge_key = list(self.c_edge.keys())

        for e in c_edge_key:
            self.c_G.add_edge(e[0], e[1])

        return self.c_G
    
    # コミュニティ内に含まれる頂点数を取得
    def get_community_size(self):
        for c_num in range(len(self.c_id)):
            self.community_size[c_num] = len(self.c_id[c_num])
            
        return self.community_size
    
    # 境界ノードをリストで取得
    def get_bridge_node(self):
        bridge_node_set = set()
        for c_num in range(len(self.c_id)):
            c_num_size = len(self.c_id[c_num])
            for i in range(c_num_size):
                
                # 全頂点を1ホップ進める
                neighbors = list(self.G.neighbors(self.c_id[c_num][i]))
                
                # 頂点 i の隣接頂点を１つずつ調べる             
                for neigh in neighbors: 
                    
                    # 隣接頂点が同じコミュニティなら for ループを抜ける
                    if self.id_c[neigh] == c_num:
                        continue
                    else:
                        bridge_node_set.add(self.c_id[c_num][i])
        
        self.bridge_node_list = list(bridge_node_set)
                        
        
        return self.bridge_node_list


# ランダムウォークのクラス
class RandomWalk:
    
    # ひたすら隣接頂点にランダムに遷移
    def simple_random_walk(self, G, v, walk_num, v_walk_num_cnt):
        for _ in range(walk_num + 1):
            if v in v_walk_num_cnt:
                v_walk_num_cnt[v] += 1
            else:
                v_walk_num_cnt[v] = 1

            neighbors = list(G.neighbors(v))
            random_index = random.randrange(len(neighbors))
            v = neighbors[random_index]

        return v_walk_num_cnt
    
    
    # 確率 d で　隣接頂点にランダムに遷移、　確率 1 - d でランダムな頂点に遷移
    def pr_random_walk(self, G, v, walk_num, v_walk_num_cnt, d):
        node_list = list(G.nodes)

        for _ in range(walk_num + 1):
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
    
    
    # 媒介中心性ベースの RW
    def random_walk_betweenness_centrality(self, G, num_walks=10000, walk_length=1000):
        
        betweenness_centrality = {node: 0.0 for node in list(G.nodes())}

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

# コミュニティ情報を用いたランダムウォーク
class CommunityRandomWalk:
     def __init__(self, G, id_c):
        self.G = G
        self.id_c = id_c
        self.rwer_info = []
        
     def get_last_node_RW(self, v, walk_num):
         
        c_id_of_v = self.id_c[v]
         
        for _ in range(walk_num + 1):
            neighbors = list(self.G.neighbors(v))
            random_index = random.randrange(len(neighbors))
            v = neighbors[random_index]
        
        c_id_of_last_v = self.id_c[v]
            
        # (RWerが最後に到達した頂点, RWerが最初にいたコミュニティ, RWerが最後にいたコミュニティ)
        return (v, c_id_of_v, c_id_of_last_v)
    
     def get_last_node_RW_n(self, walk_num):
         
         # 全グラフのノードリスト
         node_list = list(self.G.nodes())
        
         for v in node_list:
             self.rwer_info.append(self.get_last_node_RW(v, walk_num))
            
         return self.rwer_info
             

# 色取得(プロット用)    
class ColorUtil:
    def choose_colors(self, num_colors):
        tmp = list(matplotlib.colors.CSS4_COLORS.values())
        #random.shuffle(tmp)
        label2color = tmp[:num_colors]
        return label2color
