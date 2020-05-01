import re
import networkx as nx
from networkx.algorithms import community
import matplotlib.pyplot as plt
import csv
import operator
import random

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

clique_1_list = nx.find_cliques(followerGraph)
print("1-Clique: ")
largest_1_clique = 0
total_1_clique = 0
for val in clique_1_list:
    total_1_clique += 1
    if len(val) > largest_1_clique:
        largest_1_clique = len(val)
print("{} count: {}".format(largest_1_clique, total_1_clique))

clique_2_set = community.k_clique_communities(followerGraph, 2)
clique_2_list = list()
for cset in clique_2_set:
    clique_2_list.append(list(cset))

clique_3_set = community.k_clique_communities(followerGraph, 3)

clique_3_list = list()
for cset in clique_3_set:
    clique_3_list.append(list(cset))

print("2-Clique: ")
for l in clique_2_list:
    print(len(l))

print("3-Clique: ")
for l in clique_3_list:
    print(len(l))

def club(graph, k, node):
    potentialNodes = list()
    lengthInfo = nx.single_source_shortest_path_length(graph, node, k)

    for node in lengthInfo:
        validNode = True 
        for node_ in potentialNodes:
            lengthInfo_ = nx.single_source_shortest_path_length(graph, node_, k)
            if not lengthInfo_.has_key(node):
                validNode = False
                break

        if validNode:
            potentialNodes.append(node)

    if len(potentialNodes):
        potentialNodes.append(node)
    
    return potentialNodes

club_2_community = list()
club_3_community = list()
club_2_count = 0
club_3_count = 0

for node in followerGraph.nodes():
    club_2_community = club(followerGraph, 2, node)
    if len(club_2_community):
        print("2-club community: source node: {}, size: {}".format(node, len(club_2_community)))
        club_2_count += 1
    
    club_3_community = club(followerGraph, 3, node)
    if len(club_3_community):
        print("3-club community: source node: {}, size: {}".format(node, len(club_3_community)))
        club_3_count += 1

    if club_2_count >= 5 and club_3_count >= 5:
        break