import matplotlib.pyplot as plt
import numpy as np
import sys

data = np.loadtxt(str(sys.argv[1]), delimiter=',')
targetName = str(sys.argv[2])
target = []

print(data)

for x in range(len(data)):
    target.append(data[x][targetName])
    temp = {}
    for y in data[x]:
        temp[y] = data[x][y]
    data[x] = temp

print(data)

def plot(x,y):
    plt.plot(x, y, 'o', color='black')
