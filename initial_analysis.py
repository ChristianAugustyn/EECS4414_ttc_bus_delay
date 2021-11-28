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

g = open("global_eff_calculation.txt", 'r')

with open('average_clustering_calculation.txt') as f:
    lines = f.readlines()

new_lines=[]
for line in lines:
    new_lines.append(float(line))

acc_data = [
    sum(new_lines[0:879])/879, 
    sum(new_lines[880:1758])/879, 
    sum(new_lines[1759:2637])/879,
    sum(new_lines[2638:3516])/879,
    sum(new_lines[3517:4395])/879,
    sum(new_lines[4396:5274])/879,
    sum(new_lines[5275:6153])/879,
    sum(new_lines[6154:7032])/879,
    sum(new_lines[7033:7911])/879,
    sum(new_lines[7912:8798])/886,
]

x_values = ["10%", "20%","30%","40%","50%","60%","70%","80%","90%","100%"]
plt.scatter(x_values, acc_data)
plt.plot(x_values, acc_data)
plt.title("Distribution of average clustering coefficient")
plt.xlabel("percentage")
plt.ylabel("average clustering coefficient")
plt.show()

# G = G.to_undirected()
# print("here")

# # OG graph
# print("global")
# g.write(str(nx.global_efficiency(G))+"\n")
# H = nx.Graph(G)
# print("avg clustering")
# a.write(str(nx.average_clustering(H))+"\n")
# print("done")

# # Remove nodes one by one
# for k, v in sorted_dict.items():
#     print("k: "+ k)
#     G.remove_node(k)
#     print("global")
#     g.write(str(nx.global_efficiency(G))+"\n")
#     H = nx.Graph(G)
#     print("avg clustering")
#     a.write(str(nx.average_clustering(H))+"\n")
#     # break

# g.close()
# a.close()
  
