import networkx as nx
from itertools import islice
import matplotlib.pyplot as plt
import networkx as nx
import scipy as sp

G = nx.read_gpickle("transit_graph.gpickle")
G.add_node('abc', dob=1185, pob='usa', dayob='monday')

pagerank = nx.pagerank(G)

sorted_tuples = reversed(sorted(pagerank.items(), key=lambda item: item[1]))
sorted_dict = {k: v for k, v in sorted_tuples}
print("sorted")

# plt.hist(list(pagerank.values()))
# plt.title(f"Distribution of PageRank Values")
# plt.xlabel("PageRank Value")
# plt.ylabel("Count")
# plt.show()
# for item in islice(sorted_dict.items(), 50): 
#     print(G.nodes[item[0]]["stop_name"])
# print("with all nodes")
# print(nx.edge_betweenness_centrality(pagerank))
# print(nx.global_efficiency(pagerank))
# print(nx.average_clustering(pagerank))

g = open("global_eff_calculation.txt", 'w')
a = open("average_clustering_calculation.txt", 'w')

G = G.to_undirected()
print("here")

# OG graph
print("global")
g.write(str(nx.global_efficiency(G))+"\n")
H = nx.Graph(G)
print("avg clustering")
a.write(str(nx.average_clustering(H))+"\n")
print("done")

# Remove nodes one by one
for k, v in sorted_dict.items():
    print("k: "+ k)
    G.remove_node(k)
    print("global")
    g.write(str(nx.global_efficiency(G))+"\n")
    H = nx.Graph(G)
    print("avg clustering")
    a.write(str(nx.average_clustering(H))+"\n")
    # break

g.close()
a.close()
  