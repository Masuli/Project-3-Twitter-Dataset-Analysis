import networkx as nx
import matplotlib.pyplot as plt
import csv

G = nx.Graph()

with open('distinct_users_from_search_table_real_map.csv') as data:
	next(data, None)
	lines = csv.reader(data)
	for row in lines:
		G.add_node(row[0], name = row[1], in_degree = row[2], out_degree = row[3], bad_user_id = row[4])
	nodet = G.nodes(data=True)
	print(len(G))
	#print(nodes)
	#for row in lines:
		#print(row[0])

#edges = G.number_of_edges()
#print(nx.density(G))
#print(nx.degree_centrality(G))

'''while edges > 1:
	try:
		G.remove_edge(random.randint(0, 4), random.randint(0, 4))
	except:
		continue
	edges = G.number_of_edges()
	print(nx.density(G))
	nx.draw(G, with_labels = True, font_weight = "bold")
	plt.savefig("graph.png")'''