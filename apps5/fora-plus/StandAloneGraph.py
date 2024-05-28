from Node import *
from queue import Queue
import numpy as np
from scipy import sparse
from scipy.sparse import lil_matrix
import sys
import math

class StandAloneGraph():
    def __init__(self, file_path, is_directed):
        f = open(file_path)
        edges = f.read()
        f.close()
        edges = edges.split('\n')
        del edges[-1]
        for i in range(len(edges)):
            edges[i] = edges[i].split()

        self.nodes = dict()
        self.edge_list = list()
        self.is_directed = is_directed
        for edge in edges:
            src_id = int(edge[0])
            dst_id = int(edge[1])
            if src_id not in self.nodes.keys():
                self.nodes[src_id] = Node(src_id)
            if dst_id not in self.nodes.keys():
                self.nodes[dst_id] = Node(dst_id)
            src_node = self.nodes[src_id]
            dst_node = self.nodes[dst_id]
            src_node.add_edge(dst_node)
            self.edge_list.append((src_node, dst_node))
            if not is_directed:
                dst_node.add_edge(src_node)
                self.edge_list.append((dst_node, src_node))
        
        if len(edges[0]) == 2:
            random.shuffle(self.edge_list)
            print('Static Graph is initialized')
        else:
            print('Dynamic Graph is initialized')

    def get_paths(self, source_id, count, alpha):
        paths = list()
        source_node = self.nodes[source_id]
        for i in range(count):
            current_node = source_node
            path = [source_node.id]
            while True:
                if random.random() < alpha:
                    break
                current_node = current_node.get_random_adjacent()
                path.append(current_node.id)
            paths.append(path)
        return paths

    def get_random_walk_end_node_id_list(self, source_id, count, alpha):
        end_node_id_list = list()
        source_node = self.nodes[source_id]
        for _ in range(count):
            current_node = source_node
            while True:
                if random.random() < alpha:
                    end_node_id_list.append(current_node.id)
                    break
                current_node = current_node.get_random_adjacent()
        return end_node_id_list


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

    # epsilon 
    def calc_ppr_by_power_iteration(self, source_id, alpha, epsilon):
        transition_matrix, index_to_node_id = self.create_transiton_matrix_for_PPR(source_id, alpha)
        ppr_vec = np.random.rand(len(self.nodes))
        norm = np.linalg.norm(ppr_vec,ord=1)
        for i in range(len(self.nodes)):
            ppr_vec[i] /= norm

        prev = ppr_vec
        new = transition_matrix * prev
        count = 1
        diff = 1
        while (diff > epsilon):
            prev = new
            new = transition_matrix * prev
            diff = np.linalg.norm((new - prev), ord=1)
            count += 1

        ppr_dict = dict()
        for i, ppr_val in enumerate(new):
            ppr_dict[index_to_node_id[i]] = ppr_val
        return ppr_dict

    def create_transiton_matrix_for_PPR(self, source_id, alpha):
        node_id_list = list(self.nodes.keys())
        node_count = len(node_id_list)
        node_id_list.sort()
        node_id_to_index = dict()
        index_to_node_id = dict()
        for i, node_id in enumerate(node_id_list):
            node_id_to_index[node_id] = i
            index_to_node_id[i] = node_id

        transition_matrix = lil_matrix((node_count, node_count))
        for i, node_id in enumerate(node_id_list):
            transition_matrix[node_id_to_index[source_id],i] = alpha
            degree = self.nodes[node_id].degree
            if degree == 0:
                transition_matrix[i, i] = 1 - alpha
            else:
                for adj_id in self.nodes[node_id].adj.keys():
                    transition_matrix[node_id_to_index[adj_id],i] += (1-alpha)/degree
        return transition_matrix.tocsr(), index_to_node_id

    def calc_ppr_by_forward_push(self, source_id, alpha, walk_count):
        source_node = self.nodes[source_id]
        r_dict = dict()
        ppr_dict = dict()
        r_dict[source_id] = 1
        push_queue = Queue()
        push_queue.put(source_node)
        source_node.in_push_queue = True
        while not push_queue.empty():
            node = push_queue.get()
            node.in_push_queue = False
            if node.degree != 0:
                for adj_node in node.adj.values():
                    
                    # 隣接ノードに PPR 値を push 左：隣接ノードのキーを入力して PPR 値を 0 とする。 右：push した PPR 値を足す
                    r_dict[adj_node.id] = r_dict.get(adj_node.id, 0) + (1 - alpha) * r_dict[node.id] / node.degree
                    
                    # 残余が閾値を超えている場合、そのノードの隣接をキューに追加
                    if (r_dict[adj_node.id] > adj_node.degree / (alpha * walk_count)) and (adj_node.in_push_queue == False):
                        push_queue.put(adj_node)
                        adj_node.in_push_queue = True
                        
                ppr_dict[node.id] = ppr_dict.get(node.id, 0) + alpha * r_dict[node.id]
                
                
            else:
                ppr_dict[node.id] = ppr_dict.get(node.id, 0) + r_dict[node.id]
                
            r_dict[node.id] = 0

        return ppr_dict, r_dict
    
    def calc_conductance(self, node_id_set):
        total_edge_count = len(self.edge_list)
        cut_count = 0
        total_degree = 0
        for node_id in node_id_set:
            total_degree += self.nodes[node_id].degree
            for adj_id in self.nodes[node_id].adj.keys():
                if adj_id not in node_id_set:
                    cut_count += 1
        return cut_count / min(total_degree, total_edge_count - total_degree)

    def calc_PPR_by_fora(self, source_id, alpha, walk_count, has_index):
        
        
        ppr_dict, residue_dict = self.calc_ppr_by_forward_push(source_id, alpha, walk_count)

        for node_id, r_val in residue_dict.items():
            if r_val == 0:
                continue
            walk_count_i = math.ceil(r_val * walk_count)
            
            if has_index:
                end_node_id_list = self.index_for_fora_plus[node_id][:walk_count_i]
            else:
                
                # 終点ノードだけを保持したリスト
                end_node_id_list = self.get_random_walk_end_node_id_list(node_id, walk_count_i, alpha)
            
            for end_node_id in end_node_id_list:
                ppr_dict[end_node_id] = ppr_dict.get(end_node_id, 0) + r_val / walk_count_i
        
        return ppr_dict

    def set_index_for_fora_plus(self, alpha):
        self.index_for_fora_plus = dict()
        for node in self.nodes.values():
            precompute_count = math.ceil(node.degree / alpha)
            self.index_for_fora_plus[node.id] = self.get_random_walk_end_node_id_list(node.id, precompute_count, alpha)
        return

