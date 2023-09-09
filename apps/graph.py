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
        self.boundary_edge_hash_list = []

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
    
    # 境界エッジをハッシュ値にしてリストで取得
    def get_boundary_edge_hash(self):
        boundary_edge_hash_set = set()
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
                        boundary_edge = (self.c_id[c_num][i], neigh)
                        boundary_edge_hash = hash(tuple(sorted(boundary_edge)))
                        boundary_edge_hash_set.add(boundary_edge_hash)
        
        self.boundary_edge_hash_list = list(boundary_edge_hash_set)
                        
        
        return self.boundary_edge_hash_list



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
    def random_walk_betweenness_centrality(self, G, num_walks=10, walk_length=3000):
        
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
    
    
    # RW で通ったエッジ回数を記録
    def get_edge_through_cnt(self, G, num_walks=2000, walk_length=100):
        
        unique_represemtation_dict = {hash(tuple(sorted(e))) : 0 for e in G.edges}
        
        for _ in range(num_walks):
            start_node = random.choice(list(G.nodes()))
            
            for _ in range(num_walks):
                neighbors = list(G.neighbors(start_node))
                if not neighbors:
                    break
                next_node = random.choice(neighbors)
                
                through_e = (start_node, next_node)
                unique_represemtation_dict[hash(tuple(sorted(through_e)))] += 1
                
        return unique_represemtation_dict
    

# コミュニティ情報を用いたランダムウォーク
class CommunityRandomWalk:
     def __init__(self, G, c_id, id_c):
        self.G = G
        self.c_id = c_id
        self.id_c = id_c
        self.rwer_info = []
        self.last_community = {k : 0 for k in range(len(c_id))}
        self.pass_time = {}
        self.average_distance = {}
        self.original_average_distance = {}
        self.rw_path = []
        self.rw_pr_result = {}
        
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
     
     
     # 全頂点からRWし、最終的にRWer が どこに止まったかをチェック
     def get_last_node_belong_community(self, walk_num):
         rwer_info = self.get_last_node_RW_n(walk_num)
         for k in range(len(rwer_info)):
            if rwer_info[k][2] in self.last_community:
                self.last_community[rwer_info[k][2]] += 1
             
         return self.last_community
     
     # ある頂点 i からの各頂点への平均距離
     def average_distance_RW(self, step_num, jump_raito, v):
         
         starting_v = v
         distance_sum = {}
         cnt_step = 0
         pass_time_2 = {}
         rw_one_path = []
         rw_one_path.append(v)
         
         for _ in range(step_num):
             
             r_value = random.random()
             rw_pass_node = set()
             
             # 隣接頂点へ移動
             if (r_value <= jump_raito):
                neighbors = list(self.G.neighbors(v))
                random_index = random.randrange(len(neighbors))
                v = neighbors[random_index]
                cnt_step += 1
                rw_pass_node.add(v)
                rw_one_path.append(v)
                
                if v in distance_sum:
                    if v in rw_pass_node:
                        self.pass_time[v] += 1
                        
                else:
                    self.pass_time[v] = 1
                    pass_time_2[v] = 1
                    distance_sum[v] = cnt_step
            
             # 一定確率で始点に戻る
             else:
                 v = starting_v
                 cnt_step = 0
                 self.rw_path.append(rw_one_path)
                 rw_one_path = []
                 
        
         for key in self.pass_time.keys():
             self.original_average_distance[key] = distance_sum[key] / self.pass_time[key]
             self.average_distance[key] = distance_sum[key] / pass_time_2[key] 
              
            
        
         return self.average_distance
     
     def get_oritinal_average_distance(self):
         return self.original_average_distance
    
     # ある頂点 i から開始したRWが各頂点を通過した回数   
     def get_pass_time(self):
         
         return self.pass_time
     
     # RW の経路を取得
     def get_rw_path(self):
         
         return self.rw_path
     
     def rw_pr(self, jump_ratio=0.85):
         
         rw_path = self.get_rw_path()
         #pass_time = self.get_pass_time()
         original_average_distance = self.get_oritinal_average_distance()
         
         for _ in range(100000):
             random_index = random.randint(0, len(rw_path) - 1)
             
             if len(rw_path[random_index]) < 1:
                 continue
             
             v_index = random.randint(0, len(rw_path[random_index]) - 1)
             
             r_value = random.random()
             
             if(r_value <= jump_ratio):
                 v_index += 1
                 
                 if(v_index >= len(rw_path[random_index])):
                     continue 
                 
                 
                 if rw_path[random_index][v_index] in self.rw_pr_result:
                     if(original_average_distance[rw_path[random_index][v_index]] > 5):
                         self.rw_pr_result[rw_path[random_index][v_index]] = 0
                         
                     self.rw_pr_result[rw_path[random_index][v_index]] += 1
                 else:
                     if(original_average_distance[rw_path[random_index][v_index]] > 5):
                         self.rw_pr_result[rw_path[random_index][v_index]] = 0
                         
                     self.rw_pr_result[rw_path[random_index][v_index]] = 1
                 
                 
         
         return self.rw_pr_result
                    
     
            
           
