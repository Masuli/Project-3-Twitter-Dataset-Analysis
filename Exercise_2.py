import re
import networkx as nx
import matplotlib.pyplot as plt
from networkx.algorithms import community
from numpy import random

def is_integer(string):
    try: 
        int(string)
        return True
    except ValueError:
        return False

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

comp = community.label_propagation.label_propagation_communities(G)
print("Lengths of communities found using the label propagation community detection:")
for c in comp:
    print(len(c))

print()
print("Lengths of communities found using the asynchronous fluid communities algorithm:")
comp = community.asyn_fluid.asyn_fluidc(G, 5, 30, random.seed(3432))
for c in comp:
    print(len(c))