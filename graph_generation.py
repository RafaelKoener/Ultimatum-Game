import networkx as nx
import random
import numpy as np

def generate_graph(size, p, q, graph_type):
    if graph_type == 'barabasi':
        G = nx.barabasi_albert_graph(size, 3)
    elif graph_type == 'erdos':
        G = nx.erdos_renyi_graph(size, 0.5)

    f = {k: 0 for k in range(size)}

    nx.set_node_attributes(G, p, 'p')
    nx.set_node_attributes(G, q, 'q')
    nx.set_node_attributes(G, f, 'f')
    return G

def get_p_q(size, strategy):
    values = [0, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65,
            0.7, 0.75, 0.8, 0.85, 0.9, 0.95, 1]
    p_values = [values[0] for _ in range(int(0.025*size))]
    for val in values[1:20]:
        for _ in range(int(0.05*size)):
            p_values.append(val)
    for _ in range(int(0.025*size)):
        p_values.append(values[-1])
    q_values = p_values.copy()

    if strategy == 'ipq': # independent p and q
        random.shuffle(p_values)
        random.shuffle(q_values)
        p = {k: p_values[k] for k in range(size)}
        q = {k: q_values[k] for k in range(size)}
        return p, q
    elif strategy == 'pq': # p=q
        random.shuffle(p_values)
        p = {k: p_values[k] for k in range(size)}
        q = {k: p_values[k] for k in range(size)}
        return p, q
    elif strategy == 'pq1': # p=1-q
        random.shuffle(q_values)
        q = {k: q_values[k] for k in range(size)}
        p = {k: 1-q_values[k] for k in q}
        return p, q
    elif strategy == 'mixed':
        p = {}
        q = {}
        choices = ['ipq', 'pq', 'pq1']
        random.shuffle(p_values)
        random.shuffle(q_values)
        for k in range(size):
            choice = np.random.choice(choices, p=[1/3,1/3,1/3])
            if choice == 'ipq':
                p[k] = p_values[k]
                q[k] = q_values[k]
            elif choice == 'pq':
                p[k] = p_values[k]
                q[k] = p_values[k]
            elif choice == 'pq1':
                q[k] = p_values[k]
                p[k] = 1 - q[k]
        return p,q

def reset_G(G, size, p, q):
    f = {k: 0 for k in range(size)}
    nx.set_node_attributes(G, p, 'p')
    nx.set_node_attributes(G, q, 'q')
    nx.set_node_attributes(G, f, 'f')
