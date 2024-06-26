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
// c++ acc_main_x.cpp graph.cpp read.cpp -std=gnu++17 -O3 -march=native -o a.out 

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
    double min_eps = 0.1;

    vector<int> node_list_vector = graph.get_node_list();

    // self_ppr 値
    unordered_map<int, double> self_ppr;

    // Proposed 2
    auto start = chrono::system_clock::now();

    for (int src_id : node_list_vector){
        double delta = graph.determine_delta(src_id, alpha);
        int walk_count = graph.calc_omega(delta, min_eps);
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

    copy(self_ppr.begin(), self_ppr.end(), back_inserter<vector<pair_sort> >(vec));

    sort(vec.rbegin(), vec.rend(), [](const pair_sort &l, const pair_sort &r)
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

    int k = 100;


    // {id : new eps}
    unordered_map<int, double> new_eps_map;


    // {id : 一つppr 値が高いノードID}
    unordered_map<int, int> id_map;

    int cnt = 1;

    for(auto const &pair: vec){
        top_k_self_ppr[pair.first] = pair.second;
        top_k_node_list.push_back(pair.first);
        new_eps_map[pair.first] = min_eps;
        cnt += 1;

        if (cnt > k){ 
            break;
        }
    }

    std::cout << top_k_self_ppr.size() << endl;


    //auto end_sort_1 = chrono::system_clock::now();

    //chrono::duration<double> elapsed_sort_1 = end_sort_1 - start_sort_1;

    //std::cout << "Sort_1 : " << elapsed_sort_1.count() << "sec" << endl;





    // 2 つの 還流度値を比較して差が ((2*eps)/(1-eps)) * x よりもあれば PPRを再計算

    //auto start_sort_2 = chrono::system_clock::now();

    int flag = 1;

    long double omega_sum = 0;
    int cnt_node = 0;

    while(flag == 1){

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

                
                if(d > 1e-05){
                    re_omega_id_list_set.insert(top_k_node_list[i+1]);
                    //re_omega_id_list_set.insert(top_k_node_list[i]);

                    id_map[top_k_node_list[i+1]] = top_k_node_list[i];
                }

                //if(ppr_i < ppr_i_1){
                //if(top_k_self_ppr[top_k_node_list[i]] < top_k_self_ppr[top_k_node_list[i+1]]){
                //if (top_k_self_ppr[id_map[i+1]] < top_k_self_ppr[top_k_node_list[i+1]]){
                    //cout << "wrong !!!!!" << endl;
                //}
                
            }
            
        }

         // 再計算必要なくなったらループから抜ける
        //if(re_omega_id_list.empty()){
        if(re_omega_id_list_set.empty()){
        
            flag = 0;
            break;

        // それ以外は再計算
        } else {
            //for(int src_id : re_omega_id_list){
            for(int src_id : re_omega_id_list_set){
                double ppr_i_1 = top_k_self_ppr[src_id];
                double ppr_i = top_k_self_ppr[id_map[src_id]];

            

                double eps_i_1 = new_eps_map[src_id];
                double eps_i = new_eps_map[id_map[src_id]]; 

                if(ppr_i < ppr_i_1){
                    continue;
                }

                double new_eps = graph.calc_new_eps(ppr_i, ppr_i_1, eps_i, eps_i_1);

                if(new_eps <= 0){
                    continue;
                    //cout << "Nooooooooooooooooooo!!" << endl;
                }

                if(new_eps < min_eps){
                    min_eps = new_eps;
                }

                if(min_eps > new_eps/10){
                    min_eps = min_eps - 0.1 * min_eps;
                }


                new_eps_map[src_id] = min_eps;


                //cout << "ID :"<<  src_id << "-> eps : " << new_eps_map[src_id] << endl;
                cout << new_eps_map[src_id] << endl;

                double delta = graph.determine_delta(src_id, alpha);
                long long walk_count = graph.calc_omega(delta, new_eps_map[src_id]);
                omega_sum += walk_count;
                cnt_node += 1;
                unordered_map<int, double> ppr = graph.calc_ppr_by_fora(src_id, walk_count, alpha, r_max_coef);
                top_k_self_ppr[src_id] = ppr[src_id];
            }
        }

        cout << "------------- Loop End -----------------" << endl;

        vector<pair_sort> vec;
        copy(top_k_self_ppr.begin(), top_k_self_ppr.end(), back_inserter<vector<pair_sort> >(vec));

        sort(vec.rbegin(), vec.rend(), [](const pair_sort &l, const pair_sort &r)
        {
            if(l.second != r.second){
                return l.second < r.second;
            }
            return l.first < r.first;
        });

        top_k_node_list.clear();

        for(auto const &pair: vec){
            top_k_node_list.push_back(pair.first);
            new_eps_map[pair.first] = min_eps;
        } 

        
    }

    std::cout << "new eps : " << new_eps_map[top_k_node_list[40]] << endl;

    //auto end_sort_2 = chrono::system_clock::now();

    //chrono::duration<double> elapsed_sort_2 = end_sort_2 - start_sort_2;

    //std::cout << "Sort_2 : " << elapsed_sort_2.count() << "sec" << endl;

    auto end_sort_1 = chrono::system_clock::now();


    chrono::duration<double> elapsed_sort_1 = end_sort_1 - start_sort_1;

    std::cout << "Sort_1 : " << elapsed_sort_1.count() << "sec" << endl;

    std::cout << "check times : " << cnt_node << endl;

    std::cout << "Average omega : " << static_cast<long long>(omega_sum/static_cast<double>(cnt_node)) << endl;



    return 0;

}