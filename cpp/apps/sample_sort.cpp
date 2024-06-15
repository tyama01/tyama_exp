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
// c++ -std=c++14 sample_sort.cpp -O3 -march=native -o a.out 

using namespace std;

// 比較関数を定義
bool compareByValue(const std::pair<int, int>& a, const std::pair<int, int>& b) {
    return a.second > b.second; // 値で降順にソート
}

int main() {
    // unordered_map の定義
    std::unordered_map<int, int> myMap = {
        {1, 10},
        {2, 20},
        {3, 5},
        {4, 30}
    };

    // unordered_map をペアのベクトルに変換
    std::vector<std::pair<int, int> > vec(myMap.begin(), myMap.end());

    // 値で降順にソート
    std::sort(vec.begin(), vec.end(), compareByValue);

    // 結果を出力
    std::cout << "Sorted map by values in descending order:" << std::endl;
    for (pair<int, int> pair : vec) {
        std::cout << "Key: " << pair.first << ", Value: " << pair.second << std::endl;
    }

    return 0;
}