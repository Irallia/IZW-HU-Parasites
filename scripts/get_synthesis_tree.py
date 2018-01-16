import csv
import datetime
from time import gmtime, strftime

from Bio import Phylo
from termcolor import colored

# path_tree = "../data/opentree9.1_tree/grafted_solution/grafted_solution.tre"
# path_tree = "../data/opentree9.1_tree/labelled_supertree/labelled_supertree_ottnames.tre"
path_tree = "../data/opentree9.1_tree/labelled_supertree/labelled_supertree.tre"

path_parasites = "../data/interaction_data/parasite.csv"
path_freelivings = "../data/interaction_data/freeliving.csv"

# global variables:
START_TIME = datetime.datetime.now().replace(microsecond=0)
CURRENT_TIME = datetime.datetime.now().replace(microsecond=0)
nr_leave_nodes = 0
nr_used_freelivings = 0
nr_used_parasites = 0
unknown = 0
internal_parasite = 0
internal_freeliving = 0

def main():
    global START_TIME
    global CURRENT_TIME
    global nr_leave_nodes
    global nr_used_freelivings
    global nr_used_parasites
    global unknown
    global internal_parasite
    global internal_freeliving

    print(colored("------------------------ start tree calculation ------------------------", "green"))
    print(strftime("%Y-%m-%d %H:%M:%S", gmtime()))
    CURRENT_TIME = print_time(START_TIME)
    print(colored("---------------- read tree ----------------", "green"))
    tree = Phylo.read(path_tree, 'newick')
    CURRENT_TIME = print_time(CURRENT_TIME)
    print(colored("---------------- read parasites and freelivings ----------------", "green"))
    print("Freelivings:")
    freelivings = read_tags(path_freelivings)
    print("Parasites:")
    parasites = read_tags(path_parasites)
    CURRENT_TIME = print_time(CURRENT_TIME)
    print(colored("---------------- tag tree ----------------", "green"))
    fill_tree_with_tags(tree.clade, parasites, freelivings)
    print(colored(nr_leave_nodes, 'blue'), "leave nodes are in the tree")
    print(colored(nr_used_freelivings, 'blue'), "freeliving tags were used,", colored(nr_used_parasites, 'blue'), "parasite tags were used =>", colored(unknown, 'blue'), "unknown leave nodes")
    print(colored(internal_freeliving, 'blue'), "internal freeliving tags found and", colored(internal_parasite, 'blue'), "internal parasite tags found")
    CURRENT_TIME = print_time(CURRENT_TIME)
    print("save tree at ../data/tagged_tree.tre")
    Phylo.write(tree, '../data/tagged_tree.tre', 'newick')
    print(colored("--------------------------------", "green"))
    return

def read_tags(path):
    tag_array = []
    nr_tags = 0
    with open(path) as csvfile:
        reader_f = csv.DictReader(csvfile)
        for row in reader_f:
            id_array = str.split(row['taxon_external_id'], ':')
            nr_tags += 1
            tag_array.append("ott" + id_array[1])
        print('number of tag:', nr_tags)
    return tag_array

def fill_tree_with_tags(subtree, parasites, freelivings):
    global nr_leave_nodes
    global nr_used_freelivings
    global nr_used_parasites
    global unknown
    global internal_parasite
    global internal_freeliving

    if subtree.is_terminal():
        nr_leave_nodes += 1
        if get_tag(subtree.name, parasites):
            subtree.name = "2"
            nr_used_parasites += 1
        else:
            if get_tag(subtree.name, freelivings):
                subtree.name = "1"
                nr_used_freelivings += 1
            else:
                subtree.name = "NA"
                unknown += 1
    else:
        if get_tag(subtree.name, parasites):
            internal_parasite += 1
        if get_tag(subtree.name, freelivings):
            internal_parasite += 1
        # // ToDo: ? does this make any difference?
        # subtree.name = ""
        for clade in subtree.clades:
            fill_tree_with_tags(clade, parasites, freelivings)
    return

def get_tag(name, species_list):
    # Checks for the presence of name in any string in the list
    name_ott = name + "ott"
    # if any(name in s for s in species_list):
    if any((s.endswith(name) or name_ott in s for s in species_list)):
        if name not in species_list:
            matching = [s for s in species_list if name in s]
            print(name, "in", matching)
        else:
            print("found tag:", name)
        return True
    else:
        return False

def print_time(time_old):
    time_new = datetime.datetime.now().replace(microsecond=0)
    # Text colors: grey, red, green, yellow, blue, magenta, cyan, white
    print(colored("time needed:", "magenta"), time_new - time_old)
    return time_new

main()
