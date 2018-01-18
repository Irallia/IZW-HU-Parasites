import ast
import csv

import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np

# global variables:
PLOT_NUMBER = 1
ROWS = 2
COLS = 3

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
            # if int(r[3]) > 2:
            nr_children.append(int(r[3]))
    f.close()

    # print(nr_children)

    f, axs = plt.subplots(ROWS, COLS, figsize=(14, 8))
    plt.suptitle('Histograms of metadata', fontsize=14, fontweight='bold')

    NR_BINS = 70
    X_START = 1
    Y_START = 0
    Y_END = 10000000

    # -----------------------------------------------------------------------------
    ax = plt.subplot(ROWS, COLS, PLOT_NUMBER)
    PLOT_NUMBER += 1

    n, bins, patches = plt.hist([min_depths, max_depths, mean_depths], NR_BINS)

    plt.title("Histogram of depths", fontweight='bold')
    plt.xlabel("# Children")
    plt.ylabel("# Nodes")

    blue_patch = mpatches.Patch(color='blue', label='min depths')
    orange_patch = mpatches.Patch(color='orange', label='max depths')
    green_patch = mpatches.Patch(color='green', label='mean depths')
    plt.legend(handles=[blue_patch, orange_patch, green_patch], loc="upper right")

    plt.yscale('log')
    plt.axis([X_START, 30, Y_START, Y_END])
    plt.grid(True)

    # -----------------------------------------------------------------------------
    plt.subplot(ROWS, COLS, PLOT_NUMBER)
    PLOT_NUMBER += 1
    n, bins, patches = plt.hist(nr_children, NR_BINS)
    plt.title("Histogram of multifurcations", fontweight='bold')
    plt.xlabel("# Children")
    plt.ylabel("# Nodes")
    plt.yscale('log')
    # Axes.loglog(*args, **kwargs)
    plt.axis([0, 5000, Y_START, Y_END])
    plt.grid(True)

    plt.subplot(ROWS, COLS, PLOT_NUMBER)
    PLOT_NUMBER += 1
    n, bins, patches = plt.hist(nr_children, NR_BINS)
    plt.title("Histogram of multifurcations - loglog", fontweight='bold')
    plt.xlabel("# Children")
    plt.ylabel("# Nodes")
    plt.xscale('log')
    plt.yscale('log')
    # Axes.loglog(*args, **kwargs)
    plt.axis([0, 5000, Y_START, Y_END])
    plt.grid(True)

    # -----------------------------------------------------------------------------
    plt.subplot(ROWS, COLS, PLOT_NUMBER)
    PLOT_NUMBER += 1
    n, bins, patches = plt.hist(min_depths, 8, rwidth=0.9)
    # plt.title("Histogram of min depths", fontweight='bold')
    plt.xlabel("# Children")
    plt.ylabel("# Nodes")
    blue_patch = mpatches.Patch(color='blue', label='min depths')
    plt.legend(handles=[blue_patch], loc="upper right")
    plt.yscale('log')
    plt.axis([X_START, 9, Y_START, Y_END])
    plt.grid(True)

    plt.subplot(ROWS, COLS, PLOT_NUMBER)
    PLOT_NUMBER += 1
    n, bins, patches = plt.hist(max_depths, NR_BINS, color="orange")
    # plt.title("Histogram of max depths", fontweight='bold')    
    plt.xlabel("# Children")
    plt.ylabel("# Nodes")
    orange_patch = mpatches.Patch(color='orange', label='max depths')
    plt.legend(handles=[orange_patch], loc="upper right")
    plt.yscale('log')
    plt.axis([X_START, 100, Y_START, Y_END])
    plt.grid(True)

    plt.subplot(ROWS, COLS, PLOT_NUMBER)
    # PLOT_NUMBER += 1
    n, bins, patches = plt.hist(mean_depths, 22, rwidth=0.9, color="green")
    # plt.title("Histogram of mean depths", fontweight='bold')
    plt.xlabel("# Children")
    plt.ylabel("# Nodes")
    green_patch = mpatches.Patch(color='green', label='mean depths')
    plt.legend(handles=[green_patch], loc="upper right")
    plt.yscale('log')
    plt.axis([X_START, 11, Y_START, Y_END])
    plt.grid(True)

    plt.show()

main()
