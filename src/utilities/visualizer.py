import matplotlib.pyplot as plt
import numpy as np
import sys
import csv

def loadData(filename):
    with open(filename, "r") as f:
        reader = csv.DictReader(f)
        tempArr = list(reader)
    return tempArr

def plot(x,y):
    plt.plot(x, y, 'o', color='black')

project_directory = 'C:/Users/dtwiz/Documents/GitHub/Twitter-data-collector/'#Must be changed to your projectdirectory

data = loadData(project_directory + 'data/' + str(sys.argv[1]))
targetName = str(sys.argv[2])
target = []
dataDict = {}

print(data)

for y in data[0]:
    dataDict[y] = []

for x in range(len(data)):
    temp = data[x][targetName]
    if temp == '':
        temp = None
    else:
        temp = float(temp)
    target.append(temp)
    for y in data[x]:
        temp = data[x][y]
        if temp == '':
            temp = None
        else:
            temp = float(temp)
        dataDict[y].append(temp)
    #data[x] = temp

print(dataDict['vol'])
print(target)

plot(dataDict['vol'], target)
plt.show()

# count = 1
# for x in dataDict:
#     plt.figure(count)
#     plot(dataDict[x], target)
#     plt.show()
#     count += 1
