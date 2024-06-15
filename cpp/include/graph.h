#ifndef GRAPH_H_
#define GRAPH_H_

#include <iostream>
#include <vector>
#include <map>
#include <unordered_map>
#include <set>
#include <unordered_set>
#include <time.h>
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

class Graph{
    private:
        unordered_set<int> node_list_set;
        unordered_map<int, vector<int> > adj_list; // ノードid -> 隣接ノードのvector
        double r_max_func(int degree, double alpha, int walk_count, double r_max_coef) const {
            return (double)degree * r_max_coef / (alpha * (double)walk_count);
        }

    public:
        // getter 関数
        const unordered_map<int, vector<int> >& get_adj_list();
        const int get_number_of_nodes();
        const int get_number_of_edges();

        /* グラフの操作 */

        // エッジ追加　有向グラフ
        void d_add_edge(int n1, int n2);

        // エッジ追加 無向グラフ
        void u_add_edge(int n1, int n2);

        // 着目ノードの次数
        const int get_degree(int node_id);

        // 着目ノードのランダムな隣接ノードを一つ取得
        const int get_random_adjacent(int node_id);


        // ノードリスト(vector)を取得
        const vector<int> get_node_list();


        // FORA 実装
        const vector<int> get_random_walk_end_nodes(int src_id, int walk_count, double alpha);
        const pair<unordered_map<int, double>, unordered_map<int, double> > calc_ppr_by_fp(int src_id, int walk_count, double alpha, double r_max_coef);
        const unordered_map<int, double> calc_ppr_by_fora(int src_id, int walk_count, double alpha, double r_max_coef);

        // RWer 数を決める関数
        int calc_omega(double delta, double eps);

        // delta を求める (α 以上)
        double determine_delta(int src_id, double alpha);

        // 比較関数を定義
        bool comareByValue(const pair<int, int>& a, const pair<int, int>& b){
            return a.second > b.second; // 値で降順にソート
        }


};

#endif // GURAD_GRAPH_H