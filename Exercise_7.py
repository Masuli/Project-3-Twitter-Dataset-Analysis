import csv
import networkx as nx
import matplotlib.pyplot as plt
import datetime

arr = list()

with open('link_status_search_with_ordering_real.csv') as csvfile:
     reader = csv.DictReader(csvfile)
     for row in reader:
        arr.append(row['create_at'])

plt.hist(arr, bins=15)
plt.show()
