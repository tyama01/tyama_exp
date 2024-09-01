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

