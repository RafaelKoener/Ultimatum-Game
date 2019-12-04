import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from auxiliar import *
import numpy as np
import math
from graph_generation import *

if __name__ == "__main__":

    G_size = 10000
    strategy = 'ipq'  # independent p and q: ipq, p=q: pq, p=q-1: pq1, mixed: mixed
    plt.ioff()
    graph_type = 'barabasi'  # scale free graph: barabasi ; erdos-renyi graph: erdos
    p, q = get_p_q(G_size, strategy)
    G = generate_graph(G_size, p, q, graph_type)
    to_plot = {}
    to_plot_imitate = {}
    N = 2
    n_runs = 1

    time_steps = [0,  9999, 19999, 29999, 39999, 49999, 99999]
    # time_steps = [0, 99, 999, 4999, 9999, 19999]
    colors = ['b', 'r', 'g', 'm', 'black', 'c', 'orange']
    markers = ['o-', 's-', '^-', '*-', 'v-', 'p-', 'd-']
    runs_p = {k: [] for k in range(n_runs)}
    runs_q = {k: [] for k in range(n_runs)}
    for run in range(n_runs):
        reset_G(G, G_size, p, q)
        for k in range(N * len(G)):
            print('------------------', run, k, "------------------")
            node_i = select_random_node(G)
            play_round(G, node_i)
            # for natural selection
            node_j = get_random_neighbor(G, node_i)
            fitness_i = get_fitness(G, node_i)
            fitness_j = get_fitness(G, node_j)
            decision, delta_f, prob = can_imitate(fitness_i, fitness_j, G.degree(node_i), G.degree(node_j))
            to_plot_imitate[k] = [delta_f] + [prob]
            if decision:
                imitate(G, node_i, node_j)
            # for social penalty
            # social_penalty(G, strategy)
            if k % 100 == 0:
                # used to plot average p and q
                to_plot[k // 10] = [average_p(G), average_q(G)]
            if k in time_steps:
                ind = time_steps.index(k)
                hist_p, bin_edges = np.histogram(list(nx.get_node_attributes(G, 'p').values()), bins=21)
                hist_q, bin_edges = np.histogram(list(nx.get_node_attributes(G, 'q').values()), bins=21)
                runs_p[run].append(hist_p)
                runs_q[run].append(hist_q)
                print(list(nx.get_node_attributes(G, 'p').values()))
                # plot individual runs
                # plt.plot(bin_edges[1:], hist, markers[ind], c=colors[ind], label="t="+str(k+1))
        # plt.title('P values distribution for run '+ str(run))
        # plt.legend()
        # plt.show()

    # plot average results for p values
    plot_x = [0, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65,
              0.7, 0.75, 0.8, 0.85, 0.9, 0.95, 1]
    print(plot_x)
    print(bin_edges)
    plt.figure()
    for i in range(len(time_steps)):
        for k in runs_p:
            try:
                avg_hist_arrays_p = [runs_p[k][i] for k in runs_p]
                avg_hist_p = [np.mean(k) for k in zip(*avg_hist_arrays_p)]
            except:
                continue
        plt.plot(plot_x, avg_hist_p, markers[i], c=colors[i], label="t=" + str(time_steps[i] + 1))
    p, q = get_p_q(G_size, strategy)
    plt.gca().tick_params(direction='in')
    plt.xlim([0, 1])
    # plt.ylim([0, max(avg_hist_p) * 1.1])
    plt.xlabel('p')
    plt.ylabel('D(p)')
    plt.legend()
    plt.savefig("img/1.png")
    # plt.show()

    # plot average results for q values
    plt.figure()
    for j in range(len(time_steps)):
        for k in runs_q:
            try:
                avg_hist_arrays_q = [runs_q[k][j] for k in runs_q]
                avg_hist_q = [np.mean(k) for k in zip(*avg_hist_arrays_q)]
            except:
                continue
        plt.plot(plot_x, avg_hist_q, markers[j], c=colors[j], label="t=" + str(time_steps[j] + 1))
    plt.gca().tick_params(direction='in')
    plt.xlim([0, 1])
    plt.ylim([0, max(avg_hist_q) * 1.1])
    plt.xlabel('q')
    plt.ylabel('D(q)')
    plt.legend()
    plt.savefig("img/2.png")
    # plt.show()


"""
plot probability to imitate
plt.plot(sorted([to_plot_imitate[k][0] for k in to_plot_imitate]),
             sorted([to_plot_imitate[k][1] for k in to_plot_imitate]))
    plt.gca().tick_params(direction='in')
    # plt.ylim([0, 1])
    plt.title('Probability of imitating neighbour strategy')
    plt.xlabel('difference in fitness')
    plt.ylabel('Probability')
    plt.show()
    
plot average p/q with different errors
E = [0.001, 0.002, 0.003, 0.004,0.005, 0.007, 0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.1, 0.15, 0.2]
N = 100
    P = []
    Q = []
    for i in E:
        for k in range(N*len(G)):
            node_i = select_random_node(G)
            play_round(G, node_i)
            node_j = get_random_neighbor(G, node_i)
            fitness_i = get_fitness(G, node_i)
            fitness_j = get_fitness(G, node_j)
            if fitness_j > fitness_i:
                imitate(G, node_i, node_j, i)
        P.append(average_p(G))
        Q.append(average_q(G))
    print('P', P)
    print('Q', Q)
    plt.plot(E, P, label="Average P")
    plt.plot(E, Q, label="Average Q")
    plt.legend()
    plt.show()
    plt.close()

# plotting average p and q is not of interest
    plot_p = [v[0] for v in to_plot.values()]
    plot_q = [v[1] for v in to_plot.values()]

    fig, (ax1, ax2) = plt.subplots(1,2, figsize=(20,7))
    ax1.plot(list(to_plot.keys()), plot_p, c='g', label='average p value')
    ax1.plot(list(to_plot.keys()), plot_q, c='r', label='average q value')
    ax1.set_ylim(0,1)
    ax1.yaxis.set_major_locator(ticker.MultipleLocator(0.1))
    ax1.set_xlabel('time')
    ax1.set_ylabel('p and q values')
    ax1.set_title('p and q values evolution')
    ax1.legend()

    ax2.loglog(list(to_plot.keys()), plot_p, c='g', label='average p value')
    ax2.loglog(list(to_plot.keys()), plot_q, c='r', label='average q value')
    ax2.yaxis.set_major_locator(ticker.MultipleLocator(0.1))
    ax2.set_xlabel('time')
    ax2.set_ylabel('p and q values')
    ax2.set_title('p and q values evolution in loglog scale')
    ax2.legend()
    plt.show()

"""
