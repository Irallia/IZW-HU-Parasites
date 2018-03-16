"""main method"""
import csv
import datetime
import sys
from code.simulation.non_binary_simulation import buildTree
from code.simulation.non_binary_simulation.parsimony.Fitch_MP import \
    fitch_parsimony
from code.simulation.non_binary_simulation.parsimony.My_MP import my_parsimony
from code.simulation.non_binary_simulation.parsimony.Sankoff_MP import \
    sankoff_parsimony
from code.utilities.Drawings import tag_leaf_names, tag_names
from code.utilities.Helpers import print_time
from copy import deepcopy
# from pprint import pprint
from time import gmtime, strftime

from Bio import Phylo
from termcolor import colored

# input arguments
args = sys.argv

# global variables:
START_TIME = datetime.datetime.now().replace(microsecond=0)
CURRENT_TIME = datetime.datetime.now().replace(microsecond=0)

# values for simulation:
number_leafnodes = int(sys.argv[1])
number_trees = int(sys.argv[2])                 # number of simulated trees
percentage_parasites = float(sys.argv[3])       # between 0 and 1
percentage_unknown = float(sys.argv[4])         # between 0 and 1
percentage_multifurcation = float(sys.argv[5])  # between 0 and 1

def main():
    """Main method"""
    global START_TIME
    global CURRENT_TIME
    print(colored("------------------------ start simulation ------------------------", "green"))
    print(strftime("%Y-%m-%d %H:%M:%S", gmtime()))
    CURRENT_TIME = print_time(START_TIME)
    print(colored("---------------- metadata ----------------", "green"))
    metadata()
    print(colored("---------------- parameters ----------------", "green"))
    print("Simulate", colored(number_trees, 'blue'), "random trees with", 
        colored(number_leafnodes, 'blue'), "leafnodes", 
        colored(percentage_parasites*100, 'blue'), "% parasites and",
        colored(percentage_unknown*100, 'blue'), "% unknown leafnodes and",
        colored(percentage_multifurcation*100, 'blue'), "% multifurcation of internal nodes.")
    beta_distribution_parameters = decide_for_beta_distribution_parameters()
    print(beta_distribution_parameters)
    diffs = [["Fitch", "My", "Sankoff"]]
    for i in range(1, number_trees + 1):
        print("Tree", colored(i, 'red'))
        print(colored("---------------- get random tree ----------------", "green"))
        result = buildTree.get_random_tagged_tree(number_leafnodes, percentage_parasites, percentage_unknown, percentage_multifurcation, beta_distribution_parameters)
        current_tree = result[0]
        nodelist = result[1]
        # CURRENT_TIME = print_time(CURRENT_TIME)
        print(colored("---------------- multifurcate tree ----------------", "green"))
        buildTree.get_non_binary_tree(current_tree.clade, nodelist)
        CURRENT_TIME = print_time(CURRENT_TIME)
        print(colored("---------------- maximum parsimony algorithms ----------------", "green"))
        diff_percentage = run_parsimony_algorithms(current_tree, nodelist)
        diffs.append(diff_percentage)
        # ---------------- drawings ----------------
        # do_some_drawings(current_tree, nodelist, parsimony_tree, parsimony_nodelist)
        time_new = datetime.datetime.now().replace(microsecond=0)
        print(strftime("%Y-%m-%d %H:%M:%S", gmtime()))
        print("whole time needed:", time_new - START_TIME)
        print(colored("--------------------------------", "red"))
    # print("saved in:")
    # csv_title = "evaluation/" + str(number_leafnodes) + " leafnodes - " + str(number_trees) + " trees - " + str(round(percentage_U * 100, 2)) + "% unknown.csv" 
    # print(csv_title)
    # with open(csv_title, 'w', newline='') as csvfile:
    #     writer = csv.writer(csvfile)
    #     writer.writerows(diffs)

    f_dif = 0.0
    m_dif = 0.0
    s_dif = 0.0
    for i in range(1, number_trees + 1):
        f_dif += float(diffs[i][0])
        m_dif += float(diffs[i][1])
        s_dif += float(diffs[i][2])
    f_dif = round(f_dif / number_trees, 2)
    m_dif = round(m_dif / number_trees, 2)
    s_dif = round(s_dif / number_trees, 2)

    row = [percentage_unknown, percentage_multifurcation, f_dif, m_dif, s_dif]
    csv_title = "data/simulation/" + str(int(percentage_parasites*100)) + "-unknown-multifurcation.csv"
    fp = open(csv_title, 'a')
    writer = csv.writer(fp)
    writer.writerow((row)) 
    fp.close()
    print("saved in:")
    print(csv_title)

    print(colored("--------------------------------", "green"))
    print(colored(number_trees, 'blue'), " trees simulated with", 
        colored(number_leafnodes, 'blue'), "leafnodes", 
        colored(percentage_parasites*100, 'blue'), "% parasites and",
        colored(percentage_unknown*100, 'blue'), "% unknown leafnodes and",
        colored(percentage_multifurcation*100, 'blue'), "% of multifurcation of the internal nodes.")
    print("correctly predicted (including already known leaf nodes):")
    print("differences Fitch / My / Sankoff")
    percentage_correctly_predicted = "| " + str(f_dif) +" % | " + str(m_dif) + " % | " + str(s_dif) + " % |"
    print(colored(percentage_correctly_predicted, 'red'))
    print(colored("--------------------------------", "green"))
    return

def run_parsimony_algorithms(current_tree, nodelist):
    global START_TIME
    global CURRENT_TIME
    CURRENT_TIME = datetime.datetime.now().replace(microsecond=0)
    print(colored("---------------- Fitch parsimony ----------------", "green"))
    fitch_MP_tree = deepcopy(current_tree)
    fitch_MP_nodelist = deepcopy(nodelist)
    fitch_parsimony(fitch_MP_tree.clade, fitch_MP_nodelist, 3)
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
    print(colored("-------- evaluation --------", "green"))
    differences = evaluation(nodelist, fitch_MP_nodelist, my_MP_nodelist, sankoff_MP_nodelist)
    CURRENT_TIME = print_time(CURRENT_TIME)
    print(colored("--------------------------------", "green"))
    return differences

def decide_for_beta_distribution_parameters():
    global percentage_parasites
                                # [A_FL, B_FL, A_P, B_P]
    beta_distribution_parameters = [7, 3.5, 3.5, 7]   # 40 P - 60 FL

    # decide for distribution:
    if percentage_parasites == 0.1:
        beta_distribution_parameters = [7, 24, 0.5, 7]     # 10 P - 90 FL
    elif percentage_parasites == 0.2:
        beta_distribution_parameters = [7, 13.25, 1.25, 7] # 20 P - 80 FL
    elif percentage_parasites == 0.3:
        beta_distribution_parameters = [7, 8.5, 2, 7]      # 30 P - 70 FL
    elif percentage_parasites == 0.4:
        beta_distribution_parameters = [7, 5.5, 2.75, 7]   # 40 P - 60 FL
    elif percentage_parasites == 0.5:
        beta_distribution_parameters = [7, 3.5, 3.5, 7]    # 50 P - 50 FL
    return beta_distribution_parameters

def evaluation(nodelist, fitch_MP_nodelist, my_MP_nodelist, sankoff_MP_nodelist):
    result_list = [['id','original tag', 'fitch', 'my', 'sankoff']]
    differences = [0, 0, 0]
    number_nodes = 0
    for i in range(0, len(nodelist)):
        real_value = nodelist[i][2]
        # ---------------- Fitch ----------------
        f_value = fitch_MP_nodelist[i][3]
        if f_value == '':
            fitch_MP_nodelist[i][3] = '-'
        else:
            number_nodes += 1
            if f_value == '0&1':
                f_value = 0.5
            f_value = float(f_value)
            differences[0] += abs(f_value - real_value)
        # ---------------- my max pars ----------------
        m_value = my_MP_nodelist[i][3]
        if m_value == '':
            my_MP_nodelist[i][3] = '-'
        else:
            m_value = float(m_value)
            differences[1] += abs(m_value - real_value)
        # ---------------- Sankoff ----------------
        s_value = sankoff_MP_nodelist[i][3]
        if s_value == '':
            sankoff_MP_nodelist[i][3] = '-'
        else:
            # s_value = float(s_value)
            differences[2] += abs(s_value - real_value)
        # --------------------------------
        result_list.append([nodelist[i][0], nodelist[i][2], fitch_MP_nodelist[i][3], my_MP_nodelist[i][3], sankoff_MP_nodelist[i][3]])

    with open('output.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(result_list)
    # pprint(result_list)
    differences[1] = round(differences[1], 2)
    differences[2] = round(differences[2], 2)
    f_dif_p = 100 - (differences[0] / number_nodes * 100)
    m_dif_p = 100 - (differences[1] / number_nodes * 100)
    s_dif_p = 100 - (differences[2] / number_nodes * 100)
    print(number_nodes)
    diff_percentage = [f_dif_p, m_dif_p, s_dif_p]
    return diff_percentage

def do_some_drawings(tree, nodelist, parsimony_tree, parsimony_nodelist):
    """seperated drawings"""
    tree.name = 'random tree'
    # Phylo.draw(tree)
    named_tree = deepcopy(tree)
    named_tree.name = 'tagged tree'
    tag_names(named_tree.clade, nodelist, 1)
    Phylo.draw(named_tree)
    untagged_tree = deepcopy(tree)
    untagged_tree.name = 'untagged tree'
    tag_leaf_names(untagged_tree.clade, nodelist)
    # Phylo.draw(untagged_tree)
    # tree.name = 'parsimony down'
    # Phylo.draw(tree)
    # tree.name = 'parsimony up'
    # Phylo.draw(tree)
    parsimony_tree.name = 'parsimonious solution tree'
    tag_names(parsimony_tree.clade, parsimony_nodelist, 2)
    Phylo.draw(parsimony_tree)
    parsimony_like_tree = deepcopy(tree)
    parsimony_like_tree.name = 'parsimonious-like solution tree'
    tag_names(parsimony_like_tree.clade, nodelist, 2)
    Phylo.draw(parsimony_like_tree)
    # Phylo.draw_graphviz(parsimony_tree)
    # pylab.show()

def metadata():
    leaf_nodes = 2300000        # 2 300 000 Eukaryota
    number_FL = 88967 #FL
    number_P = 43674 #P
    print("real OTL tree: 2 500 000 nodes: 240 000 internal,", leaf_nodes, "leaf nodes")
    print("Information about species from GloBI:", number_P, "#P,", number_FL, "#FL")
    percentage_P = 1 / leaf_nodes * number_P
    percentage_FL = 1 / leaf_nodes * number_FL
    percentage_U = 1 - percentage_P - percentage_FL
    print("=>", round(percentage_P * 100, 2), "% parasites,", round(percentage_FL * 100, 2), "% freeliving =>", round(percentage_U * 100, 2), "% unknown leaf nodes")
    return

main()
