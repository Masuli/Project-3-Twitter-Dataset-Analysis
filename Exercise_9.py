import csv
import networkx as nx
import matplotlib.pyplot as plt
import datetime

dayGraph = nx.Graph()
weekGraph = nx.Graph()

epochDay = 86400 * 1000
epochWeek = epochDay * 7

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
             
print(maxEpoch)
print(minEpoch)

epochDiff = maxEpoch - minEpoch

numOfDays = epochDiff / epochDay
numofWeeks = epochDiff / epochWeek

print("numOfDays: {}, numOfWeeks: {}".format(numOfDays, numofWeeks))

with open('link_status_search_with_ordering_real.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        try:
            replyToUserId =  int(row['inreplyto_user_id']) 
            if replyToUserId != -1:
                epoch = int(row['create_at_long'])
                dayEvolution = int((epoch - minEpoch) / epochDay)
                weekEvolution = int((epoch - minEpoch) / epochWeek)
                dayGraph.add_edge(dayEvolution, row['user_id'])
                weekGraph.add_edge(weekEvolution, row['user_id'])
        
        except ValueError:
            continue

for i in range(0, numOfDays + 1):
    print("Day: {}, Retweet amount: {}".format(i, len(dayGraph.edges(i))))

for i in range(0, numofWeeks + 1):
    print("Week: {}, Retweet amount: {}".format(i, len(weekGraph.edges(i))))

#nx.draw(G, with_labels = False, font_weight = "bold")
#plt.savefig("graph.png")