import Node as nd
import numpy as np
import matplotlib.pyplot as plt
import StandAloneGraph as sag
import random
import networkx as nx
from scipy import linalg
import sys
import math
from tqdm import tqdm
import appr

def compute_PPR(g, i):
    ppr = list(nx.pagerank(g, alpha=0.85, personalization={i:1},dangling={i:1}).values())
    return ppr

def compute_all_PPR(g):
    pprlist = list()
    for id in tqdm(nx.nodes(g)):
        pprlist.append(compute_PPR(g, id))
    return pprlist

def PR_weight_PPR(g, pr, com, pprlist, comnum):
    v = np.zeros((comnum, nx.number_of_nodes(g)))

    for id, prnum in pr.items():
        for i in range(comnum):
            if id in com[i]:
                v[i] = v[i] + (prnum * np.array(pprlist[id]))
    for i in range(comnum):
        v[i] = v[i] / v[i].sum()

    return v

def means_PPR(g, com, pprlist, comnum):
    v = np.zeros((comnum, nx.number_of_nodes(g)))

    for eachcom in com:
        for id in eachcom:
            index = com.index(eachcom)
            v[index] = v[index] + np.array(pprlist[id])
    
    for i in range(comnum):
        v[i] = v[i] / v[i].sum()

    return v

def compute_k(g, nodei, v, pprlist, comnum):
    k = np.zeros((comnum, 1))
    v_ppr = np.array(pprlist[nodei])
    A = np.dot(v, v.T)
    b = np.dot(v, v_ppr)
    k = linalg.solve(A, b)

    return k

## 分散計算を関数化
def compute_k_Dist(g, comi, comnum, vList, pprlist):
    comnodes = len(comi)
    klist = np.zeros((comnodes, comnum))

    i = 0
    meank = np.zeros((comnum, 1))
    for id in comi:
        klist[i] = compute_k(g, id, vList, pprlist, comnum)
        for j in range(comnum):
            meank[j] += klist[i][j] 
        # print(i)
        i = i + 1
    meank = meank / comnodes

    sum = 0
    for i in range(comnodes):
        val = 0  # 積なら1だが, 和なら0
        for j in range(comnum):  # kの成分ごとの和
            t = abs(klist[i][j] - meank[j])
            if t == 0:
                t = sys.float_info.min
            val = val + math.log10(t)
        sum += val
    sum = sum / (comnum * nx.number_of_nodes(g))
    return sum

def compute_k_all_Dist(g, com, comnum, vList, pprlist):
    sum = 0
    
    return sum

def Spread_Hubs_by_PR(g, k, pr):
    # Spread Hubsによってシード検出, シードノードのリストを返す
    seed = list()
    marknodes = list()
    sorted_pr = dict(sorted(pr.items(), reverse=True, key=lambda x:x[1]))
    # print(sorted_pr)
    while len(seed) < k:
        for nodeid, nodepr in sorted_pr.items():
            if nodeid not in marknodes:
                seed.append(nodeid)
                marknodes.append(nodeid)
                neighbors = nx.neighbors(g, nodeid)
                marknodes.extend(neighbors)
                break
        print(marknodes)
    return seed

def Spread_Hubs_by_Degree(g, k, degree):
    seed = list()
    marknodes = list()
    sorted_degree = dict(sorted(degree.items(), reverse=True, key=lambda x:x[1]))
    # print(sorted_degree)
    while len(seed) < k:
        for nodeid, nodedeg in sorted_degree.items():
            if nodeid not in marknodes:
                seed.append(nodeid)
                marknodes.append(nodeid)
                neighbors = nx.neighbors(g, nodeid)
                marknodes.extend(neighbors)
                break
        # print(marknodes)
    return seed

def Kernel_K_Means():
    return seed


## シードからノードクラスタリング
def seed_extended_clustering(g, pprlist, seed):

    return com

def random_clustering(g, k): # kはコミュニティ数
    # ランダム分割
    # 各ノードに対して, ランダムにコミュニティを割り当てる
    com = list()
    for i in range(k):
        com.append([])

    for i in list(nx.nodes(g)):
        x = random.randint(0, k - 1)
        com[x].append(i)
    return com

def ppr_sim_clustering(g, pprlist, seed, k): # kはseed数
    ## PPRベクトルのcos類似度で比べる
    com = list()
    pprnp = np.array(pprlist)
    # print(pprnp)
    for i in range(k):
        com.append([])

    for i in range(len(pprlist)):
        precom = 0
        prerbf = 0
        for j in seed:
            # rbf[j] = math.exp(GANMA * (np.linalg.norm((pprnp[i] - pprnp[j])) ** 2))
            rbf = np.dot(pprnp[j], pprnp[i]) / (np.linalg.norm(pprnp[j]) * np.linalg.norm(pprnp[i]))
            if prerbf < rbf:
                prerbf = rbf
                precom = j
        # print(precom)
        com[seed.index(precom)].append(i)

    # print(com)
    return com


def ppr_sim_clustering2(g, pprlist, pprv, k):
    com = list()
    pprnp = np.array(pprlist)
    pprvlist = pprv.tolist()
    for i in range(k):
        com.append([])
    
    for i in range(len(pprlist)):
        precom = 0
        prerbf = 0
        for j in range(len(pprvlist)):
            rbf = np.dot(pprv[j], pprnp[i]) / (np.linalg.norm(pprv[j]) * np.linalg.norm(pprnp[i]))
            if prerbf < rbf:
                prerbf = rbf
                precom = j
        com[precom].append(i)    

    return com

def compute_conductance(g, clusters):
    all_conductance = list()
    nodes = nx.nodes(g)
    for set in clusters:
        other_set = [i for i in nodes if i not in set]
        all_conductance.append(nx.conductance(g, set, other_set))
    return all_conductance

def cluster_conv(clusters, k):
    new_cluster = [[] for i in range(k)]
    # print(new_cluster)
    for i in range(len(clusters)):
        # print(i, clusters[i])
        new_cluster[clusters[i]].append(i)
    return new_cluster

def all_cos(g, com, ppr):
    # comは二重リスト
    pprnp = np.array(ppr)
    allcos = list()
    for eachcom in com:
        for nodei in eachcom:
            for nodej in eachcom:
                if nodei == nodej:
                    continue
                else:
                    cos = np.dot(pprnp[nodej], pprnp[nodei]) / (np.linalg.norm(pprnp[nodej]) * np.linalg.norm(pprnp[nodei]))
                    allcos.append(cos)
    return allcos

# これを使う N : 分割数, degree : 辞書型 全ノードの次数(?) networkx degree centrality, pprlist 全ノードからのPPR 関数あり pr : networkx の辞書型
def pprsim_community_v1(g, N, degree, pprlist, pr):
    # Spread Hubs x PR weighted PPR
    seed = Spread_Hubs_by_Degree(g, N, degree)
    pprcom = ppr_sim_clustering(g, pprlist, seed, N)
    pprsim_ppr_vList = PR_weight_PPR(g, pr, pprcom, pprlist, N)
    for i in range(300):
        nextpprcom = ppr_sim_clustering2(g, pprlist, pprsim_ppr_vList, N)
        if nextpprcom == pprcom:
            break
        pprcom = nextpprcom
        pprsim_ppr_vList = PR_weight_PPR(g, pr, pprcom, pprlist, N)
    return pprcom #[[0,1,2,3], [4, 5,6, 7]]

def pprsim_community_v2(g, N, degree, pprlist, pr):
    # random x PR weighted PPR
    pprcom = random_clustering(g, N)
    pprsim_ppr_vList = PR_weight_PPR(g, pr, pprcom, pprlist, N)
    for i in range(300):
        nextpprcom = ppr_sim_clustering2(g, pprlist, pprsim_ppr_vList, N)
        if nextpprcom == pprcom:
            break
        pprcom = nextpprcom
        pprsim_ppr_vList = PR_weight_PPR(g, pr, pprcom, pprlist, N)
    return pprcom

def pprsim_community_v3(g, N, degree, pprlist, pr):
    # Spread Hubs x means PPR
    seed = Spread_Hubs_by_Degree(g, N, degree)
    pprcom = ppr_sim_clustering(g, pprlist, seed, N)
    pprsim_ppr_vList = means_PPR(g, pprcom, pprlist, N)
    for i in range(300):
        nextpprcom = ppr_sim_clustering2(g, pprlist, pprsim_ppr_vList, N)
        if nextpprcom == pprcom:
            break
        pprcom = nextpprcom
        pprsim_ppr_vList = means_PPR(g, pprcom, pprlist, N)
    return pprcom

def pprsim_community_v4(g, N, degree, pprlist, pr):
    # random x means PPR
    pprcom = random_clustering(g, N)
    pprsim_ppr_vList = means_PPR(g, pprcom, pprlist, N)
    for i in range(300):
        nextpprcom = ppr_sim_clustering2(g, pprlist, pprsim_ppr_vList, N)
        if nextpprcom == pprcom:
            break
        pprcom = nextpprcom
        pprsim_ppr_vList = means_PPR(g, pprcom, pprlist, N)
    return pprcom

def appr_community(g, N, degree):
    seeds = Spread_Hubs_by_Degree(g, N, degree)
    apprcom = list()
    model = appr.APPR(g)
    for seed in seeds:
        community = model.compute_appr(seed_node = seed)
        apprcom.append(community)
    return apprcom

def comn(g, nd, com): # ndは必ずどこかのコミュニティに属するという前提に基づき, ndの属するコミュニティ番号を返す
    comi = 0
    for eachcom in com:
        if nd in eachcom:
            break
        comi = comi + 1
    return comi

def kyokai_or_not(g, nodei, com):
    adjnodes = nx.neighbors(g, nodei)
    comi = comn(g, nodei, com) # nodeiのコミュニティ番号
    # nodeiの隣接ノードが全てnodeiと同一コミュニティならfalse, 異なるコミュニティがあればtrueを返す
    for n in adjnodes:
        # nodeiと同じコミュニティを調べる, nodeiの隣接nが同じコミュニティになければ境界なのでtrueを返す
        if n not in com[comi]:
            return True
    return False    
        
def p_at_vb_by_ppr(nodei, ppr):
    # 重心PPRにおいて境界ノードの1つnodeiの割合(元から1正規化されているので値そのまま)
    # pprは計算された重心PPRのnodeiが属するコミュニティ成分
    p = ppr[nodei]
    return p

def p_ex_vb(g, nodei, com):
    adjnodes = nx.neighbors(g, nodei)
    degree = len(adjnodes) # nodei次数, nx関数より早そう
    number = 0
    for n in adjnodes:
        if comn(g, n, com) != comn(g, nodei, com):
            number = number + 1
    p = number / degree
    return p

def slipout_by_kyokai(g, N, pr, ppr, com, pprlist):
    p = [0] * N
    centroid_ppr = PR_weight_PPR(g, N, pr, com, pprlist)
    # centroid_ppr = means_PPR(g, com, pprlist, N)
    for eachcom in com:
        com_index = com.index(eachcom)
        for nodei in eachcom:
            if kyokai_or_not(g, nodei, com):
                p_kyokai = p_at_vb_by_ppr(nodei, centroid_ppr[com_index]) * p_ex_vb(g, nodei, com)
            else:
                p_kyokai = 0
            p[com_index] = p[com_index] + p_kyokai
    return p

def slipout_by_ppr(g, N, pr, com, pprlist):
    # 確率pはコミュニティごとに計算される
    # 単純に重心PPRにおけるコミュニティ外成分の和
    p = [0] * N
    centroid_ppr = PR_weight_PPR(g, pr, com, pprlist, N)
    # centroid_ppr = means_PPR(g, com, pprlist, N)
    for eachcom in com:
        com_index = com.index(eachcom)
        for nodei in range(len(nx.nodes(g))):
            if nodei not in eachcom:
                p[com_index] = p[com_index] + centroid_ppr[com_index][nodei]

    return p