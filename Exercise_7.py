import csv
import networkx as nx
import matplotlib.pyplot as plt
import datetime

arr = list()

epochDay = 86400 * 1000
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

epochDiff = maxEpoch - minEpoch
epoch15 = epochDiff / 15

with open('link_status_search_with_ordering_real.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        try:
            epoch = int(row['create_at_long'])
            evolution = int((epoch - minEpoch) / epoch15)
            arr.append(evolution)    
        except ValueError:
            continue

plt.hist(arr, bins=15)
plt.show()