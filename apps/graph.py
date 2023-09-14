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
    
class RandomWalkers:
    def __init__(self, G):
        self.G = G
        self.group_nodes_set = set() # ノードグループ (ここから RWer がどれだけ抜け出すかをみる)
        self.next_hop_group_nodes_set = set() # 1 hop 先のノード集合
        self.walkers_num_per_node = {} # 各ノードが RWer をどれだけ持っているか
        
        # こことは別に初期化が必要な場合があることに注意 (ノード集合が変わるとき)
        self.walker_path_time = {} # 1 回の RW で通ったRWer がそのノード通った回数
        self.remaining_pr = {} # 残存 PR 的なやつ ： 通過回数 / (RWer * hop 数 ) 
        self.next_hop_remaining_pr = {}
    
    """ 
    # Random Walker を動かし続け、最終的に到達したノードを返す    
    def move_a_walker(self, v, walk_num):
        for _ in range(walk_num):
            
            neighbors = list(self.G.neighbors(v))
            random_index = random.randrange(len(neighbors))
            v = neighbors[random_index]
            
            if v in self.walker_path_time:
                self.walker_path_time[v] += 1
            
            else:
                self.walker_path_time[v] = 1
            
        return v 
    """
    
    # RWer のノードの通過回数
    def get_walker_path_time(self):
        
        return self.walker_path_time
    
    """
    def move_walkers_from_n_hop(self, v, walk_num, walkers_num, hop):
        
        self.group_nodes_set.add(v)
        group_nodes_list_sub = []
        group_nodes_list_sub.append(v)
        
        
        # ある始点頂点から n hop までをグループと見る -> ノードグループを生成
        for _ in range(hop):
            for v_1 in group_nodes_list_sub:
                neighbors = list(self.G.neighbors(v_1))
                group_nodes_list_sub = neighbors
                
                for v_2 in neighbors:
                    self.group_nodes_set.add(v_2)
        
        # 初期化 グループ毎に最初は同じ数の RWer 数をもつ walkers_num = 20 くらいにする予定
        self.walkers_num_per_node = {group_v : walkers_num for group_v in self.group_nodes_set}
        
        # 1 イテレーションごとにそのグループが保持している RWer 数
        group_rwers_num_per_interation = []
        
        initial_rwers_num = walkers_num * len(self.walkers_num_per_node)
        group_rwers_num_per_interation.append(1)
        
        
        # グループ内の各ノードから RWer を走らせ, どのノードに留まったか
        
        for _ in range(walkers_num): # このイテレーション毎の Walker の流出を記録
            
            for v_in_group in self.group_nodes_set:
                
                stay_v = self.move_a_walker(v_in_group, walk_num)
                
                # RWer 出走
                self.walkers_num_per_node[v_in_group] -= 1
                
                if stay_v in self.group_nodes_set :
                    self.walkers_num_per_node[stay_v] += 1
            
            # グループ内にどれだけ RWer が残ったかを記録    
            group_walkers_num = 0
            
            for v_in_group in self.group_nodes_set:
                group_walkers_num += self.walkers_num_per_node[v_in_group]
            
            group_rwers_num_per_interation.append(group_walkers_num / initial_rwers_num)
        
        
        return group_rwers_num_per_interation
"""

    # グループノード取得
    def get_group_nodes(self):
        
        return self.group_nodes_set
    
    # ある集合の 1hop 先のノード集合を取得
    def get_next_hop_group_nodes(self):
        
        for v in self.group_nodes_set:
            neighbors = list(self.G.neighbors(v))
            
            for n_v in neighbors:
                if n_v not in self.group_nodes_set:
                    self.next_hop_group_nodes_set.add(n_v)
                    
        
        return self.next_hop_group_nodes_set
                    
        
         
    
    # グループノード内のノード毎の最終的な RWer 保持数
    def get_walkers_per_node(self):
        
        return self.walkers_num_per_node 
    
    # walker が通ったノード set と 最後に stay した ノードを取得
    def move_a_walker_get_pass_node_set(self, v, walk_num):
        
         # ---- walker が通ったノード set と 最後に stay した ノードを取得 ----
        walker_pass_node_set = set()
        walker_pass_node_set.add(v)
        
        for _ in range(walk_num):
            
            neighbors = list(self.G.neighbors(v))
            random_index = random.randrange(len(neighbors))
            v = neighbors[random_index]
            walker_pass_node_set.add(v)
        
        # -----------------------------------------------------------
        
            # ノードの通過回数を記録
            
            if v in self.walker_path_time:
                self.walker_path_time[v] += 1
            
            else:
                self.walker_path_time[v] = 1
            
        # -----------------------------------------------------------
    
        return walker_pass_node_set, v
    
    def move_walkers_from_n_hop_exclude_come_back(self, v, walk_num, walkers_num, hop):
        
        self.group_nodes_set.add(v)
        group_nodes_list_sub = []
        group_nodes_list_sub.append(v)
        
        
        # ある始点頂点から n hop までをグループと見る -> ノードグループを生成
        for _ in range(hop):
            for v_1 in group_nodes_list_sub:
                neighbors = list(self.G.neighbors(v_1))
                group_nodes_list_sub = neighbors
                
                for v_2 in neighbors:
                    self.group_nodes_set.add(v_2)
        
        # 初期化 グループ毎に最初は同じ数の RWer 数をもつ walkers_num = 20 くらいにする予定
        self.walkers_num_per_node = {group_v : walkers_num for group_v in self.group_nodes_set}
        
        # 1 イテレーションごとにそのグループが保持している RWer 数
        group_rwers_num_per_interation = []
        
        initial_rwers_num = walkers_num * len(self.walkers_num_per_node)
        group_rwers_num_per_interation.append(1)
        
        
        # グループ内の各ノードから RWer を走らせ, どのノードに留まったか
        
        for _ in range(walkers_num): # このイテレーション毎の Walker の流出を記録
            
            for v_in_group in self.group_nodes_set:
                
                pass_node_set, stay_v = self.move_a_walker_get_pass_node_set(v_in_group, walk_num)
                
                # RWer 出走
                self.walkers_num_per_node[v_in_group] -= 1
                
                
                if pass_node_set <= self.group_nodes_set:
                    self.walkers_num_per_node[stay_v] += 1
            
            # グループ内にどれだけ RWer が残ったかを記録    
            group_walkers_num = 0
            
            for v_in_group in self.group_nodes_set:
                group_walkers_num += self.walkers_num_per_node[v_in_group]
            
            group_rwers_num_per_interation.append(group_walkers_num / initial_rwers_num)
            
            
        # 残留 PR を計算
        for v_in_group in self.group_nodes_set:
            if v_in_group in self.walker_path_time:
                
                self.remaining_pr[v_in_group] = self.walker_path_time[v_in_group] / (walkers_num * walk_num * len(self.group_nodes_set))
                
        
        # one_hop 先の　残留 PR 値
        self.get_next_hop_group_nodes()
        for v_in_next_group in  self.next_hop_group_nodes_set:
            if v_in_next_group in self.walker_path_time:
                
                self.next_hop_remaining_pr[v_in_next_group] = self.walker_path_time[v_in_next_group] / (walkers_num * walk_num * len(self.group_nodes_set))
        
        return group_rwers_num_per_interation
    
    # 残存 PR 取得 {ノード id : 残存 PR 値}
    def get_remaining_pr(self):
        
        return self.remaining_pr
    
    def get_next_hop_remaining_pr(self):
        
        return self.next_hop_remaining_pr           
        

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
    
    # ひたすら隣接頂点にランダムに遷移, どのノードを何回通ったかを記録　
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
                    
     
            
           
