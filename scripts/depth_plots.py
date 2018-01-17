import ast
import csv

import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np

# global variables:
PLOT_NUMBER = 1
ROWS = 1
COLS = 2

def main():
    global PLOT_NUMBER

    f = open('../data/nodelist.csv', 'rt')
    reader = csv.reader(f)
    min_depths = []
    max_depths = []
    mean_depths = [] 
    nr_children = []
    for r in reader:
        if r != []:
            depths = ast.literal_eval(r[2])
            min_depths.append(depths[0])
            max_depths.append(depths[1])
            mean_depths.append(depths[2])
            if(int(r[3]) != 0):
                nr_children.append(int(r[3]))
    f.close()

    print(nr_children)

    f, axs = plt.subplots(ROWS, COLS, figsize=(13, 5))
    plt.suptitle('Histograms of metadata', fontsize=12, y=1)

    ax = plt.subplot(ROWS, COLS, PLOT_NUMBER)
    PLOT_NUMBER += 1

    n, bins, patches = plt.hist([min_depths, max_depths, mean_depths], 20)

    plt.title("Histogram of depths", fontweight='bold')
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

    plt.subplot(ROWS, COLS, PLOT_NUMBER)
    n, bins, patches = plt.hist(nr_children, 20)
    plt.title("Histogram of multifurcations", fontweight='bold')

    plt.show()

main()
