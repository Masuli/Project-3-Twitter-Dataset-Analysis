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


#2-3Clique 
nd = nx.convert_node_labels_to_integers(G,first_label=2)
c = list(community.k_clique_communities(nd, 2))
print(len(c))
print(list(c[0]))

nd = nx.convert_node_labels_to_integers(G,first_label=2)
c = list(community.k_clique_communities(nd, 3))
print(len(c))
print(list(c[0]))

#2-3club
def club(k, G):
    club_communities = list()
    for node in G.nodes():
        lengthInfo = nx.single_source_dijkstra_path_length(G, node)
        validNode = True
        for value in lengthInfo:
            if value > k:
                validNode = False
        if validNode is True:
            print(node)
            club_communities.append(node)
    return club_communities


club_2_map = club(2, G)
club_3_map = club(3, G)