from copy import deepcopy

from utilities import Fitch_Versions, Helpers

def fitch_parsimony(tree_clade, nodelist, version):
    """parsimony implemented from [COO98] - changed for multifurcating trees"""
    # down:
    parsimony_down(tree_clade, nodelist)
    # up:
    parent = Helpers.find_element_in_nodelist(tree_clade.name, nodelist)
    children = []
    for clade in tree_clade.clades:
        child = Helpers.find_element_in_nodelist(clade.name, nodelist)
        children.append(child)
    for i in range(0, len(tree_clade.clades)):
        clade = tree_clade.clades[i]
        child = Helpers.find_element_in_nodelist(clade.name, nodelist)
        sublist = deepcopy(children)
        del sublist[i]
        # ToDo: decide which one, next ToDo: a second parsimony down?
        Fitch_Versions.parsimony_up(clade, nodelist, parent, sublist, version)
    # final:
    parsimony_final(tree_clade, nodelist)
    return

def parsimony_down(subtree, nodelist):
    """parsimony part: down direction -> from leafs to root"""
    # Arguments:
    #   subtree
    #                   0   1       2           3           4
    #   nodelist    - [id, depth, originaltag, finaltag, calc[taglist]]
    child_tags = []
    for clade in subtree.clades:
        child = Helpers.find_element_in_nodelist(clade.name, nodelist)
        # if child is not tagged, first tag it:
        if child[4] == []:
            parsimony_down(clade, nodelist)
        child_tags.append(child[4][0])
    element = Helpers.find_element_in_nodelist(subtree.name, nodelist)
    # get intersection or union
    tag_list = Helpers.get_intersect_or_union(child_tags)
    # add new tag
    element[4].append(tag_list)
    return

def parsimony_up(subtree, nodelist, parent, siblings):
    """parsimony part: up direction -> from root to leafs"""
    # Arguments:
    #   subtree
    #                   0   1       2           3           4
    #   nodelist    - [id, depth, originaltag, finaltag, calc[taglist]]
    #   parent      - nodelist element
    #   siblings     - [nodelist element]
    element = Helpers.find_element_in_nodelist(subtree.name, nodelist)

    parent_tag = parent[4]  # parent[4] could look like [['0', '1'], ['1']] or [['1']]
    siblings_tags = []
    siblings_tags += parent_tag
    for sibling in siblings:
        siblings_tags += sibling[4]
    
    # get intersection or union
    tag_list = Helpers.get_intersect_or_union(siblings_tags)
    # add new tag
    element[4].append(tag_list)

    # go on with children
    if not subtree.is_terminal():
        children = []
        for clade in subtree.clades:
            child = Helpers.find_element_in_nodelist(clade.name, nodelist)
            children.append(child)
        for i in range(0, len(subtree.clades)):
            clade = subtree.clades[i]
            child = Helpers.find_element_in_nodelist(clade.name, nodelist)
            sublist = deepcopy(children)
            del sublist[i]
            parsimony_up(clade, nodelist, element, sublist)
    return

def parsimony_final(subtree, nodelist):
    """parsimony final part: combine multiple tags of node to one final tag"""
    # Arguments:
    #   subtree
    #                   0   1       2           3           4
    #   nodelist    - [id, depth, originaltag, finaltag, calc[taglist]]
    element = Helpers.find_element_in_nodelist(subtree.name, nodelist)
    if subtree.is_terminal() and len(element[4][0]) == 1:
        element[3] = element[4][0][0]
    else:
        # get intersection or union
        tag_list = Helpers.get_intersect_or_union(element[4])
        # add final tag
        tag_string = ""
        for tag in tag_list:
            tag_string += str(tag) + "&"
        tag_string = tag_string[:len(tag_string)-1]
        element[3] = tag_string
    # go on with children
    if not subtree.is_terminal(): 
        for clade in subtree.clades:
            parsimony_final(clade, nodelist)
    return
