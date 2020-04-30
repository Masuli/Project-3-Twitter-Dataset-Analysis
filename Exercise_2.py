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

comp = community.label_propagation.label_propagation_communities(followerGraph)
print("Lengths of communities found using the label propagation community detection:")
for c in comp:
    quality = float(len(c)) / len(followerGraph.edges())
    print("size {}, quality: {}".format(len(c), quality))

print("Lengths of communities found using the asynchronous fluid communities algorithm:")
comp = community.asyn_fluid.asyn_fluidc(followerGraph, 5, 30, random.seed(3432))
for c in comp:
    quality = float(len(c)) / len(followerGraph.edges())
    print("size {}, quality: {}".format(len(c), quality))