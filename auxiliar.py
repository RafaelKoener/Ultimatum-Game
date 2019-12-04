import networkx as nx
import random
import numpy as np
import math
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors


def average_p(G):
    G_p = nx.get_node_attributes(G, 'p')
    return sum(G_p.values()) / len(G_p)


def average_q(G):
    G_q = nx.get_node_attributes(G, 'q')
    return sum(G_q.values()) / len(G_q)


def select_random_node(G):
    return random.choice(list(G.nodes))


def get_random_neighbor(G, node):
    neighbors = [n for n in G.neighbors(node)]
    if neighbors == []:
        return node
    else:
        return random.choice(neighbors)


def play_with(G, node, neighbor):
    if G.nodes[node]['p'] > G.nodes[neighbor]['q']:
        G.nodes[node]['f'] += 1 - G.nodes[node]['p']
        G.nodes[neighbor]['f'] += G.nodes[node]['p']


def play_round(G, node):
    neighbors = [n for n in G.neighbors(node)]
    for n in neighbors:
        play_with(G, node, n)
        play_with(G, n, node)


def get_fitness(G, node):
    return G.nodes[node]['f']


def imitate(G, node, model, E=0.1):
    error_p = random.random() * (2 * E)
    error_q = random.random() * (2 * E)
    G.nodes[node]['p'] = G.nodes[model]['p'] + (error_p - E)
    G.nodes[node]['q'] = G.nodes[model]['q'] + (error_q - E)

    if G.nodes[node]['p'] > 1:
        G.nodes[node]['p'] = 1
    if G.nodes[node]['q'] > 1:
        G.nodes[node]['q'] = 1
    if G.nodes[node]['p'] < 0:
        G.nodes[node]['p'] = 0
    if G.nodes[node]['q'] < 0:
        G.nodes[node]['q'] = 0


def can_imitate(f_i, f_j, d_i, d_j):
    p_imitate = 0
    if f_j > f_i:
        p_imitate = (f_j - f_i) / (2 * max(d_i, d_j))
        if p_imitate > 1:
            p_imitate = 1
        if p_imitate < 0:
            p_imitate = 0
        choice = np.random.choice([True, False], p=[p_imitate, 1 - p_imitate])
        return choice, f_j - f_i, p_imitate
    return False, f_j - f_i, p_imitate

def social_penalty(G, strategy):
    nodes = nx.get_node_attributes(G, 'f')
    node_min = min(nodes, key=nodes.get)
    neighbors = G.neighbors(node_min)
    l = [n for n in neighbors]
    l.append(node_min)
    if strategy == 'ipq':
        for i in l:
            G.nodes[i]['p'] = random.random()
            G.nodes[i]['q'] = random.random()
            G.nodes[i]['f'] = 0
    elif strategy == 'pq':
        for i in l:
            G.nodes[i]['p'] = random.random()
            G.nodes[i]['q'] = G.nodes[i]['p']
            G.nodes[i]['f'] = 0
    elif strategy == 'pq1':
        for i in l:
            G.nodes[i]['q'] = random.random()
            G.nodes[i]['p'] = 1 - G.nodes[i]['q']
            G.nodes[i]['f'] = 0

def draw_centrality(G):
    layout = nx.spring_layout(G)
    centrality = nx.eigenvector_centrality(G)
    nodes = nx.draw_networkx_nodes(G, layout, node_size=10, cmap=plt.cm.plasma, node_color=list(centrality.values()), nodelist=list(centrality.keys()))
    nodes.set_norm(mcolors.SymLogNorm(linthresh=0.01, linscale=1))

    
    # labels = nx.draw_networkx_labels(G, layout)
    edges = nx.draw_networkx_edges(G, layout)

    plt.title('Degree Centrality')
    plt.colorbar(nodes)
    plt.axis('off')
    plt.show()
