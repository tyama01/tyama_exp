import random

class Node():
    def __init__(self, id):
        self.id = id
        self.adj = dict()
        self.degree = 0
        self.in_push_queue = False

    def __repr__(self):
        return str(self.id)

    def __str__(self):
        return str(self.id)

    def __eq__(self, other):
        return self.id == other.id

    def add_edge(self, node):
        self.adj[node.id] = node
        self.update_degree()
        return

    def del_edge(self, adj_node):
        del self.adj[adj_node.id]
        self.update_degree()
        return
    
    def update_degree(self):
        self.degree = len(self.adj)
        return

    def get_random_adjacent(self):
        if self.degree == 0:
            return self
        else:
            return random.choice(list(self.adj.values()))