import csv
import networkx as nx
import matplotlib.pyplot as plt
import datetime
import numpy as np
import math

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
            
#print(maxEpoch)
#print(minEpoch)

diff = float((maxEpoch - minEpoch)) / 1000
print("1 tweet is sent every {} seconds.".format(round((diff / float(count)), 4)))
print("{} tweets are sent every second.".format(round((float(count) / diff), 4)))

'''
Now that we have the average time between events (1 tweet / 0.3496s), we can calculate λ for the following equation:

			  (e^-λ) * λ^k
P(k events in interval) = -------------
			        k!

This is the poisson distribution probability of k events in an interval. We can choose a time period/interval and some amount of tweets
and then calculate the probability of that happening.
λ is the average time between events multiplied by the interval.

Example: Probability of people tweeting 25 times in 10 seconds

λ = 1 / (diff / float(count)) * 10 seconds = 28.6

			      (e^-28.6) * 28.6^25
P(25 tweets in 10 seconds) = --------------------- * 100 = 6.27%
				       25!
'''

k = 25
λ = 1 / (diff / float(count)) * 10
print("λ: {} tweets are expected.".format(round(λ, 2)))

p = np.exp(-λ) * np.power(λ, k) / math.factorial(k)
print("Probability of people tweeting 25 times in 10 seconds is {}%".format(round((p * 100), 2)))

k = np.arange(10, 60, 1)
d = []

for i in k:
	p = np.exp(-λ) * np.power(λ, i) / math.factorial(i)
	d.append(p)

sum = 0
for v in d:
	sum += v

print("The sum of all probabilities from 10 tweets to 60 tweets in 10 seconds: {}".format(sum))
print("The most likely amount of tweets in 10 seconds was {} with the probability of {}%".format(k[d.index(max(d))], round((max(d) * 100), 2)))
plt.plot(k, d, 'bs')
plt.show()

'''
This plot shows the poisson distribution probabilities of people tweeting from 10 to 60 times in 10 seconds.
'''

'''
The average time between tweets was been calculated by parsing the excel file for the (epoch) dates of the earliest and the most recent tweet.
The smaller date was then subtracted from the bigger date to get the time between the first and last tweet (in seconds).
We then simply divided the time by the number of tweets to get the average time between tweets.
Because we used the whole file to get the value, it should be the most accurate and therefore optimal.
'''
