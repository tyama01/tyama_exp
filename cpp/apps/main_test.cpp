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
// c++ main_test.cpp graph.cpp read.cpp -std=gnu++17 -O3 -march=native -o a.out 

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

    vector<int> node_list_vector = graph.get_node_list();

     // SSPPR
    auto start_ss = chrono::system_clock::now();

    for (int src_id : node_list_vector){
        double delta = 1/N;
        int walk_count = graph.calc_omega(delta);
        cout << "SSPPR : " << walk_count << endl;
        break;
        //unordered_map<int, double> ppr = graph.calc_ppr_by_fora(src_id, walk_count, alpha, r_max_coef);
    }

    auto end_ss = chrono::system_clock::now();

    chrono::duration<double> elapsed_ss = end_ss - start_ss;

    //cout << "SSPPR : " << elapsed_ss.count() << "sec" << endl;

     // BATON
    auto start_bt = chrono::system_clock::now();

    for (int src_id : node_list_vector){
        int deg = graph.get_degree(src_id);
        double delta = (alpha * (1 - alpha)) / deg;
        //cout << delta << endl;
        int walk_count = graph.calc_omega(delta);
        cout << "BATON : " << walk_count << endl;
        break;

        //unordered_map<int, double> ppr = graph.calc_ppr_by_fora(src_id, walk_count, alpha, r_max_coef);
    }

    auto end_bt = chrono::system_clock::now();

    chrono::duration<double> elapsed_bt = end_bt - start_bt;

    //cout << "BATON : " << elapsed_bt.count() << "sec" << endl;


    // Proposed 1
    auto start1 = chrono::system_clock::now();

    for (int src_id : node_list_vector){
        int walk_count = graph.calc_omega(alpha);

        cout << "Proposed_1 : "  << walk_count << endl;
        break;
        //unordered_map<int, double> ppr = graph.calc_ppr_by_fora(src_id, walk_count, alpha, r_max_coef);
    }

    auto end1 = chrono::system_clock::now();

    chrono::duration<double> elapsed = end1 - start1;

    //cout << "Proposed_1 : " << elapsed.count() << "sec" << endl;


    // Proposed 2
    auto start2 = chrono::system_clock::now();

    

    for (int src_id : node_list_vector){
        double delta = graph.determine_delta(src_id, alpha);
        int walk_count = graph.calc_omega(delta);

        cout << "Proposed_2 : " << walk_count << endl;
        break;
        //unordered_map<int, double> ppr = graph.calc_ppr_by_fora(src_id, walk_count, alpha, r_max_coef);
    }

    auto end2 = chrono::system_clock::now();

    chrono::duration<double> elapsed2 = end2 - start2;

    //cout << "Proposed_2 : " << elapsed2.count() << "sec" << endl;  


    return 0;

}