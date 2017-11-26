from pprint import pprint

import csv
import numpy as np
import matplotlib.pyplot as plt

from Bio import Phylo

def main():
    """main method"""
    # tree = Phylo.read('../../data/opentree9.1_tree/grafted_solution/grafted_solution.tre', 'newick')
    tree = Phylo.read('../../data/opentree9.1_tree/labelled_supertree/labelled_supertree.tre', 'newick')
    # cellular organisms: ott93302
    get_metadata_of_subtree(tree.clade, "ott93302", "data/cellular_organisms.csv")
    # get_metadata_of_subtree(tree.clade, "ott304358", "data/Eukaryota.csv")
    # get_metadata_of_subtree(tree.clade, "ott691846", "data/Metazoa.csv")
    # get_metadata_of_subtree(tree.clade, "ott770311", "data/Hominidae.csv")
    # get_metadata_of_subtree(tree.clade, "ott422673", "data/Apicomplexa.csv")
    # #internal nodes, #leaf nodes:
    # mean depth, max depth, min depth:

    # ['ott93302', 4.453689419493294, 94, 3]
    # Eukaryota:
    # 2535437 nodes -> [241974, 2293463]
    # ['ott304358', 3.370789824804477, 93, 2]
    # Metazoa:
    # 1670956  nodes -> [179944, 1491012]
    # ['ott691846', 5.323464690895551, 88, 2]
    # Hominidae:
    # 26  nodes -> [12, 14]
    # ['ott770311', 4.775, 6, 4]
    # Apicomplexa:
    # 2102  nodes -> [239, 1863]
    # ['ott422673', 3.7152309882752474, 15, 2]
    return

def get_metadata(subtree, nodelist, metadata):
    """calculate depths of every node"""
    #                   0       1
    #   nodelist    - [ottId, mean depth, max depth, min depth]
    #   metadata    - [#internal nodes, #leaf nodes]
    mean_depth = -1
    max_depth = -1
    min_depth = 10000000000000000000000000
    nodelist.append([subtree.name, mean_depth, max_depth, min_depth])
    current_list_index = len(nodelist) - 1
    # if leaf node, then depth = 1
    if subtree.is_terminal():
        mean_depth = 1
        max_depth = 1
        min_depth = 1
        metadata[1] += 1
    else:
        child_depth = 0
        metadata[0] += 1
        for clade in subtree.clades:
            result = get_metadata(clade, nodelist, metadata)
            nodelist = result[0]
            child_depth = child_depth + result[1][0]
            metadata = result[2]
            if result[1][1] > max_depth:
                max_depth = result[1][1]
            if result[1][2] < min_depth:
                min_depth = result[1][2]
        mean_depth = child_depth/len(subtree.clades) + 1
        max_depth += 1
        min_depth += 1
    nodelist[current_list_index][1] = mean_depth
    nodelist[current_list_index][2] = max_depth
    nodelist[current_list_index][3] = min_depth
    depths = [mean_depth, max_depth, min_depth]
    return [nodelist, depths, metadata]

def get_metadata_of_subtree(tree, ott, filename):
    subtree = get_subtree(tree, ott)
    # print(subtree)
    print(subtree.name)

    result = get_metadata(subtree, [], [0,0])
    nodelist = result[0]
    depth = result[1]
    metadata = result[2]
    print("root node:", nodelist[0][0])
    print("mean depth, max depth, min depth:")
    pprint(nodelist[0])
    print(metadata[0] + metadata[1], "nodes")
    print("#internal nodes, #leaf nodes:")
    pprint(metadata)

    # write it
    with open(filename, 'w') as csvfile:
        writer = csv.writer(csvfile)
        [writer.writerow(r) for r in nodelist]

    plot_histogram(nodelist)
    return

def get_subtree(subtree, ott):
    if subtree.name == ott:
        return subtree
    if subtree.is_terminal():
        return -1
    for clade in subtree.clades:
        subtree = get_subtree(clade, ott)
        if subtree != -1:
            # if subtree.name == ott:
            return subtree
    return -1

def plot_histogram(nodelist):
    # the histogram of the data
    plt.figure(1)
    plt.title('Histograms of depths')
    # plt.xlabel("Value")
    # plt.ylabel("Frequency")
    # plt.grid(True)
    # plt.axis([0, 1, 0, 10])

    plt.subplot(311)
    plt.text(7, 5, r'mean depth')
    plt.hist([row[1] for row in nodelist], 100, normed=1, facecolor='r', alpha=0.75)

    plt.subplot(312)
    plt.text(70, 0.5, r'max depth')
    plt.hist([row[2] for row in nodelist], 100, normed=1, facecolor='b', alpha=0.75)

    plt.subplot(313)
    plt.text(5, 8, r'min depth')
    plt.hist([row[3] for row in nodelist], 100, normed=1, facecolor='g', alpha=0.75)

    plt.show()
    return
    

main()
