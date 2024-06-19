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
// c++ acc_main.cpp graph.cpp read.cpp -std=gnu++17 -O3 -march=native -o a.out 

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
    double eps = 0.1;

    vector<int> node_list_vector = graph.get_node_list();

    // self_ppr 値
    unordered_map<int, double> self_ppr;

    // Proposed 2
    auto start = chrono::system_clock::now();

    for (int src_id : node_list_vector){
        double delta = graph.determine_delta(src_id, alpha);
        int walk_count = graph.calc_omega(delta, eps);
        unordered_map<int, double> ppr = graph.calc_ppr_by_fora(src_id, walk_count, alpha, r_max_coef);
        self_ppr[src_id] = ppr[src_id];
    }

    auto end = chrono::system_clock::now();

    chrono::duration<double> elapsed = end - start;

    cout << "Proposed_2 : " << elapsed.count() << "sec" << endl;  





    auto start_sort_1 = chrono::system_clock::now();

    // ppr を value ソート
    typedef pair<int, double> pair;
    vector<pair> vec;

    copy(self_ppr.begin(), self_ppr.end(), back_inserter<vector<pair> >(vec));

    sort(vec.rbegin(), vec.rend(), [](const pair &l, const pair &r)
    {
        if(l.second != r.second){
            return l.second < r.second;
        }
        return l.first < r.first;
    });

    // 上位 k ノードの SelfPPR 値　を取り出す
    unordered_map<int, double> top_k_self_ppr;
    vector<int> top_k_node_list;
    int k = 100;

    unordered_map<int, double> new_eps_map;
    unordered_map<int, double> d_map;

    int cnt = 1;

    for(auto const &pair: vec){
        top_k_self_ppr[pair.first] = pair.second;
        top_k_node_list.push_back(pair.first);
        new_eps_map[pair.first] = eps;
        d_map[pair.first] = 0;
        cnt += 1;

        if (cnt > k){
            break;
        }
    }

    cout << top_k_self_ppr.size() << endl;

    auto end_sort_1 = chrono::system_clock::now();

    chrono::duration<double> elapsed_sort_1 = end_sort_1 - start_sort_1;

    cout << "Sort_1 : " << elapsed_sort_1.count() << "sec" << endl;





    // 2 つの 還流度値を比較して差が ((2*eps)/(1-eps)) * x よりもあれば PPRを再計算

    auto start_sort_2 = chrono::system_clock::now();

    int flag = 1;

    double omega_sum = 0;
    int cnt_node = 0;

    while(flag == 1){

        vector<int> re_omega_id_list;

        for (int i = 0; i < (top_k_node_list.size() - 1); i++){

            double eps_para = ( (new_eps_map[top_k_node_list[i]] + new_eps_map[top_k_node_list[i+1]]) / (1 - new_eps_map[top_k_node_list[i]]) );
            double d = top_k_self_ppr[i] - top_k_self_ppr[i + 1];
            if(eps_para * top_k_self_ppr[top_k_node_list[i + 1]] > d){
                re_omega_id_list.push_back(top_k_node_list[i + 1]);
                d_map[top_k_node_list[i + 1]] = d;
            }
        }

         // 再計算必要なくなったらループから抜ける
        if(re_omega_id_list.empty()){
            flag = 0;
            break;

        // それ以外は再計算
        } else {
            for(int src_id : re_omega_id_list){
                double ppr_val = top_k_self_ppr[src_id];
                double eps = graph.determine_new_eps(ppr_val, new_eps_map[src_id], d_map[src_id]);
                new_eps_map[src_id] = eps;
                double delta = graph.determine_delta(src_id, alpha);
                int walk_count = graph.calc_omega(delta, eps);
                omega_sum += walk_count;
                cnt_node += 1;
                unordered_map<int, double> ppr = graph.calc_ppr_by_fora(src_id, walk_count, alpha, r_max_coef);
                top_k_self_ppr[src_id] = ppr[src_id];
            }

            vector<pair> vec;
            copy(top_k_self_ppr.begin(), top_k_self_ppr.end(), back_inserter<vector<pair> >(vec));

            sort(vec.rbegin(), vec.rend(), [](const pair &l, const pair &r)
            {
                if(l.second != r.second){
                    return l.second < r.second;
                }
                return l.first < r.first;
            });

            top_k_node_list.clear();

            for(auto const &pair: vec){
                top_k_node_list.push_back(pair.first);
            } 

        }
    }

    auto end_sort_2 = chrono::system_clock::now();

    chrono::duration<double> elapsed_sort_2 = end_sort_2 - start_sort_2;

    cout << "Sort_2 : " << elapsed_sort_2.count() << "sec" << endl;

    cout << "check times : " << cnt_node << endl;

    cout << "Average omega : " << int(ceil(omega_sum/static_cast<double>(cnt_node))) << endl;



    return 0;

}