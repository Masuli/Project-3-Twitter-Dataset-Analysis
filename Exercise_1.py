import re
import networkx as nx
import matplotlib.pyplot as plt

def is_integer(string):
    try: 
        int(string)
        return True
    except ValueError:
        return False

def print_average_and_variance(hash_map, name):
    total = 0
    for val in hash_map:
        total += hash_map[val]

    average = total / len(hash_map)

    varianceSum = 0
    for val in hash_map:
        varianceSum += (hash_map[val] - average) ** 2

    variance = varianceSum / (len(hash_map) - 1)
    
    print ("{} average: {}, variance: {}".format(name, average, variance))  

G = nx.Graph()
i = 0
exit_this = False

with open("active_follower_real.sql") as myfile:
    for line in myfile:
        if exit_this == True:
            break
        result = re.findall(r'\(.*?\)', line)
        for value in result:
            stripped = value.strip('()')
            values = stripped.split(',')
            if len(values) == 2 and is_integer(values[0]) and is_integer(values[1]):
                G.add_edge(values[0], values[1])
                i += 1
                if i >= 1000:
                    exit_this = True
                    break

print ("numOfNodes: {}, numOfEdges: {}".format(G.number_of_nodes(), G.number_of_edges())) 

print_average_and_variance(nx.degree_centrality(G), "degree centrality")
print_average_and_variance(nx.betweenness_centrality(G), "betweenness centrality")
print_average_and_variance(nx.closeness_centrality(G), "closeness centrality")
print_average_and_variance(nx.pagerank(G), "page rank")
print_average_and_variance(nx.square_clustering(G), "clustering coefficient")

avgShortestPath = nx.average_shortest_path_length(G)

spVarianceSum = 0
spVarianceCount = 0

for node in G.nodes():
    lengthInfo = nx.single_source_dijkstra_path_length(G, node)
    pathSum = float(sum(lengthInfo.values()))
    pathLength = len(lengthInfo.values())
    spVarianceSum += (pathSum / pathLength - avgShortestPath) ** 2
    spVarianceCount += 1

spVariance = spVarianceSum / (spVarianceCount - 1)
print("shortest path: average: {}, variance: {}".format(avgShortestPath, spVariance))

#not sure about Giant component size.
Gcc = sorted(nx.connected_components(G), key=len, reverse=True)
print("Giant component size: {}".format(len(Gcc[0])))

print("drawing graph")
nx.draw(G, with_labels = False, font_weight = "bold")
plt.savefig("graph.png")
