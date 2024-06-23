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
// c++ acc_main_z.cpp graph.cpp read.cpp -std=gnu++17 -O3 -march=native -o a.out 

using namespace std;
namespace fs = std::filesystem;

int main(int argc, char* argv[]){

    /* グラフ選択 */
    string graph_name;
    std::cout << "Enter graph name : ";
    cin >> graph_name;

    /* グラフのデータセットがあるか確認 */
    string dataset_path = "../../datasets/" + graph_name + ".txt"; 
    if(!fs::is_regular_file(dataset_path)){ // なければ異常終了
        std::cout << "There are no such datasets" << endl;
        return 1;
    }

    /* グラフ読み込み */
    Graph graph;

    // 無向グラフ
    read_u_graph_from_text_file(dataset_path, graph);
    std::cout << "Compleate reading graph" << endl;

    /* グラフ情報(ノード数, エッジ数) */
    int N = graph.get_number_of_nodes();

    // 無向グラフなのでエッジ数は半分
    int E = graph.get_number_of_edges()/2;

    std::cout << "Nodes : " << N << endl;
    std::cout << "Edges : " << E << endl;

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

    std::cout << "Proposed_2 : " << elapsed.count() << "sec" << endl;  





    auto start_sort_1 = chrono::system_clock::now();

    // ppr を value ソート
    typedef pair<int, double> pair_sort;
    vector<pair_sort> vec;

    std::copy(self_ppr.begin(), self_ppr.end(), back_inserter<vector<pair_sort> >(vec));

    std::sort(vec.rbegin(), vec.rend(), [](const pair_sort &l, const pair_sort &r)
    {
        if(l.second != r.second){
            return l.second < r.second;
        }
        return l.first < r.first;
    });


    // 上位 k ノードの SelfPPR 値　を取り出す
    unordered_map<int, double> top_k_self_ppr;
    unordered_map<int, double> over_k_self_ppr;
    vector<int> top_k_node_list;
    vector<int> over_k_node_list;

    int k = 20;


    // {id : new eps}
    unordered_map<int, double> new_eps_map;

    // {id : 一つ前のノードのppr値差}
    unordered_map<int, double> d_map;

    // {id : 一つppr 値が高いノードID}
    unordered_map<int, int> id_map;

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

    std::cout << top_k_self_ppr.size() << endl;


    double omega_sum = 0;
    int cnt_node = 0;

    int flag = 0;

    while(1){

        //vector<int> re_omega_id_list;
        unordered_set<int> re_omega_id_list_set;

        for (int i = 0; i < (top_k_node_list.size() - 1); i++){

            double ppr_i = top_k_self_ppr[top_k_node_list[i]]; 
            double ppr_i_1 = top_k_self_ppr[top_k_node_list[i+1]];

            double d = ppr_i - ppr_i_1;

            pair<double, double> tmp_i = graph.calc_upper_and_lower_ppr(ppr_i, new_eps_map[top_k_node_list[i]]);
            double ppr_i_min = tmp_i.second;
            
            pair<double, double> tmp_i_1 = graph.calc_upper_and_lower_ppr(ppr_i_1, new_eps_map[top_k_node_list[i+1]]);
            double ppr_i_1_max = tmp_i_1.first;

            if(ppr_i_min < ppr_i_1_max){

                //double eps_para = ( (new_eps_map[top_k_node_list[i]] + new_eps_map[top_k_node_list[i+1]]) / (1 - new_eps_map[top_k_node_list[i+1]]) );
               
                re_omega_id_list_set.insert(top_k_node_list[i+1]);
                re_omega_id_list_set.insert(top_k_node_list[i]);
                   
                d_map[top_k_node_list[i + 1]] = d;

                id_map[top_k_node_list[i+1]] = top_k_node_list[i];
                
            }
        }

         // 再計算必要なくなったらループから抜ける
        if(re_omega_id_list_set.empty()){
            break;

        // それ以外は再計算
        } else {
            //for(int src_id : re_omega_id_list){
            for(int src_id : re_omega_id_list_set){
                double ppr_val = top_k_self_ppr[src_id];
                double ideal_eps = graph.determine_new_eps(ppr_val, new_eps_map[src_id], d_map[src_id]);
                double old_eps = new_eps_map[src_id];

                if(ideal_eps < 0){
                    new_eps_map[src_id] = old_eps / 100000;
                    cout << "Not" << endl;
                    //continue;

                }else{
                    new_eps_map[src_id] = ideal_eps;

                    cout << "Ideal" << endl;
                }

                //cout << "ID : " << src_id << "-> eps : " << new_eps_map[src_id] << endl;
                //cout << "ID : " << src_id << "-> d : " << d_map[src_id] << endl;




                double delta = graph.determine_delta(src_id, alpha);
                int walk_count = graph.calc_omega(delta, new_eps_map[src_id]);
                omega_sum += walk_count;
                cnt_node += 1;
                unordered_map<int, double> ppr = graph.calc_ppr_by_fora(src_id, walk_count, alpha, r_max_coef);
                top_k_self_ppr[src_id] = ppr[src_id];
            }

            

            vector<pair_sort> vec;
            std::copy(top_k_self_ppr.begin(), top_k_self_ppr.end(), back_inserter<vector<pair_sort> >(vec));

            std::sort(vec.rbegin(), vec.rend(), [](const pair_sort &l, const pair_sort &r)
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

    std::cout << "new eps : " << new_eps_map[top_k_node_list[5]] << endl;

   
    auto end_sort_1 = chrono::system_clock::now();


    chrono::duration<double> elapsed_sort_1 = end_sort_1 - start_sort_1;

    std::cout << "Sort_1 : " << elapsed_sort_1.count() << "sec" << endl;

    std::cout << "check times : " << cnt_node << endl;

    std::cout << "Average omega : " << int(ceil(omega_sum/static_cast<double>(cnt_node))) << endl;



    return 0;

}