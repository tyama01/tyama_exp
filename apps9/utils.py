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
      
#------------------------------------------------------------------

#------------------------------------------------------------------
# SNMF 実装

class SNMF:
    def __init__(self, A):
        self.A = A * 100000000000000
        
    def get_Rvec(self, k, max_iter=200, tol=1e-4, random_state=None):
        
        if random_state is not None:
            np.random.seed(random_state)
            
        n = self.A.shape[0]
        R = np.random.rand(n, k)
        
        for _ in range(max_iter):
            R_old = R.copy()
            
            numerator = self.A @ R
            denominator = R @ (R.T @ R) + 1e-9
            
            R *= numerator / denominator
            
            if np.linalg.norm(R - R_old, 'fro') < tol:
                break

        return R
    
    # 呼び出す関数はこれ
    def get_best_Rvec(self, k, max_iter=200, tol=1e-4, n_runs=10):
        
        best_R = None
        best_obj_value = float('inf')
        
        for i in range(n_runs):
            R = self.get_Rvec(k, max_iter, tol, random_state=i)
            
            obj_value = np.linalg.norm(self.A - R @ R.T, 'fro')
            
            if obj_value < best_obj_value:
                best_obj_value = obj_value
                best_R = R
                
        return best_R    

#------------------------------------------------------------------




