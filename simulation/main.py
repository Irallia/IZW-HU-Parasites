"""main method"""
import csv
import datetime
from copy import deepcopy
from pprint import pprint
from time import gmtime, strftime

from Bio import Phylo
from termcolor import colored

from non_binary_simulation import buildTree
from non_binary_simulation.parsimony.Fitch_MP import fitch_parsimony
from non_binary_simulation.parsimony.My_MP import my_parsimony
from non_binary_simulation.parsimony.Sankoff_MP import sankoff_parsimony
from utilities import Drawings

START_TIME = datetime.datetime.now().replace(microsecond=0)
CURRENT_TIME = datetime.datetime.now().replace(microsecond=0)

def main():
    """Main method"""
    global START_TIME
    global CURRENT_TIME
    print(colored("------------------------ start simulation ------------------------", "green"))
    print(strftime("%Y-%m-%d %H:%M:%S", gmtime()))
    CURRENT_TIME = print_time(START_TIME)
    print(colored("---------------- metadata ----------------", "green"))
    number_trees = 1    # number of simulated trees
    number_leafnodes = 20000
    realP = 40   # percentage of parasites (percentage +-5%)

    print("Build", number_trees, "random trees with", colored(number_leafnodes, 'blue'), "leafnodes", realP, "% parasites.")    
    leaf_nodes = 2300000
    print("real OTL tree: 2500000 nodes: 240000 internal,", leaf_nodes, "leaf nodes")
    number_P = 43674
    number_FL = 88967
    print("Information about species from GloBI:", number_P, "#P,", number_FL, "#FL")
    percentage_P = 1 / leaf_nodes * number_P
    percentage_FL = 1/ leaf_nodes * number_FL
    percentage_U = 1 - percentage_P - percentage_FL
    print("=>", round(percentage_P * 100, 2), "% parasites,", round(percentage_FL * 100, 2), "% freeliving =>", round(percentage_U * 100, 2), "% unknown leaf nodes")
    # print("=> %.2f \% parasites %.2f" % percentage_P, % percentage_FL)
    percentage = [realP, percentage_P, percentage_FL]

    for _ in range(0, number_trees):
        print(colored("---------------- get random tree ----------------", "green"))
        result = buildTree.get_random_tagged_tree(number_leafnodes, percentage)
        current_tree = result[0]
        nodelist = result[1]
        # Phylo.draw(current_tree)
        CURRENT_TIME = print_time(CURRENT_TIME)
        print(colored("---------------- multifurcate tree ----------------", "green"))
        buildTree.get_non_binary_tree(current_tree.clade, nodelist)
        # Phylo.draw(current_tree)
        CURRENT_TIME = print_time(CURRENT_TIME)
        print(colored("---------------- maximum parsimony algorithms ----------------", "green"))
        run_parsimony_algorithms(current_tree, nodelist)
        # ---------------- compare results ----------------
        print(colored("-------- evaluation --------", "green"))
        # ---------------- drawings ----------------
        # do_some_drawings(current_tree, nodelist, parsimony_tree, parsimony_nodelist)
        time_new = datetime.datetime.now().replace(microsecond=0)
        print(strftime("%Y-%m-%d %H:%M:%S", gmtime()))
        print("whole time needed:", time_new - START_TIME)
    return

def run_parsimony_algorithms(current_tree, nodelist):
    global START_TIME
    global CURRENT_TIME
    CURRENT_TIME = datetime.datetime.now().replace(microsecond=0)
    print(colored("---------------- Fitch parsimony ----------------", "green"))
    fitch_MP_tree = deepcopy(current_tree)
    fitch_MP_nodelist = deepcopy(nodelist)
    fitch_parsimony(fitch_MP_tree.clade, fitch_MP_nodelist)
    CURRENT_TIME = print_time(CURRENT_TIME)
    print(colored("---------------- my parsimony ----------------", "green"))
    my_MP_tree = deepcopy(current_tree)
    my_MP_nodelist = deepcopy(nodelist)
    my_parsimony(my_MP_tree.clade, my_MP_nodelist)
    CURRENT_TIME = print_time(CURRENT_TIME)
    print(colored("---------------- Sankoff parsimony ----------------", "green"))
    sankoff_MP_tree = deepcopy(current_tree)
    sankoff_MP_nodelist = deepcopy(nodelist)
    sankoff_parsimony(sankoff_MP_tree, sankoff_MP_nodelist)
    CURRENT_TIME = print_time(CURRENT_TIME)
    # --------------------------------------------------------
    result_list = [['id','original tag', 'fitch', 'my', 'sankoff']]
    for i in range(0, len(nodelist)):
        if fitch_MP_nodelist[i][3] == '':
            fitch_MP_nodelist[i][3] = '-'
        if my_MP_nodelist[i][3] == '':
            my_MP_nodelist[i][3] = '-'
        if sankoff_MP_nodelist[i][3] == '':
            sankoff_MP_nodelist[i][3] = '-'
        result_list.append([nodelist[i][0], nodelist[i][2], fitch_MP_nodelist[i][3], my_MP_nodelist[i][3], sankoff_MP_nodelist[i][3]])

    with open('output.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(result_list)
    # pprint(result_list)
    return

def do_some_drawings(tree, nodelist, parsimony_tree, parsimony_nodelist):
    """seperated drawings"""
    tree.name = 'random tree'
    # Phylo.draw(tree)
    named_tree = deepcopy(tree)
    named_tree.name = 'tagged tree'
    Drawings.tag_names(named_tree.clade, nodelist, 1)
    Phylo.draw(named_tree)
    untagged_tree = deepcopy(tree)
    untagged_tree.name = 'untagged tree'
    Drawings.tag_leaf_names(untagged_tree.clade, nodelist)
    # Phylo.draw(untagged_tree)
    # tree.name = 'parsimony down'
    # Phylo.draw(tree)
    # tree.name = 'parsimony up'
    # Phylo.draw(tree)
    parsimony_tree.name = 'parsimonious solution tree'
    Drawings.tag_names(parsimony_tree.clade, parsimony_nodelist, 2)
    Phylo.draw(parsimony_tree)
    parsimony_like_tree = deepcopy(tree)
    parsimony_like_tree.name = 'parsimonious-like solution tree'
    Drawings.tag_names(parsimony_like_tree.clade, nodelist, 2)
    Phylo.draw(parsimony_like_tree)
    # Phylo.draw_graphviz(parsimony_tree)
    # pylab.show()


def print_time(time_old):
    time_new = datetime.datetime.now().replace(microsecond=0)
    print("time needed:", time_new - time_old)
    return time_new

main()
