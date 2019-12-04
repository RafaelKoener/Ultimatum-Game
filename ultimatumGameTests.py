import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from auxiliar import *
import numpy as np
import math
from graph_generation import *
# file only used for testing and generating graphics for the report
if __name__ == "__main__":
    plt.ioff()
    G_size = 10000
    N = 10
    n_runs = 1
    time_steps = [0, 9999, 19999, 29999, 39999, 49999, 99999]
    time_steps_original = [0, 99, 999, 4999, 9999, 19999]
    colors = ['b', 'r', 'g', 'm', 'black', 'c', 'orange']
    colors_original = ['b', 'r', 'g', 'y', 'm', 'black']
    markers = ['o-', 's-', '^-', '*-', 'v-', 'p-', 'd-']
    markers_original = ['o-', 's-', '^-', 'v-', '*-', 'd-']
    plot_x = [0, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95, 1]
####################################################### pq1 erdos ######################################################
    sp_pq1_e_strategy = 'pq1'  # independent p and q: ipq, p=q: pq, p=q-1: pq1, mixed: mixed
    sp_pq1_e_graph_type = 'erdos'  # scale free graph: barabasi ; erdos-renyi graph: erdos
    sp_pq1_e_p, sp_pq1_e_q = get_p_q(G_size, sp_pq1_e_strategy)
    sp_pq1_e_G = generate_graph(G_size, sp_pq1_e_p, sp_pq1_e_q, sp_pq1_e_graph_type)
    sp_pq1_e_to_plot = {}
    sp_pq1_e_to_plot_imitate = {}
    sp_pq1_e_runs_p = {k: [] for k in range(n_runs)}
    sp_pq1_e_runs_q = {k: [] for k in range(n_runs)}
    sp_pq1_e_runs_p_original = {k: [] for k in range(n_runs)}
    sp_pq1_e_runs_q_original = {k: [] for k in range(n_runs)}
    for run in range(n_runs):
        reset_G(sp_pq1_e_G, G_size, sp_pq1_e_p, sp_pq1_e_q)
        print('------------------ sp_pq1_e', run, "------------------")
        for k in range(N * len(sp_pq1_e_G)):
            sp_pq1_e_node_i = select_random_node(sp_pq1_e_G)
            play_round(sp_pq1_e_G, sp_pq1_e_node_i)
            social_penalty(sp_pq1_e_G, sp_pq1_e_strategy)
            if k in time_steps:
                sp_pq1_e_ind = time_steps.index(k)
                sp_pq1_e_hist_p, sp_pq1_e_bin_edges = np.histogram(
                    list(nx.get_node_attributes(sp_pq1_e_G, 'p').values()), bins=21)
                sp_pq1_e_hist_q, sp_pq1_e_bin_edges = np.histogram(
                    list(nx.get_node_attributes(sp_pq1_e_G, 'q').values()), bins=21)
                sp_pq1_e_runs_p[run].append(sp_pq1_e_hist_p)
                sp_pq1_e_runs_q[run].append(sp_pq1_e_hist_q)
            if k in time_steps_original:
                sp_pq1_e_ind_original = time_steps_original.index(k)
                sp_pq1_e_hist_p_original, sp_pq1_e_bin_edges_original = np.histogram(
                    list(nx.get_node_attributes(sp_pq1_e_G, 'p').values()), bins=21)
                sp_pq1_e_hist_q_original, sp_pq1_e_bin_edges_original = np.histogram(
                    list(nx.get_node_attributes(sp_pq1_e_G, 'q').values()), bins=21)
                sp_pq1_e_runs_p_original[run].append(sp_pq1_e_hist_p_original)
                sp_pq1_e_runs_q_original[run].append(sp_pq1_e_hist_q_original)

    plt.figure()
    for i in range(len(time_steps)):
        for k in sp_pq1_e_runs_p:
            try:
                sp_pq1_e_avg_hist_arrays_p = [sp_pq1_e_runs_p[k][i] for k in sp_pq1_e_runs_p]
                sp_pq1_e_avg_hist_p = [np.mean(k) for k in zip(*sp_pq1_e_avg_hist_arrays_p)]
            except:
                continue
        plt.plot(plot_x, sp_pq1_e_avg_hist_p, markers[i], c=colors[i], label="t=" + str(time_steps[i] + 1))
    p, q = get_p_q(G_size, sp_pq1_e_strategy)
    plt.gca().tick_params(direction='in')
    plt.xlim([0, 1])
    plt.ylim([0, max(sp_pq1_e_avg_hist_p) * 1.1])
    plt.xlabel('p')
    plt.ylabel('D(p)')
    plt.legend()
    plt.savefig('img/sp_pq1_e_p.pdf')
    plt.figure()
    for j in range(len(time_steps)):
        for k in sp_pq1_e_runs_q:
            try:
                sp_pq1_e_avg_hist_arrays_q = [sp_pq1_e_runs_q[k][j] for k in sp_pq1_e_runs_q]
                sp_pq1_e_avg_hist_q = [np.mean(k) for k in zip(*sp_pq1_e_avg_hist_arrays_q)]
            except:
                continue
        plt.plot(plot_x, sp_pq1_e_avg_hist_q, markers[j], c=colors[j], label="t=" + str(time_steps[j] + 1))
    plt.gca().tick_params(direction='in')
    plt.xlim([0, 1])
    plt.ylim([0, max(sp_pq1_e_avg_hist_q) * 1.1])
    plt.xlabel('q')
    plt.ylabel('D(q)')
    plt.legend()
    plt.savefig('img/sp_pq1_e_q.pdf')
    plt.figure()
    for i in range(len(time_steps_original)):
        for k in sp_pq1_e_runs_p_original:
            try:
                sp_pq1_e_avg_hist_arrays_p_original = [sp_pq1_e_runs_p_original[k][i] for k in sp_pq1_e_runs_p_original]
                sp_pq1_e_avg_hist_p_original = [np.mean(k) for k in zip(*sp_pq1_e_avg_hist_arrays_p_original)]
            except:
                continue
        plt.plot(plot_x, sp_pq1_e_avg_hist_p_original, markers_original[i], c=colors_original[i],
                 label="t=" + str(time_steps_original[i] + 1))
    p, q = get_p_q(G_size, sp_pq1_e_strategy)
    plt.gca().tick_params(direction='in')
    plt.xlim([0, 1])
    plt.ylim([0, max(sp_pq1_e_avg_hist_p_original) * 1.1])
    plt.xlabel('p')
    plt.ylabel('D(p)')
    plt.legend()
    plt.savefig('img/sp_pq1_e_p_o.pdf')
    plt.figure()
    for j in range(len(time_steps_original)):
        for k in sp_pq1_e_runs_q_original:
            try:
                sp_pq1_e_avg_hist_arrays_q_original = [sp_pq1_e_runs_q_original[k][j] for k in sp_pq1_e_runs_q_original]
                sp_pq1_e_avg_hist_q_original = [np.mean(k) for k in zip(*sp_pq1_e_avg_hist_arrays_q_original)]
            except:
                continue
        plt.plot(plot_x, sp_pq1_e_avg_hist_q_original, markers_original[j], c=colors_original[j],
                 label="t=" + str(time_steps_original[j] + 1))
    plt.gca().tick_params(direction='in')
    plt.xlim([0, 1])
    plt.ylim([0, max(sp_pq1_e_avg_hist_q_original) * 1.1])
    plt.xlabel('q')
    plt.ylabel('D(q)')
    plt.legend()
    plt.savefig('img/sp_pq1_e_q_o.pdf')