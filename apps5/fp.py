from collections import deque
import networkx as nx
import time


class ETA:
    def __init__(self):
        self.start = time.time()

    def eta(self, frac_done: float):
        """_summary_

        Args:
            frac_done float: % tasks already done in [0, 1]
        """
        return round(self.total_time() / frac_done * (1-frac_done), 3)

    def total_time(self):
        return time.time() - self.start


def forward_push(g: nx.DiGraph, src: int, alpha=0.85, eps=10**-6) -> dict:
    residue = {nd: 0 for nd in g}  # 残余
    reserve = {nd: 0 for nd in g}  # 確定値
    residue[src] = 1  # 初期値
    q = deque([src])
    while q:
        nd = q.popleft()
        deg_w = g.out_degree(nd)
        reserve[nd] += residue[nd] * (1 - alpha)
        if (deg_w == 0):
            residue[src] += residue[nd] * alpha
            residue[nd] = 0
            continue
        push_val = residue[nd] * alpha
        residue[nd] = 0
        for nbr in g.successors(nd):
            nbr_val_old = residue[nbr]
            residue[nbr] += push_val / deg_w
            if nbr_val_old <= eps * g.out_degree(nbr) < residue[nbr]:
                q.append(nbr)
    # 正規化
    sum_reserve = sum(reserve.values())
    for nd in reserve.keys():
        reserve[nd] /= sum_reserve
    return reserve


def PPRs(G: nx.DiGraph):  # 関数 MC の代わり
    ALPHA = 0.85
    EPS = 10 ** -6
    nd2pprs = {}  # ppr_matome のこと
    percent = len(G) / 100
    percent_done = 1
    eta = ETA()
    for cnt, src in enumerate(G, 1):
        ppr = forward_push(G, src, ALPHA, EPS)
        nd2pprs[src] = ppr
        if cnt / percent >= percent_done:
            print(
                f'Completed: {percent_done}%',
                f'ETA: {round(eta.eta(cnt / len(G)), 1)}s',
                sep=', '
            )
            percent_done += 1
    return nd2pprs


def read_digraph(path: str, weighted=True) -> nx.DiGraph:
    f = open(path)
    DiG = nx.DiGraph()
    for line in f.readlines():
        if "#" in line:
            continue
        values = line.split()
        if len(values) == 2:
            u, v = map(int, line.split())
            DiG.add_edge(u, v)
        if len(values) == 3:
            u, v = int(values[0]), int(values[1])
            w = float(values[2]) if weighted else 1
            DiG.add_edge(u, v, weight=w)
    return DiG


if __name__ == "__main__":
    G = read_digraph("clickstream_weighted_edges.tsv", weighted=False)
    ppr_matome = PPRs(G)
