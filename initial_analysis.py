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

plt.hist(list(pagerank.values()))
plt.title(f"Distribution of PageRank Values")
plt.xlabel("PageRank Value")
plt.ylabel("Count")
plt.show()
# for item in islice(sorted_dict.items(), 50): 
#     print(G.nodes[item[0]]["stop_name"])
print("with all nodes")
# print(nx.edge_betweenness_centrality(pagerank))
# print(nx.global_efficiency(pagerank))
# print(nx.average_clustering(pagerank))

f = open("calculation.txt")

for k, v in sorted_dict:
    temp = pagerank.remove_node(k)
    f.write("remove " + k + " : ")
    print("remove " + k + " : ")
    # f.write(nx.edge_betweenness_centrality(temp))
    # print(nx.edge_betweenness_centrality(temp))
    f.write(nx.global_efficiency(temp))
    print(nx.global_efficiency(temp))
    f.write(nx.average_clustering(temp))
    print(nx.average_clustering(temp))
    break

f.close()
  
