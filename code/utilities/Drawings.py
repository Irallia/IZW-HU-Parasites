"""functions just for nice figures"""
from utilities import Helpers

def tag_names(subtree, nodelist, tag_id):
    """tag all nodes"""
    # Arguments:
    #   subtree
    #   nodelist      - [id, originaltag, finaltag, calc[taglist]]
    element = Helpers.find_element_in_nodelist(subtree.name, nodelist)
    subtree.name = element[tag_id]
    for clade in subtree.clades:
        tag_names(clade, nodelist, tag_id)
    return

def tag_leaf_names(subtree, nodelist):
    """tag all leafs"""
    # Arguments:
    #   subtree
    #   nodelist      - [id, originaltag, finaltag, calc[taglist]]
    if subtree.is_terminal():
        element = Helpers.find_element_in_nodelist(subtree.name, nodelist)
        subtree.name = element[1]
    else:
        subtree.name = ''
    for clade in subtree.clades:
        tag_leaf_names(clade, nodelist)
    return
