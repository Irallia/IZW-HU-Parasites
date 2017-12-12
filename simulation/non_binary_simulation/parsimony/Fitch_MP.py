from copy import deepcopy

from utilities import Helpers

# TAGS = ["FL", "P"]
TAGS = [0, 1]

def fitch_parsimony(tree_clade, nodelist):
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
        parsimony_up(clade, nodelist, parent, sublist)
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
    tag_list = get_intersect_or_union(child_tags)
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
    tag_list = get_intersect_or_union(siblings_tags)
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
        tag_list = get_intersect_or_union(element[4])
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

def get_intersect_or_union(tags_list):
    """returns the intersection of all list elements, if not empty"""
    # Arguments:
    #   tags_list - a list of tag_lists
    #       tags_list[tag_list]
    # pairwise intersection
    tag_set = []
    while len(tags_list) > 1:
        tag_list_i = tags_list[0]
        tag_list_j = tags_list[1]
        # RULE 1: share any states in common -> assign shared states
        # intersection:
        tag_set = (set(tag_list_i) & set(tag_list_j))
        # RULE 2: no shared states -> assign union of states
        if tag_set == set():
            # union:
            return TAGS
        else:
            tags_list.remove(tag_list_i) # same as 
            tags_list.remove(tag_list_j)
            tags_list.append(list(tag_set))
    return list(tag_set)
