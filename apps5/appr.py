import networkx as nx
from collections import deque, defaultdict
import time

INF = float('inf')

class APPR:
    def __init__(self, g: nx.Graph):
        self._g = g
        self._weights = {}
        self._total_vol = 0
        self._cnt = 0
        self._duration1 = 0
        self._duration2 = 0
        self._duration3 = 0
        self._appr_vec = defaultdict(float)
        self._node_in_order = []
        self._cond_profile = []
        self._size_global_min = 0
        self._size_first_local_min = -1

        # To store the number of motif instances on each edge.
        # vec = Counts[u].GetDat(v) are the numbers of instances of several motif types on edge (u, v)
        # For undirected graph, vec[i] is the number of (i+3)-cliques on this edge, i.e., vec[0] is for triangle
        # For directed graph motif,
        #    vec[0] is for uni-directed edges,
        #    vec[1] is for bi-directed edges,
        #    vec[i] is for M_{i-1} as defined in Austin et al. (Science 2016).
        self._counts = {}
        self._delete_self_edges()
        self._create_weights()
        # seed_node = 355935
        # print("first 0:", seed_node in g)
        # print("first 1:", seed_node in self._weights)
        # print("first 2:", self._weights[seed_node])
        # print("first 3:", seed_node in self._weights[seed_node])

    def top_appr(self):
        for i, v in enumerate(self._cond_profile):
            if v <= 0:
                return self._node_in_order[:i]
            return self._node_in_order

    def compute_appr(self, seed_node, alpha=0.85, eps=0.0001, total_vol=None, original=True):
        start_a = time.time() 
        self._appr_vec = defaultdict(float)
        self._node_in_order = []
        self._cond_profile = []
        self._size_global_min = 0
        self._size_first_local_min = -1
        residual = defaultdict(float)
        num_pushes = 0
        appr_norm = 0
        weights = self._weights
        if weights[seed_node][seed_node] * eps >= 1:
            self._appr_vec[seed_node] = 0
            return []
        residual[seed_node] = 1
        q = deque()
        q.append(seed_node)

        # PPR by Anderson
        while(q):
            num_pushes += 1
            nd = q.popleft()
            # print(nd)

            deg_w = weights[nd][nd]
            # print(nd, "deg_w", deg_w)
            if (deg_w == 0):
                self._appr_vec[nd] += residual[nd]
                appr_norm += residual[nd]
                residual[nd] = 0
                continue
            push_val = residual[nd] - deg_w * eps / 2
            self._appr_vec[nd] += push_val * (1 - alpha)
            appr_norm += push_val * (1 - alpha)
            residual[nd] = deg_w * eps / 2

            push_val *= alpha/deg_w
            for nbr in self._g.neighbors(nd):
                nbr_val_old = residual[nbr]
                nbr_val_new = nbr_val_old + push_val * weights[nd][nbr]
                residual[nbr] = nbr_val_new
                if (nbr_val_old <= eps * weights[nbr][nbr] and nbr_val_new > eps * weights[nbr][nbr]):
                    q.append(nbr)
        # print(residual)
        # print()
        # print(self._appr_vec)
        end_a = time.time()  
        time_diff_a = end_a - start_a  # 処理完了後の時刻から処理開始前の時刻を減算する
        # print('appr ' + str(time_diff_a) + ' sec') #
        if total_vol:
            self._compute_profile(total_vol)
        else:
            self._compute_profile(self._total_vol)

        cluster = self._node_in_order[:self._size_global_min + 1]

        if original:
            return cluster
        return self._single_node_cut(self._g, cluster, seed_node)

    def _single_node_cut(self, g: nx.Graph, cluster: list, s: int) -> list:
        assert g.has_node(s)
        sub = g.subgraph(cluster)
        inside = set([s] + [nd for nd in sub.neighbors(s)])
        reach = set()
        q = deque([nd for nd in sub.neighbors(s)])
        while q:
            nd = q.popleft()
            for nbr in sub.neighbors(nd):
                if nbr in inside:
                    continue
                if nbr in reach:
                    reach.remove(nbr)
                    inside.add(nbr)
                    q.append(nbr)
                    continue
                # we first meet this not
                reach.add(nbr)
        res = []
        for nd in cluster:
            if nd in inside:
                res.append(nd)
        return res

    def get_total_vol(self):
        return self._total_vol

    def get_graph(self):
        return self._g

    def _create_weights(self):
        for nd in self._g.nodes():
            deg_w = 0
            self._weights[nd] = {}
            for nbr in self._g.neighbors(nd):
                edge_data = self._g.get_edge_data(nd, nbr)
                if 'weight' in edge_data:
                    w = edge_data['weight']
                else:
                    w = 1
                self._weights[nd][nbr] = w
                deg_w += w
            self._weights[nd][nd] = deg_w
            self._total_vol += deg_w

    def _compute_profile(self, total_vol):
        quotient = []
        weights = self._weights

        # D^-1 * p
        for nd, val in self._appr_vec.items():
            if weights[nd][nd] == 0:
                quotient.append((nd, INF))
            else:
                quotient.append((nd, val / weights[nd][nd]))
        quotient.sort(key=lambda x: x[1], reverse=True)

        vol, cut = 0, 0
        is_in = set()
        vol_small = 1  # = 1 if volume(IsIn) <= VolAll/2, and = -1 otherwise;

        for nd, val in quotient:
            weights_here = self._weights[nd]
            self._node_in_order.append(nd)
            is_in.add(nd)
            vol += vol_small * weights_here[nd]

            if vol_small == 1 and vol >= total_vol / 2:
                vol = total_vol - vol
                vol_small = -1

            cut += weights_here[nd]
            for nbr in self._g.neighbors(nd):
                if nbr in is_in:
                    cut -= 2 * weights_here[nbr]
            if vol:
                self._cond_profile.append(cut / vol)
            else:
                self._cond_profile.append(1)
        self._find_global_min()
        self._find_first_local_min()
        # print("global min:", self._size_global_min)
        # print("first local min:", self._size_first_local_min)
        # print(self._node_in_order[:self._size_global_min])

    def _find_global_min(self):
        min_cond_val = 2
        for i, m in enumerate(self._cond_profile):
            if (m < min_cond_val):
                self._size_global_min = i + 1
                min_cond_val = m

    def _find_first_local_min(self):
        self._size_first_local_min = 2
        while(self._size_first_local_min < len(self._cond_profile)):
            if self._is_local_min(self._size_first_local_min - 1):
                break
            self._size_first_local_min += 1
        if self._size_first_local_min >= len(self._cond_profile):
            if self._size_global_min == 0:
                self._find_global_min()
            self._size_first_local_min = self._size_global_min

    def _is_local_min(self, idx, thresh=1.2):
        if idx <= 0 or idx >= len(self._cond_profile) - 1:
            return False
        if (self._cond_profile[idx] >= self._cond_profile[idx - 1]):
            return False
        idx_right = idx
        while idx_right < len(self._cond_profile) - 1:
            idx_right += 1
            if self._cond_profile[idx_right] > self._cond_profile[idx] * thresh:
                return True
            elif self._cond_profile[idx_right] <= self._cond_profile[idx]:
                return False

        return False

    def _delete_self_edges(self):
        for nd in self._g.nodes:
            if self._g.has_edge(nd, nd):
                self._g.remove_edge(nd, nd)