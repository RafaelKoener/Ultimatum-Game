import matplotlib.pyplot as plt
from auxiliar import *
import numpy as np


if __name__ == "__main__":

    # for replicating G_size = 10000
    G_size = 100
    # G = nx.complete_graph(G_size)
    G = nx.barabasi_albert_graph(G_size,3)

    p = {k: random.random() for k in range(G_size)}
    q = {k: random.random() for k in range(G_size)}
    f = {k: 0 for k in range(G_size)}
    nx.set_node_attributes(G, p, 'p')
    nx.set_node_attributes(G, q, 'q')
    nx.set_node_attributes(G, f, 'f')
    to_plot = {}
    N = 100
    # for replicating time_steps = [1, 100, 1000, 10000, 20000]
    time_steps = [1, 10, 100, 500, 1000, 2000, 5000, 9999]
    for k in range(N*len(G)):
        print('------------------',k,'------------------')
        node_i = select_random_node(G)
        play_round(G, node_i)
        node_j = get_random_neighbor(G, node_i)
        print(node_i)
        print([n for n in G.neighbors(node_i)])
        print(k, nx.get_node_attributes(G, 'f'))
        fitness_i = get_fitness(G, node_i)
        fitness_j = get_fitness(G, node_j)
        if can_imitate(fitness_i, fitness_j, G.degree(node_i), G.degree(node_j)):
            imitate(G,node_i, node_j)
        print(average_p(G), average_q(G))  # ESTÃO MAIORES QUE 1!!!!!!
        if k%100==0:
            to_plot[k//10] = [average_p(G), average_q(G)]
        if k in time_steps:
            hist, bin_edges = np.histogram(list(nx.get_node_attributes(G, 'p').values()), bins=20, range=(0, 1))
            plt.plot(bin_edges[1:], hist, '-o')
            plt.title('timestep'+str(k))
            plt.show()

    plot_p = [v[0] for v in to_plot.values()]
    plot_q = [v[1] for v in to_plot.values()]

    f, (ax1, ax2) = plt.subplots(1,2, sharey=True, figsize=(20,7))
    ax1.plot(list(to_plot.keys()), plot_p, c='b', label='average p value')
    ax1.plot(list(to_plot.keys()), plot_q, c='r', label='average q value')
    ax1.set_xlabel('time' )
    ax1.set_ylabel('p and q values')
    ax1.set_title('p and q values evolution')
    ax1.legend()

    ax2.loglog(list(to_plot.keys()), plot_p, c='b', label='average p value')
    ax2.loglog(list(to_plot.keys()), plot_q, c='r', label='average q value')
    ax2.set_xlabel('time' )
    ax2.set_ylabel('p and q values')
    ax2.set_title('p and q values evolution loglog')
    ax2.legend()
    plt.show()