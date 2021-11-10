import networkx as nx
from itertools import islice
import matplotlib.pyplot as plt

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

