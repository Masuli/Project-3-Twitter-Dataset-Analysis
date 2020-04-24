import csv
import networkx as nx
import matplotlib.pyplot as plt
import datetime

count = 0
minEpoch = 0
maxEpoch = 0
with open('link_status_search_with_ordering_real.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        epochValue = int(row['create_at_long'])
        count += 1
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

diff = float((maxEpoch - minEpoch)) / 1000
print("{} tweets per second.".format(float(count) / diff))