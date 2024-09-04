import networkx as nx 
import random
from queue import Queue
import numpy as np
import itertools
import math
from collections import deque



#------------------------------------------------------------------

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
            
        self.node_list = list(self.G.nodes())
        self.edge_list = list(self.G.edges())
            
    def get_graph(self):
        return self.G
    
    def load_community(self):
        community_path = "../datasets/" + self.dataset_name + "_louvain.txt"
        with open(community_path, 'r') as f:
            lines = f.readlines()
        for line in lines:
            data = line.split()
            self.c_id.setdefault(int(data[0]), []).append(int(data[1]))
            self.id_c[int(data[1])] = int(data[0])
            
    def get_communities(self):
        return self.c_id, self.id_c
    
    def get_adj_matrix(self, is_directed):
        n = len(self.node_list)
        A = np.zeros((n, n))
        
        if(is_directed):
            for edge in self.edge_list:
                A[edge[0]][edge[1]] = 1
                
        else:
            for edge in self.edge_list:
                A[edge[0]][edge[1]] = 1
                A[edge[1]][edge[0]] = 1
                
        return A
    
    # コミュニティ境界ノードを取得
    def get_bound_node(self):
        
        # {所属コミュニティ：境界ノード}
        com_bound_node_dic = {com_id : [] for com_id in self.c_id}
        
        for com_id in self.c_id:
            for v in self.c_id[com_id]:
                v_neighbors_list = list(self.G.neighbors(v))
                
                for adj_node in v_neighbors_list:
                    if(com_id != self.id_c[adj_node]):
                        com_bound_node_dic[com_id].append(v)
                        
        
        return com_bound_node_dic 
    
    # ノード情報取得 (次数(コミュニティ内/外), 所属コミュニティ)
    def get_node_info(self, v):
        
        # 次数
        v_deg = self.G.degree(v)
        
        # 所属コミュニティ
        v_belong_com = self.id_c[v]
        
        # どれだけ他のコミュニティノードと繋がっているか
        com_bound_deg_dic = {com_id : 0 for com_id in self.c_id}
        
        v_neighbors_list = list(self.G.neighbors(v))
        for adj_node in v_neighbors_list:
            com_bound_deg_dic[self.id_c[adj_node]] += 1
            
            
        return v_deg, v_belong_com, com_bound_deg_dic
    
        
          


#------------------------------------------------------------------



#------------------------------------------------------------------
# 還流度によるエッジ RW 流量比を計算
class FLOW:
    def __init__(self, G):
        self.G = G 
    
    # PPR した際の経路
    def get_paths(self, source_node, count, alpha):
        paths = list()
        #node_list = list(self.G.nodes)         
            
        for _ in range(count):
            current_node = source_node
            path = [source_node]
            while True:
                if random.random() < alpha:
                    break
                neighbors = list(self.G.neighbors(current_node))
                
                if(len(neighbors) == 0): # 有向エッジがない場合はランダムジャンプ
                    current_node = source_node
                    break
                else:   
                    random_index = random.randrange(len(neighbors))
                    current_node = neighbors[random_index]
                    path.append(current_node)
            paths.append(path)
            
        return paths
    
    
            
        
    def get_flow_times(self, src_node, count, alpha):
        
        # ソースノードの隣接ノード
        adj_node_list = list(self.G.neighbors(src_node))
        
        # 隣接ノード -> ソースノードに流入した回数を記録
        flow_times = {(adj_node, src_node) : 0 for adj_node in adj_node_list}
        
        paths = self.get_paths(src_node, count, alpha)
        
        for path in paths:
            for hop_num in range(len(path)):
                if (hop_num > 1 and path[hop_num] == src_node):
                    flow_times[(path[hop_num - 1], src_node)] += 1
                    
        return flow_times
                
        
#------------------------------------------------------------------

#------------------------------------------------------------------

# エッジ還流度 演算

class EPPR:
    def __init__(self, G):
        self.G = G
        self.edge_list = list(self.G.edges())        
    
    # エッジ還流度を計算    
    def calc_edge_selfppr(self, node_selfppr):
        
        edge_selfppr = {}
        
        for edge in self.edge_list:
            
            edge_selfppr_val = 0
            
            for id in edge:
                
                neighbors_list = list(self.G.neighbors(id))
                neighbors_num = len(neighbors_list)

                
                # ノード の還流度 / そのノードの出次数
                edge_selfppr_val += node_selfppr[id] / neighbors_num
            
           
            edge_selfppr[edge] = edge_selfppr_val
            
            
        return edge_selfppr
    
    def calc_flow_edge_selfppr(self, node_selfppr, flow):
        
        edge_selfppr = {}
        
        for edge in self.edge_list:
            
            edge_selfppr_val = 0
            
                
            
            # edge (0)
            
            total_flow_val_0 = sum(flow[edge[0]].values())
            flow_ratio_0 = flow[edge[0]][(edge[1], edge[0])] / total_flow_val_0
            edge_selfppr_val += node_selfppr[edge[0]] * flow_ratio_0
            
            # edge (1)
            
            total_flow_val_1 = sum(flow[edge[1]].values())
            flow_ratio_1 = flow[edge[1]][(edge[0], edge[1])] / total_flow_val_1
            edge_selfppr_val += node_selfppr[edge[1]] * flow_ratio_1
                
            
            
           
            edge_selfppr[edge] = edge_selfppr_val
            
            
        return edge_selfppr
      
#------------------------------------------------------------------

#------------------------------------------------------------------
# 幅優先探索 BFS
class BFS:
    def __init__(self, G):
        self.G = G
        self.node_list = list(self.G.nodes)
        
    def calc_simple_bfs(self, src_node):
        
        # BFS のためのデータ構造
        dist_dict = {node : -1 for node in self.node_list} # 全ノードを「未訪問」に初期化
        que = Queue()
        
        # 初期化条件 (ソースノードを初期ノードとする)
        dist_dict[src_node] = 0
        que.put(src_node)
        
        # BFS 開始 (キューがからになるまで探索を行う)
        while not que.empty():
            node = que.get() # キューから先頭ノードを取り出す
            
            # node から辿れるノードを全て辿る
            adj_list = list(self.G.neighbors(node))
            if(len(adj_list) != 0):
                for adj_node in adj_list:
                    if (dist_dict[adj_node] != -1):
                        continue # 既に発見済みのノードは探索しない
                    
                    # 新たに発見した頂点について距離情報を更新してキューに追加
                    dist_dict[adj_node] = dist_dict[node] + 1
                    que.put(adj_node)
                    
        return dist_dict
    
    # 山下り でコミュニティ分割
    # 計算量に関しては改善の余地あり (現状は全探索している。部分的に探索すればもっと早くなりそう)
    def get_com_by_bfs(self, node_selfppr, edge_selfppr, a_ratio):
        
        # エッジ還流度が大きい順にエッジをソート
        edge_sort_list = []
        for tmp in sorted(edge_selfppr.items(), key=lambda x:x[1], reverse=True):
            edge_sort_list.append(tmp[0])
            
        # エッジ還流度が最も大きいエッジを取得
        # そのエッジの内ノード還流度か高い方のノードを始点ノードとしてBFS
        
        max_edge = edge_sort_list[2] # エッジ還流度が最大のエッジ
        
        #print(f"max edge : {max_edge}")
        
        #a_val = edge_selfppr[max_edge] * a_ratio  #増加幅の許容範囲
        
        if(node_selfppr[max_edge[0]] > node_selfppr[max_edge[1]]): # ノード還流度が大きい方が始点
            src_node = max_edge[0]
        else:
            src_node = max_edge[1]
            
        print(f"src_node : {src_node}")
            
        # BFS を実行 {ノードID : 距離k層}
        dist_dic = self.calc_simple_bfs(src_node)
        #print(dist_dic)
        
        # 最大距離
        max_dist = max(dist_dic.values())
        
        
        # {距離k層 : [ノードリスト]}
        key_dist_dic = {dist : [node for node, k in dist_dic.items() if k == dist] for dist in range(max_dist + 1)}
        #print(key_dist_dic)
        
        # 距離k層以内のノードリスト
        # 距離1層までのノードを先に入れとく
        k_dist_node_list = [src_node]
        for node in key_dist_dic[1]:
            k_dist_node_list.append(node)
        
        
        # {距離層 k : [エッジ]}
        H_k_edge_diff_dic = {k : [] for k in range(1, max_dist+1)}
        
        # k距離1層までのエッジを先に入れとく
        H_1 = self.G.subgraph(k_dist_node_list)
        H_1_edge_list = list(H_1.edges())
        
        for edge in H_1_edge_list:
            H_k_edge_diff_dic[1].append(edge)
        
        
        # 元グラフの情報を保持しておきたい
        G_copy = self.G.copy()
            
        for k in range(1, max_dist):
            
            # 距離k+1層のノードリスト
            k_plus_one_dist_node_list = []
            for node in k_dist_node_list:
                k_plus_one_dist_node_list.append(node)
            for node in key_dist_dic[k+1]:
                k_plus_one_dist_node_list.append(node)
                
            # print(f"{k}_node_list : {k_dist_node_list}")
            # print(f"{k+1}_plut_one_node_list : {k_plus_one_dist_node_list}")
                
            
            # 部分グラフ生成
            H_k = G_copy.subgraph(k_dist_node_list)
            H_k_1 = G_copy.subgraph(k_plus_one_dist_node_list)
            
            # 部分グラフのエッジを取得
            H_k_edge_list = list(H_k.edges())
            #print(H_k_edge_list)
            print(f"H_k_edge_num : {len(H_k_edge_list)}")
            print("---------------------")
            
            H_k_1_edge_list = list(H_k_1.edges())
            #print(H_k_1_edge_list)
            print(f"H_k_1_edge_num : {len(H_k_1_edge_list)}")
            print("---------------------")
    
            dist_k_1_edge_list = []
            
            for k_1_edge in H_k_1_edge_list:
                if(((k_1_edge[0], k_1_edge[1]) not in H_k_edge_list)):
                   if ((k_1_edge[1], k_1_edge[0]) not in H_k_edge_list):
                        dist_k_1_edge_list.append(k_1_edge)
            
            print(f"差 : {len(dist_k_1_edge_list)}")
            print("---------------------")
            
            for edge in dist_k_1_edge_list:
                H_k_edge_diff_dic[k+1].append(edge)
            
            
                    
          
            
            # エッジ還流度が減少から増加に変わるタイミングのエッジを削除していく
            for edge_k in H_k_edge_diff_dic[k]:
                
                # 無向グラフでの例外処理
                try: # キーがエッジだが、(3, 0) がキーにある場合(0, 3) がないので両方対応するため
                    edge_k_selfppr = edge_selfppr[edge_k]
                except KeyError:
                    edge_k = (edge_k[1], edge_k[0])
                    edge_k_selfppr = edge_selfppr[edge_k]
                
                a_val = edge_selfppr[edge_k] * a_ratio  #増加幅の許容範囲
                
                for edge_k_1 in dist_k_1_edge_list:
                    
                    
                    
                    # # 無向グラフでの例外処理
                    # try: # キーがエッジだが、(3, 0) がキーにある場合(0, 3) がないので両方対応するため
                    #     edge_k_selfppr = edge_selfppr[edge_k]
                    # except KeyError:
                    #     edge_k = (edge_k[1], edge_k[0])
                    #     edge_k_selfppr = edge_selfppr[edge_k]
                        
                    
                        
                    try:
                        edge_k_1_selfppr = edge_selfppr[edge_k_1]
                    except KeyError:
                        edge_k_1 = (edge_k_1[1], edge_k_1[0])
                        edge_k_1_selfppr = edge_selfppr[edge_k_1]
                    
                    if(edge_k_1_selfppr > (edge_k_selfppr + a_val)):
                        
                        print("------------------------")
                        print(f"{edge_k} : {edge_k_selfppr + a_val}")
                        print(f"{edge_k_1} : {edge_k_1_selfppr}")
                        print("------------------------")
                        
                        
                        
                        #print(f"cut edge : {edge_k}")
                        G_copy.remove_edges_from([edge_k])
                        
                        
                        Gcc = sorted(nx.connected_components(G_copy), key=len, reverse=True)
                        
                        if(len(Gcc) >= 2):
                            #print(H_k_edge_diff_dic)
                            return list(Gcc)
                        
                        # 1 度エッジをカットしたら for 分を抜ける
                        break
                    
        
    
                
           
            
            # 距離k層 を更新
            for node in key_dist_dic[k+1]:
                k_dist_node_list.append(node)
                
            pre_dist_k_1_edge_list = []
            
            for node in dist_k_1_edge_list:
                pre_dist_k_1_edge_list.append(node)
                
            print(f" k={k} : {pre_dist_k_1_edge_list}")
                
        
        return 0
        
            
        
        
        

#------------------------------------------------------------------


