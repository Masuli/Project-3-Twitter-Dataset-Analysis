import csv
import networkx as nx
import matplotlib.pyplot as plt
import datetime
import numpy as np
import math

G = nx.Graph()

epochDay = 86400 * 1000

minEpoch = 0
maxEpoch = 0

with open('link_status_search_with_ordering_real.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        epochValue = int(row['create_at_long'])
        if minEpoch == 0:
            maxEpoch = epochValue
            minEpoch = epochValue
            continue
        if epochValue > maxEpoch:
            maxEpoch = epochValue
        if epochValue < minEpoch:
            minEpoch = epochValue
             
#print("maxEpoch: {}".format(maxEpoch))
#print("minEpoch: {}".format(minEpoch))

diff = float((maxEpoch - minEpoch)) / 1000

with open('link_status_search_with_ordering_real.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        try:
            replyToUserId =  int(row['inreplyto_user_id']) 
            if replyToUserId != -1:
                epoch = int(row['create_at_long'])
                dayEvolution = int((epoch - minEpoch) / epochDay)
                G.add_edge(dayEvolution, row['id'])
            else:
                epoch = int(row['create_at_long'])
                dayEvolution = int((epoch - minEpoch) / epochDay)
        except ValueError:
            continue

retweets = nx.number_of_edges(G)
print("1 retweet is sent every {} seconds.".format(round((diff / float(retweets)), 4)))
print("{} retweets are sent every second.".format(round((float(retweets) / diff), 4)))

λ = 1 / (diff / float(retweets)) * 60
print("λ: {} retweets are expected.".format(round(λ, 2)))

k = np.arange(5, 30, 1)
d = []

for i in k:
	p = np.exp(-λ) * np.power(λ, i) / math.factorial(i)
	d.append(p)

sum = 0
for v in d:
	sum += v

print("The sum of all probabilities from 5 retweets to 30 retweets in 1 minute: {}".format(sum))
print("The most likely amount of retweets in 1 minute was {} with the probability of {}%".format(k[d.index(max(d))], round((max(d) * 100), 2)))
plt.plot(k, d, 'bs')
plt.show()
