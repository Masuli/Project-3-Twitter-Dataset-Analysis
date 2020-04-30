import re
import networkx as nx
import matplotlib.pyplot as plt
import csv
import operator

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

users = dict()

with open('distinct_users_from_search_table_real_map.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        users[row['user_id']] = row['indegree']

mostFollowed = max(users.iteritems(),key=lambda x: int(operator.itemgetter(1)(x)))
mostFollowedUID = int(mostFollowed[0])

print(mostFollowed)# we find britney spears. (Most followed in the follower sql dump.)
followers = dict()
status = False
index = 0
with open("active_follower_real.sql") as myfile:
    for line in myfile:
        if status:
            break
        result = re.findall(r'\(.*?\)', line)
        for value in result:
            stripped = value.strip('()')
            values = stripped.split(',')
            if len(values) == 2 and is_integer(values[0]) and is_integer(values[1]) and int(values[1]) == mostFollowedUID:
                followers[values[0]] = []
                index += 1
                if index == 10:
                    status = True
                    break

followerGraph = nx.Graph()
print(len(followers))
total = 0
with open("active_follower_real.sql") as myfile:
    for line in myfile:
        result = re.findall(r'\(.*?\)', line)
        for value in result:
            stripped = value.strip('()')
            values = stripped.split(',')
            if len(values) == 2 and is_integer(values[0]) and is_integer(values[1]) and followers.has_key(values[1]):
                followerGraph.add_edge(values[0], values[1])


print("nodes: {} edges: {}".format(len(followerGraph.nodes()), len(followerGraph.edges())))
print_average_and_variance(nx.degree_centrality(followerGraph), "degree centrality")
print_average_and_variance(nx.betweenness_centrality(followerGraph), "betweenness centrality")
print_average_and_variance(nx.closeness_centrality(followerGraph), "closeness centrality")
print_average_and_variance(nx.pagerank(followerGraph), "page rank")
print_average_and_variance(nx.square_clustering(followerGraph), "clustering coefficient")

avgShortestPath = nx.average_shortest_path_length(followerGraph)

spVarianceSum = 0
spVarianceCount = 0

for node in followerGraph.nodes():
    lengthInfo = nx.single_source_dijkstra_path_length(followerGraph, node)
    pathSum = float(sum(lengthInfo.values()))
    pathLength = len(lengthInfo.values())
    spVarianceSum += (pathSum / pathLength - avgShortestPath) ** 2
    spVarianceCount += 1

spVariance = spVarianceSum / (spVarianceCount - 1)
print("shortest path: average: {}, variance: {}".format(avgShortestPath, spVariance))

#not sure about Giant component size.
Gcc = sorted(nx.connected_components(followerGraph), key=len, reverse=True)
print("Giant component size: {}".format(len(Gcc[0])))

print("drawing graph")
nx.draw(followerGraph, with_labels = False, node_size = 2)
plt.savefig("graph.png")
