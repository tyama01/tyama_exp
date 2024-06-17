#include <fstream>
#include <iostream>
#include <string>
#include <vector>
#include <unordered_map>
#include <filesystem>
#include <utility>
#include <bits/stdc++.h> // iota
#include <time.h> // time
#include <chrono>
#include <thread>
#include "../include/graph.h"
#include "../include/read.h"

// Files to compile
// c++ omega_num_main.cpp graph.cpp read.cpp -std=gnu++17 -O3 -march=native -o a.out 

using namespace std;
namespace fs = std::filesystem;

int main(int argc, char* argv[]){

    /* グラフ選択 */
    string graph_name;
    cout << "Enter graph name : ";
    cin >> graph_name;

    /* グラフのデータセットがあるか確認 */
    string dataset_path = "../../datasets/" + graph_name + ".txt"; 
    if(!fs::is_regular_file(dataset_path)){ // なければ異常終了
        cout << "There are no such datasets" << endl;
        return 1;
    }

    /* グラフ読み込み */
    Graph graph;

    // 無向グラフ
    read_u_graph_from_text_file(dataset_path, graph);
    cout << "Compleate reading graph" << endl;

    /* グラフ情報(ノード数, エッジ数) */
    int N = graph.get_number_of_nodes();

    // 無向グラフなのでエッジ数は半分
    int E = graph.get_number_of_edges()/2;

    cout << "Nodes : " << N << endl;
    cout << "Edges : " << E << endl;

    // パラメータ

    //int src_id = 0;
    //int walk_count = 10000;
    double alpha = 0.15;
    double r_max_coef = 1;
    double eps = 0.9;

    vector<int> node_list_vector = graph.get_node_list();

    // SSPPR RWer 数
    double delta_ss = 1/static_cast<double>(N);
    int omega_ss = graph.calc_omega(delta_ss, eps);

    cout << "SSPPR omega : " << omega_ss << endl;

    // BATON

    double omega_bt = 0;
    for (int src_id : node_list_vector){
        int deg = graph.get_degree(src_id);
        double delta = (alpha * (1 - alpha)) / static_cast<double>(deg);
        int walk_count = graph.calc_omega(delta, eps);
        omega_bt += walk_count / static_cast<double>(N);
    }

    cout << "BATON omega : " << int(ceil(omega_bt)) << endl;

    // Proposed 1
    int omega_1 = graph.calc_omega(alpha, eps);
    cout << "Proposed_1 omega : " << omega_1 << endl;


    // Proposed 2
    double omega_2 = 0;
    for (int src_id : node_list_vector){
        double delta = graph.determine_delta(src_id, alpha);
        int walk_count = graph.calc_omega(delta, eps);
        omega_2 += walk_count/static_cast<double>(N);   
    }

    cout << "Proposed_2 omega : " << int(ceil(omega_2)) << endl;


    return 0;
}