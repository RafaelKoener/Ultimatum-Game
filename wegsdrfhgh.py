ns_ipq_b_strategy = 'ipq'  # independent p and q: ipq, p=q: pq, p=q-1: pq1, mixed: mixed
ns_ipq_b_graph_type = 'barabasi'  # scale free graph: barabasi ; erdos-renyi graph: erdos
ns_ipq_b_p,ns_ipq_b_q = get_p_q(G_size, ns_ipq_b_strategy)
ns_ipq_b_G = generate_graph(G_size, ns_ipq_b_p, ns_ipq_b_q, ns_ipq_b_graph_type)
ns_ipq_b_to_plot = {}
ns_ipq_b_to_plot_imitate = {}
ns_ipq_b_runs_p = {k: [] for k in range(n_runs)}
ns_ipq_b_runs_q = {k: [] for k in range(n_runs)}
ns_ipq_b_runs_p_original = {k: [] for k in range(n_runs)}
ns_ipq_b_runs_q_original = {k: [] for k in range(n_runs)}
for run in range(n_runs):
    reset_G(ns_ipq_b_G, G_size, ns_ipq_b_p, ns_ipq_b_q)
    print('------------------ ns_ipq_b', run, "------------------")
    for k in range(N * len(ns_ipq_b_G)):
        ns_ipq_b_node_i = select_random_node(ns_ipq_b_G)
        play_round(ns_ipq_b_G, ns_ipq_b_node_i)
        ns_ipq_b_node_j = get_random_neighbor(ns_ipq_b_G, ns_ipq_b_node_i)
        ns_ipq_b_fitness_i = get_fitness(ns_ipq_b_G, ns_ipq_b_node_i)
        ns_ipq_b_fitness_j = get_fitness(ns_ipq_b_G, ns_ipq_b_node_j)
        ns_ipq_b_decision, ns_ipq_b_delta_f, ns_ipq_b_prob = can_imitate(ns_ipq_b_fitness_i, ns_ipq_b_fitness_j, ns_ipq_b_G.degree(ns_ipq_b_node_i), ns_ipq_b_G.degree(ns_ipq_b_node_j))
        ns_ipq_b_to_plot_imitate[k] = [ns_ipq_b_delta_f] + [ns_ipq_b_prob]
        if ns_ipq_b_decision:
            imitate(ns_ipq_b_G, ns_ipq_b_node_i, ns_ipq_b_node_j)
        if k in time_steps:
            ns_ipq_b_ind = time_steps.index(k)
            ns_ipq_b_hist_p, ns_ipq_b_bin_edges = np.histogram(list(nx.get_node_attributes(ns_ipq_b_G, 'p').values()), bins=21)
            ns_ipq_b_hist_q, ns_ipq_b_bin_edges = np.histogram(list(nx.get_node_attributes(ns_ipq_b_G, 'q').values()), bins=21)
            ns_ipq_b_runs_p[run].append(ns_ipq_b_hist_p)
            ns_ipq_b_runs_q[run].append(ns_ipq_b_hist_q)
        if k in time_steps_original:
            ns_ipq_b_ind_original = time_steps_original.index(k)
            ns_ipq_b_hist_p_original, ns_ipq_b_bin_edges_original = np.histogram(list(nx.get_node_attributes(ns_ipq_b_G, 'p').values()), bins=21)
            ns_ipq_b_hist_q_original, ns_ipq_b_bin_edges_original = np.histogram(list(nx.get_node_attributes(ns_ipq_b_G, 'q').values()), bins=21)
            ns_ipq_b_runs_p_original[run].append(ns_ipq_b_hist_p_original)
            ns_ipq_b_runs_q_original[run].append(ns_ipq_b_hist_q_original)

plt.figure()
for i in range(len(time_steps)):
    for k in ns_ipq_b_runs_p:
        try:
            ns_ipq_b_avg_hist_arrays_p = [ns_ipq_b_runs_p[k][i] for k in ns_ipq_b_runs_p]
            ns_ipq_b_avg_hist_p = [np.mean(k) for k in zip(*ns_ipq_b_avg_hist_arrays_p)]
        except:
            continue
    plt.plot(plot_x, ns_ipq_b_avg_hist_p, markers[i], c=colors[i], label="t=" + str(time_steps[i] + 1))
p, q = get_p_q(G_size, ns_ipq_b_strategy)
plt.gca().tick_params(direction='in')
plt.xlim([0, 1])
plt.ylim([0, max(ns_ipq_b_avg_hist_p) * 1.1])
plt.xlabel('p')
plt.ylabel('D(p)')
plt.legend()
plt.savefig('img/ns_ipq_b_p.png', dpi=300)
plt.figure()
for j in range(len(time_steps)):
    for k in ns_ipq_b_runs_q:
        try:
            ns_ipq_b_avg_hist_arrays_q = [ns_ipq_b_runs_q[k][j] for k in ns_ipq_b_runs_q]
            ns_ipq_b_avg_hist_q = [np.mean(k) for k in zip(*ns_ipq_b_avg_hist_arrays_q)]
        except:
            continue
    plt.plot(plot_x, ns_ipq_b_avg_hist_q, markers[j], c=colors[j], label="t=" + str(time_steps[j] + 1))
plt.gca().tick_params(direction='in')
plt.xlim([0, 1])
plt.ylim([0, max(ns_ipq_b_avg_hist_q) * 1.1])
plt.xlabel('q')
plt.ylabel('D(q)')
plt.legend()
plt.savefig('img/ns_ipq_b_q.png', dpi=300)
plt.figure()
for i in range(len(time_steps_original)):
    for k in ns_ipq_b_runs_p_original:
        try:
            ns_ipq_b_avg_hist_arrays_p_original = [ns_ipq_b_runs_p_original[k][i] for k in ns_ipq_b_runs_p_original]
            ns_ipq_b_avg_hist_p_original = [np.mean(k) for k in zip(*ns_ipq_b_avg_hist_arrays_p_original)]
        except:
            continue
    plt.plot(plot_x, ns_ipq_b_avg_hist_p_original, markers_original[i], c=colors_original[i], label="t=" + str(time_steps_original[i] + 1))
p, q = get_p_q(G_size, ns_ipq_b_strategy)
plt.gca().tick_params(direction='in')
plt.xlim([0, 1])
plt.ylim([0, max(ns_ipq_b_avg_hist_p_original) * 1.1])
plt.xlabel('p')
plt.ylabel('D(p)')
plt.legend()
plt.savefig('img/ns_ipq_b_p_o.png', dpi=300)
plt.figure()
for j in range(len(time_steps_original)):
    for k in ns_ipq_b_runs_q_original:
        try:
            ns_ipq_b_avg_hist_arrays_q_original = [ns_ipq_b_runs_q_original[k][j] for k in ns_ipq_b_runs_q_original]
            ns_ipq_b_avg_hist_q_original = [np.mean(k) for k in zip(*ns_ipq_b_avg_hist_arrays_q_original)]
        except:
            continue
    plt.plot(plot_x, ns_ipq_b_avg_hist_q_original, markers_original[j], c=colors_original[j], label="t=" + str(time_steps_original[j] + 1))
plt.gca().tick_params(direction='in')
plt.xlim([0, 1])
plt.ylim([0, max(ns_ipq_b_avg_hist_q_original) * 1.1])
plt.xlabel('q')
plt.ylabel('D(q)')
plt.legend()
plt.savefig('img/ns_ipq_b_q_o.png', dpi=300)