import csv
import networkx as nx
import matplotlib.pyplot as plt
import datetime

G = nx.Graph()

tweets = dict()

with open('link_status_search_with_ordering_real.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        try:
            replyToUserId =  int(row['inreplyto_user_id']) 
            if replyToUserId == -1:
                tweets[row['id']] = row['create_at_long']
        
        except ValueError:
            continue

for tweet in tweets:
    print(tweet)

#nx.draw(G, with_labels = False, font_weight = "bold")
#plt.savefig("graph.png")