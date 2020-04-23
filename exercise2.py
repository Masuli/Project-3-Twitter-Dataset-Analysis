import re
import networkx as nx
from networkx.algorithms import community
import matplotlib.pyplot as plt

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
for c in comp:
    print(len(c))