import csv
import sys
from copy import deepcopy
from pprint import pprint

from Bio import Phylo

# input arguments
args = sys.argv

# values from  input:
taxa = sys.argv[1]

# global variables:
taxa_otts = []
current_ott_list = []
taxa_mapping = []

def main():
    global taxa_otts
    global taxa_mapping

    with open('./data/interaction_data/ott_taxa.csv') as csv_file:
        reader = csv.reader(csv_file, delimiter=',')
        # row: ott_id, name, rank, uniqname
        for row in reader:
            if row != []:
                if row[2] == taxa:
                    taxa_otts.append([row[0], row[1]])
                # else:
                #     row_string = ",".join(str(x) for x in row)
                #     if taxa in row_string:
                #         print(row)
            
    print('all', taxa, ': ', len(taxa_otts))
    nr_taxa = len(taxa_otts)

    subtree_path = './data/subtree/Eukaryota.tre'
    tree = Phylo.read(subtree_path, 'newick')
    find_subtree(tree.clade)
    print(nr_taxa - len(taxa_otts))
    nr_taxa = len(taxa_otts)

    header = ['ott_id', taxa]
    path = './data/nodelist/Eukaryota-' + taxa + '_mapping.csv'
    with open(path, 'w') as fp:
        writer = csv.writer(fp, delimiter=',')
        writer.writerow(header)
        for row in taxa_mapping:
            writer.writerow(row)

    print('find', taxa, '2...')
    find_subtree(tree.clade)
    print(nr_taxa - len(taxa_otts))
    nr_taxa = len(taxa_otts)

    header_taxa = taxa + '2'
    header = ['ott_id', header_taxa]
    path = './data/nodelist/Eukaryota-' + taxa + '2_mapping.csv'
    with open(path, 'w') as fp:
        writer = csv.writer(fp, delimiter=',')
        writer.writerow(header)
        for row in taxa_mapping:
            writer.writerow(row)

    print('find', taxa, '3...')
    find_subtree(tree.clade)
    print(nr_taxa - len(taxa_otts))
    nr_taxa = len(taxa_otts)

    header_taxa = taxa + '3'
    header = ['ott_id', header_taxa]
    path = './data/nodelist/Eukaryota-' + taxa + '3_mapping.csv'
    with open(path, 'w') as fp:
        writer = csv.writer(fp, delimiter=',')
        writer.writerow(header)
        for row in taxa_mapping:
            writer.writerow(row)

    # pprint(taxa_otts)

    print(len(taxa_otts), 'taxa not found')

    return

def find_subtree(subtree):
    global taxa_otts
    
    if len(taxa_otts) == 0:
        return
    
    for ott_name in taxa_otts:
        if subtree.name.split("$")[0] == ott_name[0]:  # is taxa?
            get_all_nodes(subtree, ott_name)
            taxa_otts.remove(ott_name)
            return
    if not subtree.is_terminal():
        for clade in subtree.clades:
            find_subtree(clade)
    return

def get_all_nodes(subtree, ott_name):
    global taxa_mapping
    taxa_mapping.append([subtree.name.split("$")[0], ott_name])
    if not subtree.is_terminal():
        for clade in subtree.clades:
            get_all_nodes(clade, ott_name)
    return

main()
