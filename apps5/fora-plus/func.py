from StandAloneGraph import *
import json
import numpy as np
import copy
from decimal import Decimal, ROUND_HALF_UP
import matplotlib.pyplot as plt
import datetime
from pathlib import Path

def load_json(filepath):
    f = open(filepath, 'r')
    obj = json.load(f)
    f.close()
    return obj

def dump_json(obj, filepath):
    f = open(filepath, 'w')
    json.dump(obj, f)
    f.close()
    return

def get_timestamp():
    dt_now = datetime.datetime.now()
    return dt_now.strftime('%y/%m/%d %H:%M:%S')

def get_ranking(visited_count, k):
    sorted_count = sorted(visited_count.items(), key=lambda x: x[1], reverse=True)
    topk = list()
    if len(sorted_count) < k:
        repeat_count = len(sorted_count)
    else:
        repeat_count = k

    for i in range(repeat_count):
        topk.append(sorted_count[i][0])
    return topk

# approximate: ranking  e.g., [node1, node2, ..., nodek]
# exact: ranking & values  e.g., [(node1, val1), (node2, val2), ..., (nodek, valk)]
def dcg(approx_nodes, exact_dict):
    k = len(approx_nodes)
    rtn = 0
    for i in range(k):
        rtn += ((2 ** exact_dict.get(approx_nodes[i], 0) - 1) / np.log2(i+2))
    return rtn

def dcg_perfect(exact_dict, k):
    sorted_nodes = sorted(exact_dict.items(), key=lambda x: x[1], reverse=True)[:k]
    rtn = 0
    for i in range(len(sorted_nodes)):
        rtn += ((2 ** sorted_nodes[i][1] - 1) / np.log2(i+2))
    return rtn

def calc_ndcg(approx_nodes, exact_dict, k):
    return dcg(approx_nodes, exact_dict) / dcg_perfect(exact_dict, k)

def calc_accuracy(app_node_set, exact_node_set):
    return len(app_node_set & exact_node_set) / len(exact_node_set)

def calc_average_l1_norm(approx_dict, exact_dict, graph):
    l1_diff = 0
    for node_id in graph.nodes.keys():
        l1_diff += abs(exact_dict.get(node_id, 0) - approx_dict.get(node_id, 0))
    return l1_diff / len(graph.nodes)

def calc_RMSE(app_vals, exact_vals):
    total = 0
    copied_app_vals = copy.deepcopy(app_vals)
    while len(copied_app_vals) < len(exact_vals):
        copied_app_vals.append(0)
    for i in range(len(exact_vals)):
        total += (exact_vals[i] - copied_app_vals[i]) ** 2
    total /= len(exact_vals)
    return total ** 0.5

def calc_MAE(app_vals, exact_vals):
    total = 0
    copied_app_vals = copy.deepcopy(app_vals)
    while len(copied_app_vals) < len(exact_vals):
        copied_app_vals.append(0)
    for i in range(len(exact_vals)):
        total += abs(copied_app_vals[i] - exact_vals[i])
    total /= len(exact_vals)
    return total

def calc_ave_error_ratio(approx_vec, exact_vec, thr):
    error_ratio_list = list()
    for node_id, exact_val in exact_vec.items():
        if exact_val < thr:
            pass
        else:
            approx_val = approx_vec.get(node_id, 0)
            error_ratio_list.append(abs(approx_val - exact_val) / exact_val)
    return sum(error_ratio_list) / len(error_ratio_list)

def get_ordinal(i):
    ordinal = (lambda n: "%d%s" % (n, "tsnrhtdd"[(n / 10 % 10 != 1) * (n % 10 < 4) * n % 10::4]))(i)
    return ordinal

def get_attribute_str(data_dir, attribute):
    with open('{}/dataset/{}/attributes.txt'.format(Path.home(), data_dir), 'r') as f:
        txt = f.read()
        lines = txt.split('\n')
        del lines[-1]
        for line in lines:
            array = line.split()
            if array[0] == attribute:
                return array[1]
    class InvalidAttributeError(Exception):
        pass           
    raise InvalidAttributeError

def read_csv(file_path, splitter=' '):
    arrays = list()
    with open(file_path, 'r') as f:
        txt = f.read()
        lines = txt.split('\n')
        del lines[-1]
        for line in lines:
            array = line.split(splitter)
            arrays.append(array)
    return arrays

def strtobool(targetStr):
    return targetStr.lower() in ["y", "yes", "t", "true", "on", "1"]