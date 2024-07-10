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


#------------------------------------------------------------------

#------------------------------------------------------------------

# PPR 演算    
class PPR:
    def __init__(self, G):
        self.G = G    
    
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
                    # random_index = random.randrange(len(node_list))
                    # current_node = node_list[random_index]
                    # path.append(current_node)
                    
                    # 強制終了 RWer を死亡させる
                    current_node = source_node
                    break
                    
                    
                    
                    
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

#------------------------------------------------------------------

# FORA 実装
class FORA:
    def __init__(self, G):
        self.G = G
        self.node_list = list(self.G.nodes)
        self.push_queue_dict = {node : False for node in list(self.G.nodes)}
        
    def calc_ppr_by_forward_push(self, source_node, alpha, walk_count):
        
        r_dict = dict()
        ppr_dict = dict()
        r_dict[source_node] = 1
        push_queue = Queue()
        push_queue.put(source_node)
        self.push_queue_dict[source_node] = True
        
        while not push_queue.empty():
            node = push_queue.get()
            self.push_queue_dict[node] = False
            
            neighbors = list(self.G.neighbors(node))
            
            if len(neighbors) != 0:
                for adj_node in neighbors:
                    
                    # 隣接ノードに PPR 値を push 左：隣接ノードのキーを入力して PPR 値を 0 とする。 右：push した PPR 値を足す
                    r_dict[adj_node] = r_dict.get(adj_node, 0) + (1 - alpha) * r_dict[node] / len(neighbors)
                    
                    
                    # 残余が閾値を超えている場合、そのノードの隣接をキューに追加
                    adj_neighbors = list(self.G.neighbors(adj_node))
                    
                    if (r_dict[adj_node] > len(adj_neighbors)/(alpha * walk_count)) and (self.push_queue_dict[adj_node] == False):
                        push_queue.put(adj_node)
                        self.push_queue_dict[adj_node] = True
                        
                
                ppr_dict[node] = ppr_dict.get(node, 0) + alpha * r_dict[node]
                
            else:
                ppr_dict[node] = ppr_dict.get(node, 0) + alpha * r_dict[node]
                #r_dict[source_node] += r_dict[node] * (1 - alpha)
                
            r_dict[node] = 0
            
        return ppr_dict, r_dict    
    
    def get_random_walk_end_node_list(self, source_node, count, alpha):
        end_node_list = list()
        for _ in range(count):
            current_node = source_node
            while True:
                if random.random() < alpha:
                    end_node_list.append(current_node)
                    break
                
                neighbors = list(self.G.neighbors(current_node))
                random_index = random.randrange(len(neighbors))
                current_node = neighbors[random_index]
                
        return end_node_list
    
    def set_index_for_fora_plus(self, alpha):
        self.index_for_fora_plus = dict()
        
        for node in self.node_list:
            neighbors = list(self.G.neighbors(node))
            precompute_count = math.ceil(len(neighbors) / alpha)
            
            self.index_for_fora_plus[node] = self.get_random_walk_end_node_list(node, precompute_count, alpha)
    
    
        return
        
    def calc_PPR_by_fora(self, source_node, alpha, walk_count, has_index):
        
        ppr_dict, residue_dict = self.calc_ppr_by_forward_push(source_node, alpha, walk_count)
        
        for node, r_val in residue_dict.items():
            if r_val == 0:
                continue
            
            walk_count_i = math.ceil(r_val * walk_count)
            
            if has_index:
                end_node_list = self.index_for_fora_plus[node][:walk_count_i]
                
            else:
                
                end_node_list = self.get_random_walk_end_node_list(node, walk_count_i, alpha)
                
                
            for end_node in end_node_list:
                ppr_dict[end_node] = ppr_dict.get(end_node, 0) + r_val / walk_count_i



        return ppr_dict
    
    
    # Self PPR の デルタ を決める
    def determine_delta(self, source_node, alpha):
        
        
        # source node の隣接ノード
        adj_list = list(self.G.neighbors(source_node))
        
        # source node の次数
        source_node_degree = len(adj_list)
        
        # hamonic_centrality の計算 source ノードの隣接ノードの次数の逆数の総和
        hamonic_c = 0
        
        for adj_node in adj_list:
            hamonic_c += 1 / (self.G.degree[adj_node])
            
        # 公比
        r = (((1 - alpha) * (1 - alpha)) / source_node_degree) * hamonic_c
        
        deno = 1 - r
        delta = alpha / deno
        
        return delta
    
    
#------------------------------------------------------------------

#------------------------------------------------------------------


# エッジ還流度 演算

class EPPR:
    def __init__(self, G):
        self.G = G
        self.edge_list = list(self.G.edges())
        
    
    # エッジ還流度を計算 (次数 1を含むエッジは除く)    
    def calc_edge_selfppr(self, node_selfppr):
        
        edge_selfppr = {}
        
        for edge in self.edge_list:
            
            edge_selfppr_val = 0
            flag = 1
            
            for id in edge:
                
                neighbors_list = list(self.G.neighbors(id))
                neighbors_num = len(neighbors_list)
                
                # 次数 1 のやつは除く
                if(neighbors_num == 1):
                    flag = 0
                    break
                
                # ノード の還流度 / そのノードの出次数
                edge_selfppr_val += node_selfppr[id] / neighbors_num
            
            if (flag == 1):    
                edge_selfppr[edge] = edge_selfppr_val
            
            
        return edge_selfppr
    
    
    
    # 還流度の低いエッジを削除していってコミュニティを取得, ただし、次数 1 のやつはスルー
    def get_community_sub_graph_nodes(self, edge_selfppr, k):
        
        # 元グラフの情報を保持しておきたい
        G_copy = self.G.copy()
        
        Gcc = sorted(nx.connected_components(G_copy), key=len, reverse=True)    
        
        
        
        # エッジ還流度が低い順からエッジを削除
        for tmp in sorted(edge_selfppr.items(), key=lambda x:x[1], reverse=False):
            #print(tmp[1])
            
            # エッジ削除
            node_a_deg = len(list(G_copy.neighbors(tmp[0][0])))
            node_b_deg = len(list(G_copy.neighbors(tmp[0][1])))
            
            if(node_a_deg == 1 or node_b_deg == 1):
                continue
            
            G_copy.remove_edge(*tmp[0])
            
            Gcc = sorted(nx.connected_components(G_copy), key=len, reverse=True)
            
            if(len(Gcc) == k):
                break
            
    
        return Gcc
    
    
    # 提案手法で得られた分割のモジュラリティを計算
    def calc_modularity(self, edge_selfppr, k):
        
        # 元グラフの情報を保持しておきたい
        G_copy = self.G.copy()
        
        Gcc = sorted(nx.connected_components(G_copy), key=len, reverse=True)
        
        mod_list = []    
        
        
        
        # エッジ還流度が低い順からエッジを削除
        for tmp in sorted(edge_selfppr.items(), key=lambda x:x[1], reverse=False):
            #print(tmp[1])
            
            # 連結成分数
            min_c_num = len(Gcc)
            
            # エッジ削除
            node_a_deg = len(list(G_copy.neighbors(tmp[0][0])))
            node_b_deg = len(list(G_copy.neighbors(tmp[0][1])))
            
            if(node_a_deg == 1 or node_b_deg == 1):
                continue
            
            # if(tmp[0][0] not in Gcc[0] or tmp[0][1] not in Gcc[0]):
            #     #print("Nooooooooooooooo!!")
            #     continue
            
            G_copy.remove_edge(*tmp[0])
            
            Gcc = sorted(nx.connected_components(G_copy), key=len, reverse=True)
            
            Gcc_min = Gcc[-1]
            
            if(len(Gcc_min) < 10):
                G_copy.add_edge(*tmp[0])
                
            Gcc = sorted(nx.connected_components(G_copy), key=len, reverse=True)
            
            
            
            if(len(Gcc) > min_c_num):
                part = []
                
                for group_nodes in Gcc:
                    part.append(group_nodes)
                    
                #print(f"{min_c_num} : {nx.community.modularity(self.G, part)}")
                mod_list.append(nx.community.modularity(self.G, part))
                                
                    
            if(len(Gcc) == k):
                break
            
    
        return Gcc, mod_list
        
    
    
#------------------------------------------------------------------



#------------------------------------------------------------------
# NDCG の計算
class NDCG:
    def __init__(self, nodes_num):
        self.nodes_num = nodes_num
        
    def ndcg(self, rel_true, rel_pred, p=None, form="linear"):
        """ Returns normalized Discounted Cumulative Gain
        Args:
            rel_true (1-D Array): relevance lists for particular user, (n_songs,)
            rel_pred (1-D Array): predicted relevance lists, (n_pred,)
            p (int): particular rank position
            form (string): two types of nDCG formula, 'linear' or 'exponential'
        Returns:
            ndcg (float): normalized discounted cumulative gain score [0, 1]
        """
        rel_true = np.sort(rel_true)[::-1]
        p = min(len(rel_true), len(rel_pred))
        discount = 1 / (np.log2(np.arange(p) + 2))

        if form == "linear":
            idcg = np.sum(rel_true[:p] * discount)
            dcg = np.sum(rel_pred[:p] * discount)
        elif form == "exponential" or form == "exp":
            idcg = np.sum([2**x - 1 for x in rel_true[:p]] * discount)
            dcg = np.sum([2**x - 1 for x in rel_pred[:p]] * discount)
        else:
            raise ValueError("Only supported for two formula, 'linear' or 'exp'")
        
        return dcg / idcg
    
    # 入力 正解の PR, 比較対象のPR 辞書型
    def calc_ndcg(self, pr_original, comp_pr, x_ratio):
        
        rel_true = list(pr_original.values())
        
        comp_pr_sort = sorted(comp_pr.items(), key=lambda x : x[1], reverse=True)
        
        comp_keys = []
        for item in comp_pr_sort:
            comp_keys.append(item[0])
        
        rel_pred = []
        for tmp_key in comp_keys:
            rel_pred.append(pr_original[tmp_key])
        
        top_x = int(self.nodes_num * x_ratio)
        
        return self.ndcg(rel_true, rel_pred[:top_x], form="exp")
        
        
        


#------------------------------------------------------------------



