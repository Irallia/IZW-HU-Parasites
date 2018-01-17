import ast
import csv

import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np

f = open('../data/nodelist.csv', 'rt')
reader = csv.reader(f)
min_depths = []
max_depths = []
mean_depths = [] 
for r in reader:
    if r != []:
        depths = ast.literal_eval(r[2])
        min_depths.append(depths[0])
        max_depths.append(depths[1])
        mean_depths.append(depths[2])
f.close()

plt.figure(figsize=(13,5))
n, bins, patches = plt.hist([min_depths, max_depths, mean_depths], 50)

plt.title("Depths", fontweight='bold')
plt.xlabel("# Children")
plt.ylabel("# Nodes")

# plt.xscale('log')
plt.yscale('log')
# plt.yscale('symlog')

blue_patch = mpatches.Patch(color='blue', label='min depths')
orange_patch = mpatches.Patch(color='orange', label='max depths')
green_patch = mpatches.Patch(color='green', label='mean depths')
plt.legend(handles=[blue_patch, orange_patch, green_patch], loc="upper right")
plt.grid(True)

plt.show()
