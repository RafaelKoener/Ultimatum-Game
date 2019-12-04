import numpy as np
import matplotlib.pyplot as plt
s = np.random.uniform(0, 1, 100)
print(s)


plt.plot(s)
plt.show()
# for replicating G_size = 10000
# G_size = 100
# # G = nx.complete_graph(G_size)
# G = nx.barabasi_albert_graph(G_size,3)
#
# p = {k: random.random() for k in range(G_size)}
# q = {k: random.random() for k in range(G_size)}
# f = {k: 0 for k in range(G_size)}
# nx.set_node_attributes(G, p, 'p')
# nx.set_node_attributes(G, q, 'q')
# nx.set_node_attributes(G, f, 'f')