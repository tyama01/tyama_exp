import networkx as nx 
import random
import numpy as np

#------------------------------------------------------------------

# データセット読み込みのクラス
class DataLoader:
    def __init__(self, dataset_name, is_directed):
        self.dataset_name = dataset_name
        self.is_directed = is_directed
        
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

#------------------------------------------------------------------

#------------------------------------------------------------------

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

#------------------------------------------------------------------

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
                
                if(len(neighbors) == 0): # 有向エッジがない場合は終了
                    #random_index = random.randrange(len(node_list))
                    #current_node = node_list[random_index]
                    #path.append(current_node)
                    
                    current_node = source_node
                    break
                    #path.append(source_node)
                    #continue
                    
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
        
        if source_id not in visited_ratio: # 自ノードに帰ってこない場合は self PPR 値は0
            visited_ratio[source_id] = 0
        
        return visited_ratio
        
        # if source_id in visited_ratio:
        #     return visited_ratio[source_id]
        
        # else:
        #     return 0

#------------------------------------------------------------------

#------------------------------------------------------------------
## PPR から PR 演算
class PR:
    def __init__(self, G):
        self.G = G
        
    def calc_pr_by_ppr(self, ppr_dic, node_list, alpha, is_directed):
        n = len(node_list)
        pr = {target_node : 0 for target_node in ppr_dic}
        
        
        for src_node in ppr_dic:
            for target_node in ppr_dic[src_node]:
                pr[target_node] += ppr_dic[src_node][target_node] / n
                
        return pr
                    
               
        # 有向グラフの場合 dangling ノードのスコア分配をやると逆に精度が悪くなる、、、        
        if(is_directed):
                
            # dangling ノードを検出、スコアも再定義
            dangling_score_list = []
            for node in node_list:
                if(self.G.out_degree[node] == 0):
                    dangling_score = pr[node] / n
                    dangling_score_list.append(dangling_score)
                    pr[node] = 0
                else:
                    continue
                
            #print(f"dangling num : {len(dangling_score_list)}")
            #print(f"danglng score : {dangling_score_list[0]}")
            
            # ダングリングノードに溜まったスコアを分配        
            for dangling_score in dangling_score_list:
                for node in node_list:
                    pr[node] += dangling_score
                    
            return pr
        
        # 無向グラフの場合
        else:    
            return pr
        
        

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



