#include "Graph.h"

Graph::Graph(string input_data_dir, bool with_no_edge) {
    data_dir = input_data_dir;
    char splitter = ' ';
    srand((unsigned int)time(NULL));
    fstream file;
    string attribute_file_path = string(getenv("HOME")) + "/dataset/" + data_dir + "/attributes.txt";
    file.open(attribute_file_path, ios::in);
    assert(file.is_open());
    string line, attribute, val;
    bool error_flag = false;
    while (getline(file, line)) {
        stringstream ss{line};
        getline(ss, attribute, splitter);
        if (attribute == "n") {
            getline(ss, val, splitter);
            n = stoi(val);
        } else if (attribute == "is_directed") {
            getline(ss, val, splitter);
            if (val == "true") is_directed = true;
            else if (val == "false") is_directed = false;
            else error_flag = true;
        } else if (attribute == "is_dynamic") {
            getline(ss, val, splitter);
            if (val == "true") is_dynamic = true;
            else if (val == "false") is_dynamic = false;
            else error_flag = true;
        } else if (attribute == "initial_edge_count") {
            getline(ss, val, splitter);
            initial_edge_count = stoi(val);
        }
        else error_flag = true;
    }
    file.close();
    assert(!error_flag);
    // for (int node_id = 0; node_id < n; node_id++) nodes.push_back(Node(node_id));
    
    adj_list_list = vector<vector<int>>(n, vector<int>());
    adj_set_list = vector<unordered_set<int>>(n, unordered_set<int>());
    if (with_no_edge) return;
    else {
        string file_path = string(getenv("HOME")) + "/dataset/" + data_dir + "/indexed_edges.txt";
        file.open(file_path, ios::in);
        assert(file.is_open());
        string node_id_str;
        while (getline(file, line)) {
            stringstream ss{line};
            int src_id, dst_id;
            getline(ss, node_id_str, splitter);
            src_id = stoi(node_id_str);
            getline(ss, node_id_str, splitter);
            dst_id = stoi(node_id_str);
            if (src_id == dst_id) continue; // ignore self-loop
            
            int insert_count = insert_edge(src_id, dst_id);
            assert(insert_count > 0);

            // Node* src_node = &(nodes.at(src_id));
            // Node* dst_node = &(nodes.at(dst_id));
            // src_node -> add_edge(dst_node);
            // if (! is_directed) dst_node -> add_edge(src_node);
        }
        file.close();
        return;
    }
}

// int Graph::node_size() const {
//     return n;
// }

int Graph::edge_size() const {
    int edge_count = 0;
    // for ( itr = nodes.begin(); itr != nodes.end(); itr++) edge_count += (*itr).get_degree();
    for (int node_id = 0; node_id < n; node_id++) edge_count += adj_list_list.at(node_id).size();
    if (!is_directed) edge_count /= 2;
    return edge_count;
}

// Node* Graph::get_node(int node_id) {
//     return &(nodes.at(node_id));
// }

int Graph::get_random_adjacent(int node_id) const {
    vector<int> adj_list = adj_list_list.at(node_id);
    int degree = adj_list.size();
    if (degree == 0) return -1;
    else return adj_list.at((int)(rand() % degree));
}

// path.back() == -1 は dangling node で強制終了した path を表現
vector<vector<int>> Graph::get_paths(int src_id, int walk_count, double alpha) const {
    vector<vector<int>> paths;
    // const Node* src_node;
    // src_node = &(nodes.at(src_id));
    for (int i = 0; i < walk_count; i++) {
        vector<int> path;
        // const Node* current_node = src_node;
        int current_node_id = src_id;
        // Node* next_node;
        int next_node_id;
        bool is_dangling = false;
        do {
            if (is_dangling) {
                path.push_back(-1);
                break;
            }
            path.push_back(current_node_id);
            next_node_id = get_random_adjacent(current_node_id);
            if (next_node_id == -1) is_dangling = true;
            else current_node_id = next_node_id;
        } while ((double)rand()/RAND_MAX > alpha);
        
        paths.push_back(path);
    }
    return paths;
}

// path.back() == -1 は dangling node で強制終了した path を表現
vector<int> Graph::get_random_walk_end_nodes(int src_id, int walk_count, double alpha) const {
    vector<int> end_node_id_list;
    for (int i = 0; i < walk_count; i++) {
        int current_node_id = src_id;
        while ((double)rand()/RAND_MAX > alpha) {
            if (current_node_id == -1) break;
            current_node_id = get_random_adjacent(current_node_id);
        }
        end_node_id_list.push_back(current_node_id);
    }
    return end_node_id_list;
}

map<int, double> Graph::calc_ppr_by_rw(int src_id, int walk_count, double alpha) const {
    vector<vector<int>> paths = get_paths(src_id, walk_count, alpha);
    map<int, double> ppr;
    for (int i = 0; i < walk_count; i++) {
        vector<int> path = paths[i];
        int end_node_id = path.back();
        if (ppr.count(end_node_id) == 0) ppr.emplace(end_node_id, 0.0);
        ppr[end_node_id] += 1.0 / walk_count;
    }
    return ppr;
}

pair<unordered_map<int, double>, unordered_map<int, double>> Graph::calc_ppr_by_fp(int src_id, int walk_count, double alpha, double r_max_coef) const {
    unordered_map<int, double> ppr, residue;
    unordered_set<int> active_node_set;
    queue<int> active_node_queue;
    // Node* src_node = get_node(src_id);
    int src_degree = get_degree(src_id);
    active_node_set.insert(src_id);
    active_node_queue.push(src_id);
    residue.emplace(src_id, 1);
    while (active_node_queue.size() > 0) {
        int node_id = active_node_queue.front();
        int node_degree = get_degree(node_id);
        active_node_queue.pop();
        active_node_set.erase(node_id);
        // if (ppr.count(node_id) == 0) ppr.emplace(node_id, 0);
        // dangling node 到達時はスーパーノード-1に渡す．スーパーノードはactive node 対象外
        if (node_degree == 0) {
            ppr[node_id] += alpha * residue.at(node_id);
            // if (ppr.count(-1) == 0) ppr.emplace(-1, 0.0);
            ppr[-1] += (1 - alpha) * residue.at(node_id);
        } else {
            vector<int> adj_list = get_adj_list(node_id);
            for (int i = 0; i < node_degree; i++) {
                int adj_id = adj_list[i];
                int adj_degree = get_degree(adj_id);
                // if (residue.count(adj_id) == 0) residue.emplace(adj_id, 0);
                residue[adj_id] += (1 - alpha) * residue.at(node_id) / node_degree;
                if ((residue.at(adj_id) > r_max_func(adj_degree, alpha, walk_count, r_max_coef)) && (active_node_set.count(adj_id) == 0)) {
                    active_node_set.insert(adj_id);
                    active_node_queue.push(adj_id);
                }
            }
            ppr[node_id] += alpha * residue.at(node_id);
        }
        residue[node_id] = 0;
    }

    return make_pair(ppr, residue);
}

unordered_map<int, double> Graph::calc_ppr_by_fora(int src_id, int walk_count, double alpha, double r_max_coef) const {
    pair<unordered_map<int, double>, unordered_map<int, double>> tmp = calc_ppr_by_fp(src_id, walk_count, alpha, r_max_coef);
    unordered_map<int, double> ppr = tmp.first;
    unordered_map<int, double> residue = tmp.second;

    for (auto itr = residue.begin(); itr != residue.end(); itr++) {
        int node_id = itr->first;
        double r_val = itr->second;
        if (r_val == 0) continue;
        
        int walk_count_i = (int)ceil(r_val * walk_count);
        vector<int> end_node_id_list = get_random_walk_end_nodes(node_id, walk_count_i, alpha);
        for (int end_node_id : end_node_id_list) {
            if (ppr.count(end_node_id) == 0) ppr[end_node_id] = 0;
            ppr[end_node_id] += (double)r_val / walk_count_i;
        }
    }
    return ppr;
}

// map<int, double> Graph::calc_ppr_by_fora_plus(int src_id, int walk_count, double alpha, double r_max_coef, const unordered_map<int, map<int, vector<int>>>& precomputed_paths) {
//     pair<map<int, double>, map<int, double>> tmp = calc_ppr_by_fp(src_id, walk_count, alpha, r_max_coef);
//     map<int, double> ppr = tmp.first;
//     map<int, double> residue = tmp.second;

//     double r_sum = 0;
//     for (auto itr = residue.begin(); itr != residue.end(); itr++) {
//         r_sum += itr->second;
//     }
//     double omega = r_sum * walk_count;
//     for (auto itr = residue.begin(); itr != residue.end(); itr++) {
//         int node_id = itr->first;
//         double r_val = itr->second;
//         if (r_val == 0) {
//             continue;
//         }
//         int walk_count_i = (int)ceil(r_val * walk_count);
//         double walker_weight = (r_val / r_sum) * (omega / walk_count_i);
//         auto path_itr = precomputed_paths.at(node_id).end();
//         for (int i = 0; i < walk_count_i; i++) {
//             path_itr--;
//             vector<int> path = path_itr -> second;
//             int end_node_id = path.back();
//             if (ppr.count(end_node_id) == 0) ppr[end_node_id] = 0;
//             ppr[end_node_id] += walker_weight / walk_count;
//         }
//     }
//     return ppr;
// }

unordered_map<int, double> Graph::calc_ppr_by_fora_plus(int src_id, int walk_count, double alpha, const vector<vector<int>>& precomputed_paths) const {
    double r_max_coef = 1;
    pair<unordered_map<int, double>, unordered_map<int, double>> tmp = calc_ppr_by_fp(src_id, walk_count, alpha, r_max_coef);
    unordered_map<int, double> ppr = tmp.first;
    unordered_map<int, double> residue = tmp.second;

    for (auto itr = residue.begin(); itr != residue.end(); itr++) {
        int node_id = itr->first;
        double r_val = itr->second;
        if (r_val == 0) continue;
        int walk_count_i = (int)ceil(r_val * walk_count);
        auto end_node_id_itr = precomputed_paths.at(node_id).end();
        for (int i = 0; i < walk_count_i; i++) {
            end_node_id_itr--;
            int end_node_id = *end_node_id_itr;
            if (ppr.count(end_node_id) == 0) ppr[end_node_id] = 0;
            ppr[end_node_id] += double(r_val) / walk_count_i;
        }
    }
    return ppr;
}

unordered_map<int, double> Graph::calc_ppr_by_fora_plus(int src_id, int walk_count, double alpha, const vector<deque<int>>& precomputed_paths) const {
    double r_max_coef = 1;
    pair<unordered_map<int, double>, unordered_map<int, double>> tmp = calc_ppr_by_fp(src_id, walk_count, alpha, r_max_coef);
    unordered_map<int, double> ppr = tmp.first;
    unordered_map<int, double> residue = tmp.second;

    for (auto itr = residue.begin(); itr != residue.end(); itr++) {
        int node_id = itr->first;
        double r_val = itr->second;
        if (r_val == 0) continue;
        int walk_count_i = (int)ceil(r_val * walk_count);
        auto end_node_id_itr = precomputed_paths.at(node_id).end();
        for (int i = 0; i < walk_count_i; i++) {
            end_node_id_itr--;
            int end_node_id = *end_node_id_itr;
            if (ppr.count(end_node_id) == 0) ppr[end_node_id] = 0;
            ppr[end_node_id] += double(r_val) / walk_count_i;
        }
    }
    return ppr;
}

vector<double> Graph::calc_pagerank_by_power_iteration(double alpha, double epsilon) const {
    double tmp_sum = 0;
    vector<double> pr(n, 0);
    for (int i = 0; i < n; i++) {
        double tmp = (double)rand()/RAND_MAX;
        tmp_sum += tmp;
        pr[i] = tmp;
    }
    for (int node_id = 0; node_id < n; node_id++) 
        pr[node_id] = pr.at(node_id) / tmp_sum;

    double l1_norm;
    do {
        vector<double> new_pr(n, 0);
        double jump_val = 0.0;
        for (int node_id = 0; node_id < n; node_id++) {
            // Node* node = &(nodes.at(node_id));
            int node_degree = get_degree(node_id);
            double pr_val = pr.at(node_id);
            if (node_degree == 0) {
                jump_val += pr_val;
            } else {
                vector<int> adj_list = get_adj_list(node_id);
                for (auto itr = adj_list.begin(); itr != adj_list.end(); itr++) {
                    int adj_id = *itr;
                    new_pr[adj_id] += pr_val * (1 - alpha) / node_degree;
                }
                jump_val += pr_val * alpha;
            }
        }
        for (int node_id = 0; node_id < n; node_id++) {
            new_pr[node_id] += jump_val / n;
        }

        l1_norm = 0;
        for (int node_id = 0; node_id < n; node_id++) {
            l1_norm += abs(pr[node_id] - new_pr[node_id]);
            pr[node_id] = new_pr[node_id];
        }
    } while (l1_norm > epsilon);
    return pr;
}

vector<pair<int, double>> Graph::get_ordered_ppr(map<int, double> ppr) const {
    vector<pair<int, double>> ppr_vec;
    for(auto itr = ppr.begin(); itr != ppr.end(); ++itr) {
        ppr_vec.push_back({itr->first, itr->second});
    }
    sort(ppr_vec.begin(), ppr_vec.end(),
        [](const pair<int, double> &l, const pair<int, double> &r)
        {
            if (l.second != r.second) {
                return l.second > r.second;
            }
            return l.first < r.first;
        });
    
    return ppr_vec;
}

// double Graph::r_max_func(int degree, double alpha, int walk_count, double r_max_coef) const {
//     return degree * r_max_coef / (alpha * walk_count);
// }

// bool Graph::get_is_directed() const {
//     return is_directed;
// }

void Graph::show_edge_list() const {
    cout << "edge_list" << endl;
    for (int node_id = 0; node_id < n; node_id++) {
        vector<int> adj_list = get_adj_list(node_id);
        for (auto itr = adj_list.begin(); itr != adj_list.end(); itr++) {
            cout << node_id << " " << *itr << endl;
        }
    }
    cout << endl;
}

// void Graph::insert_edge(Node* src_node, Node* dst_node) {
//     int tmp_insert_count =  src_node -> add_edge(dst_node);
//     assert(tmp_insert_count == 1);
//     if (!is_directed) {
//         tmp_insert_count =  dst_node -> add_edge(src_node);
//         assert(tmp_insert_count == 1);
//     }
// }

int Graph::insert_edge(int src_id, int dst_id) {
    // Node* src_node = get_node(src_id);
    // Node* dst_node = get_node(dst_id);
    // insert_edge(src_node, dst_node);
    if (adj_set_list.at(src_id).count(dst_id) != 0) return 0;
    if (!is_directed) assert(adj_set_list.at(dst_id).count(src_id) == 0);

    adj_set_list.at(src_id).insert(dst_id);
    adj_list_list.at(src_id).push_back(dst_id);
    if (!is_directed) {
        adj_set_list.at(dst_id).insert(src_id);
        adj_list_list.at(dst_id).push_back(src_id);
        return 2;
    }
    return 1;
}

int Graph::remove_edge(int src_id, int dst_id) {
    if (adj_set_list.at(src_id).count(dst_id) == 0) {
        if (!is_directed) assert(adj_set_list.at(dst_id).count(src_id) == 0);
        return 0;
    }
    if (!is_directed) assert(adj_set_list.at(dst_id).count(src_id) != 0);

    adj_set_list.at(src_id).erase(dst_id);
    for (int node_index = 0; node_index < adj_list_list.at(src_id).size(); node_index++) {
        if (adj_list_list.at(src_id)[node_index] == dst_id) {
            adj_list_list.at(src_id)[node_index] = adj_list_list.at(src_id).back();
            adj_list_list.at(src_id).pop_back();
        }
    }
    if (!is_directed) {
        adj_set_list.at(dst_id).erase(src_id);
        for (int node_index = 0; node_index < adj_list_list.at(dst_id).size(); node_index++) {
        if (adj_list_list.at(dst_id)[node_index] == src_id) {
            adj_list_list.at(dst_id)[node_index] = adj_list_list.at(dst_id).back();
            adj_list_list.at(dst_id).pop_back();
        }
    }
        return 2;
    }
    return 1;
}

// int Graph::get_degree(int node_id) const {
//     return adj_list_list.at(node_id).size();
// }

// vector<int> Graph::get_adj_list(int node_id) const {
    // return adj_list_list.at(node_id);
// }

vector<pair<int, int>> Graph::load_edge_list() const {
    vector<pair<int, int>> edge_list;
    fstream file;
    string line;
    char splitter = ' ';
    string file_path = "/home/tullys2/dataset/" + data_dir + "/indexed_edges.txt";
    file.open(file_path, ios::in);
    assert(file.is_open());
    string edge_str;
    while (getline(file, line)) {
        stringstream ss{line};
        int src_id, dst_id;
        getline(ss, edge_str, splitter);
        src_id = stoi(edge_str);
        getline(ss, edge_str, splitter);
        dst_id = stoi(edge_str);
        if (src_id == dst_id) continue; // ignore self-loop
        edge_list.push_back(make_pair(src_id, dst_id));
    }
    file.close();

    return edge_list;
}

// int Graph::get_initial_edge_count() const {
    // return initial_edge_count;
// }

// bool Graph::get_is_dynamic() const {
//     return is_dynamic;
// }

void Graph::show_graph_size_in_kb() const {
    long long byte = 0;
    byte += sizeof(adj_list_list);
    for (vector<int> adj_list : adj_list_list) {
        byte += sizeof(adj_list);
        byte += sizeof(int) * adj_list.size();
    }

    byte += sizeof(adj_set_list);
    for (unordered_set<int> adj_set : adj_set_list) {
        byte += sizeof(adj_set);
        byte += sizeof(int) * adj_set.size();
    }

    cout << "graph\t" << byte / 1000 << " [KB]" << endl;
}

bool Graph::has_edge(int src_id, int dst_id) const {
    if (adj_set_list.at(src_id).count(dst_id) == 0) {
        if (!is_directed) assert(adj_set_list.at(dst_id).count(src_id) == 0);
        return false;
    }
    if (!is_directed) assert(adj_set_list.at(dst_id).count(src_id) != 0);
    return true;
}