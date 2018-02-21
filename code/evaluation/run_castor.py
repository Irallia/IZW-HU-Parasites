"""Maximum parsimony algorithm from Sankoff implemented in the R package castor"""

import csv
import datetime
from code.utilities.castor_util import sankoff_parsimony
from code.utilities.Helpers import find_element_in_nodelist, print_time
from time import gmtime, strftime

from Bio import Phylo
from termcolor import colored

# global variables:
START_TIME = datetime.datetime.now().replace(microsecond=0)
CURRENT_TIME = datetime.datetime.now().replace(microsecond=0)

print(colored("------------------------ Sankoff Maximum Parsimony ------------------------", "green"))

def run_castor(index, border):
    global START_TIME
    global CURRENT_TIME

    print('Run castor - Sankoff parsimony - for Eukaryota')
    print(colored("---------------- read tree ----------------", "green"))
    subtree_path = './data/subtree/Eukaryota.tre'
    tree = Phylo.read(subtree_path, 'newick')
    CURRENT_TIME = print_time(CURRENT_TIME)
    print(colored("---------------- read nodelist ----------------", "green"))
    nodelist_path = './data/evaluation/Eukaryota'+ index + '-' + str(border) +'.csv'
    #              0        1           2
    # nodelist - [id, originaltag, finaltag]
    nodelist = []
    with open(nodelist_path, 'r') as csv_file:
        reader = csv.reader(csv_file, delimiter=',')
        for row in reader:
            if row != []:
                ott = row[0]
                originaltag = row[1]
                finaltag = row[2]
                nodelist.append([ott, originaltag, finaltag])
    CURRENT_TIME = print_time(CURRENT_TIME)
    print(colored("---------------- Sankoff parsimony ----------------", "green"))
    sankoff_parsimony(tree, nodelist)
    CURRENT_TIME = print_time(CURRENT_TIME)
    print(colored("---------------- Save nodelist ----------------", "green"))
    nodelist_path = './data/evaluation/Eukaryota'+ index + '-' + str(border) +'-castor.csv'
    header = ['ott_id', 'originaltag', 'finaltag']
    with open(nodelist_path, 'w') as nodelist_file:
        writer = csv.writer(nodelist_file, delimiter=',')
        writer.writerow(header)
        for row in nodelist:
            writer.writerow(row)
    CURRENT_TIME = print_time(CURRENT_TIME)
    print(colored("--------------------------------", "green"))
    return
