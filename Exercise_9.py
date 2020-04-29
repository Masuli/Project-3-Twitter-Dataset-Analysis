import csv
import networkx as nx
import matplotlib.pyplot as plt
import datetime

dayGraph = nx.Graph()
weekGraph = nx.Graph()
dayTweetGraph = nx.Graph()

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
             
print("maxEpoch: {}".format(maxEpoch))
print("minEpoch: {}".format(minEpoch))

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
                dayGraph.add_edge(dayEvolution, row['id'])
                weekGraph.add_edge(weekEvolution, row['id'])
            else:
                epoch = int(row['create_at_long'])
                dayEvolution = int((epoch - minEpoch) / epochDay)
                dayTweetGraph.add_edge(dayEvolution, row['id'])
        except ValueError:
            continue

for i in range(0, numOfDays + 1):
    print("Day: {}, Retweet amount: {}".format(i, len(dayGraph.edges(i))))

print("")

for i in range(0, numofWeeks + 1):
    print("Week: {}, Retweet amount: {}".format(i, len(weekGraph.edges(i))))

print("")

for i in range(0, numOfDays + 1):
    print("Day: {}, Tweet amount: {}, Retweet amount: {}, Ratio: {} retweets / tweet.".format(i, len(dayTweetGraph.edges(i)), len(dayGraph.edges(i)), float(len(dayGraph.edges(i))) / len(dayTweetGraph.edges(i))))