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
// c++ selfpr_main.cpp graph.cpp read.cpp -std=gnu++17 -O3 -march=native -o a.out 

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

    double alpha = 0.1;
    double r_max_coef = 1;
    double eps = 0.1;

    unordered_map<int, double> selfpr = graph.calc_selfpr_by_fora(alpha, eps, r_max_coef);

    cout << "End calc" << endl;

    // map valueソート して出力
    typedef pair<int, double> pair;
    vector<pair> vec;

    copy(selfpr.begin(), selfpr.end(), back_inserter<vector<pair> >(vec));

    sort(vec.rbegin(), vec.rend(), [](const pair &l, const pair &r)
    {
        if(l.second != r.second){
            return l.second < r.second;
        }
        return l.first < r.first;
    });

    string result_path = "selfpr_15_01.txt";
    ofstream ofs;
    ofs.open(result_path);

    for(auto const &pair: vec){
        ofs << pair.first << " " << pair.second << endl;
    }


    return 0;

}