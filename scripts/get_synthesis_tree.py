from Bio import Phylo
import csv

path_tree = "../data/opentree9.1_tree/grafted_solution/grafted_solution.tre"
# path_tree = "../data/opentree9.1_tree/labelled_supertree/labelled_supertree_ottnames.tre"

path_parasites = "../data/interaction_data/parasite.csv"
path_freelivings = "../data/interaction_data/freeliving.csv"

def main():
    tree = Phylo.read(path_tree, 'newick')
    print("tree name: ", tree.clade.name)
    print("first clades: ")
    for clade in tree.clade.clades:
        print(clade.name)

    parasites = []
    freelivings = []

    with open(path_parasites) as csvfile:
        reader_p = csv.DictReader(csvfile)
        for row in reader_p:
            id_array = str.split(row['taxon_external_id'], ':')
            if id_array[0] == "OTT":
                parasites.append("ott" + id_array[1])
        #     print(row['taxon_external_id'], row['taxon_name'])

    with open(path_freelivings) as csvfile:
        reader_f = csv.DictReader(csvfile)
        for row in reader_f:
            id_array = str.split(row['taxon_external_id'], ':')
            if id_array[0] == "OTT":
                freelivings.append("ott" + id_array[1])
        #     print(row['taxon_external_id'], row['taxon_name'])
    
    fill_tree_with_tags(tree.clade, parasites, freelivings)

    Phylo.write(tree, '../data/tagged_tree.tre', 'newick')

    return

def fill_tree_with_tags(subtree, parasites, freelivings):
    if subtree.is_terminal():
        if get_tag(subtree.name, parasites):
            subtree.name = "parasite"
            print("found parasite")
        else:
            if get_tag(subtree.name, freelivings):
                subtree.name = "freeliving"
                print("found freeliving")
            else:
                subtree.name = "NA"
    else:
        for clade in subtree.clades:
            fill_tree_with_tags(clade, parasites, freelivings)
    return

def get_tag(name, species_list):
    if name in species_list:
        return True
    else:
        return False

main()