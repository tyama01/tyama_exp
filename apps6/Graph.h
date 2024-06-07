#ifndef GRAPH_H_
#define GRAPH_H_
// #include "Node.h"
#include <iostream>
#include <vector>
#include <unordered_map>
#include <map>
#include <unordered_set>
#include <set>
#include <queue>
#include <algorithm>
#include <string>
#include <fstream>
#include <sstream>
#include <ctime>
#include <cstdlib>
#include <cmath>
// #define NDEBUG
#include <cassert>
using namespace std;

class Graph {
public:
    Graph(string data_dir, bool with_no_edge=false);

public:
    int node_size() const {
        return n;
    }
    int edge_size() const;
    int del_random_edge();
    // Node* get_node(int node_id);

    // node_id が dangling の場合，-1を返す
    int get_random_adjacent(int node_id) const;
    vector<vector<int>> get_paths(int src_id, int walk_count, double alpha) const;
    vector<int> get_random_walk_end_nodes(int src_id, int walk_count, double alpha) const;
    map<int, double> calc_ppr_by_rw(int src_id,  int walk_count, double alpha) const;
    pair<unordered_map<int, double>, unordered_map<int, double>> calc_ppr_by_fp(int src_id, int walk_count, double alpha, double r_max_coef=1.0) const;
    unordered_map<int, double> calc_ppr_by_fora(int src_id, int walk_count, double alpha, double r_max_coef=1) const;
    // map<int, double> calc_ppr_by_fora_plus(int src_id, int walk_count, double alpha, double r_max_coef, const unordered_map<int, map<int, vector<int>>>& precomputed_paths);
    unordered_map<int, double> calc_ppr_by_fora_plus(int src_id, int walk_count, double alpha, const vector<vector<int>>& precomputed_paths) const;
    unordered_map<int, double> calc_ppr_by_fora_plus(int src_id, int walk_count, double alpha, const vector<int>& precomputed_end_node_list) const;
    unordered_map<int, double> calc_ppr_by_fora_plus(int src_id, int walk_count, double alpha, const vector<deque<int>>& precomputed_paths) const;
    vector<double> calc_pagerank_by_power_iteration(double alpha, double epsilon) const;
    vector<pair<int, double>> get_ordered_ppr(map<int, double> ppr) const;
    bool get_is_directed() const {
        return is_directed;
    }
    void show_edge_list() const;
    // void insert_edge(Node* src_node, Node* dst_node); // undirected graph では両方向挿入
    
    // undirected graph では両方向挿入. 返り値は挿入したエッジ数
    int insert_edge(int src_id, int dst_id); 
    // undirected graph では両方向削除. 返り値は削除したエッジ数
    int remove_edge(int src_id, int dst_id); 

    int get_degree(int node_id) const {
        return adj_list_list[node_id].size();
    }
    vector<int> get_adj_list(int node_id) const {
        return adj_list_list[node_id];
    };

    vector<pair<int, int>> load_edge_list() const;
    int get_initial_edge_count() const {
        return initial_edge_count;
    }
    bool get_is_dynamic() const {
        return is_dynamic;
    }
    string get_data_dir() const {
        return data_dir;
    }
    void show_graph_size_in_kb() const;
    bool has_edge(int src_id, int dst_id) const;

private:
    // vector<Node> nodes;
    vector<vector<int>> adj_list_list;
    vector<unordered_set<int>> adj_set_list;
    double r_max_func(int degree, double alpha, int walk_count, double r_max_coef) const {
        return (double)degree * r_max_coef / (alpha * (double)walk_count);
    }
    bool is_directed;
    bool is_dynamic;
    int n; // # of nodes
    int initial_edge_count = -1;
    string data_dir;
};

#endif