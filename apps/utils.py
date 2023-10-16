import networkx as nx
import random

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

# 周辺類似性指数 PSI エッジの重みづけ
class PSI:
    def __init__(self, G):
        self.G = G
        
        # エッジの重み {id : {id : 重み}}
        self.edge_weight = {id : {} for id in list(self.G.nodes)}
    
    # PSI 計算
    def calc_psi(self):
        
        # 全ノードに対して行う
        for id in list(self.G.nodes):
            
            # id の隣接に対して
            neighbors = list(self.G.neighbors(id))
            
            for neigh_id in neighbors:
                self.edge_weight[id][neigh_id] = 1
            
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
                        
                        self.edge_weight[id][neigh_id] += round(d/n, 1)
        
        return self.edge_weight
    
    # PSI の重みつきグラフを txt ファイルで出力
    def out_put_psi_graph(self, dataset_name):
        
        self.calc_psi()
        
        output_file = dataset_name + "_psi.txt"
        out_path = "../datasets/" + output_file
        
        f = open(out_path, 'w')
        
        for v in self.edge_weight:
            for neigh_v in self.edge_weight[v]:
                f.write(str(v) + " ")
                f.write(str(neigh_v) + " ")
                f.write(str(self.edge_weight[v][neigh_v]))
                f.write('\n')
                
        f.close()
        
        
        
        
            
