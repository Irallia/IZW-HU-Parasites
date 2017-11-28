import Helpers

def my_parsimony(tree_clade, nodelist):
    """mean based parsimony"""
    # down:
    parsimony_down(tree_clade, nodelist)
    # up:
    parent = Helpers.find_element_in_nodelist(tree_clade.name, nodelist)
    left_child = Helpers.find_element_in_nodelist(tree_clade.clades[0].name, nodelist)
    right_child = Helpers.find_element_in_nodelist(tree_clade.clades[1].name, nodelist)
    parsimony_up(tree_clade.clades[0], nodelist, parent, right_child)
    parsimony_up(tree_clade.clades[1], nodelist, parent, left_child)
    # final:
    parsimony_final(tree_clade, nodelist)
    return

def parsimony_down(subtree, nodelist):
    """parsimony part: down direction -> from leafs to root"""
    # Arguments:
    #   subtree
    #   nodelist      - [id, originaltag, finaltag, calc[taglist]]
    element = Helpers.find_element_in_nodelist(subtree.name, nodelist)
    left_child = Helpers.find_element_in_nodelist(subtree.clades[0].name, nodelist)
    right_child = Helpers.find_element_in_nodelist(subtree.clades[1].name, nodelist)
    # if not both children are tagged, first tag them:
    if left_child[3] == []:
        parsimony_down(subtree.clades[0], nodelist)
    if right_child[3] == []:
        parsimony_down(subtree.clades[1], nodelist)
    # if leafs:
    if subtree.clades[0].is_terminal():
        if left_child[3][0] == 'FL':
            left_child[3][0] = 1
        else:
            left_child[3][0] = 0
    if subtree.clades[1].is_terminal():
        if right_child[3][0] == 'FL':
            right_child[3][0] = 1
        else:
            right_child[3][0] = 0
    # calculate mean
    mean = (left_child[3][0] + right_child[3][0]) / 2
    element[3].append(mean)
    return

def parsimony_up(subtree, nodelist, parent, sibling):
    """parsimony part: up direction -> from root to leafs"""
    # Arguments:
    #   subtree
    #   nodelist    - [id, originaltag, finaltag, calc[taglist]]
    #   parent      - nodelist element
    #   sibling     - nodelist element
    if not subtree.is_terminal():
        element = Helpers.find_element_in_nodelist(subtree.name, nodelist)
        # calculate mean
        joined_tags = parent[3] + sibling[3]
        mean = sum(joined_tags) / len(joined_tags)
        element[3].append(mean)
        # go on with children
        left_child = Helpers.find_element_in_nodelist(subtree.clades[0].name, nodelist)
        right_child = Helpers.find_element_in_nodelist(subtree.clades[1].name, nodelist)
        parsimony_up(subtree.clades[0], nodelist, element, right_child)
        parsimony_up(subtree.clades[1], nodelist, element, left_child)
    return

def parsimony_final(subtree, nodelist):
    """parsimony final part: combine multiple tags of node to one final tag"""
    # Arguments:
    #   subtree
    #   nodelist      - [id, originaltag, finaltag, calc[taglist]]
    element = Helpers.find_element_in_nodelist(subtree.name, nodelist)
    # calculate mean
    mean = sum(element[3]) / len(element[3])
    element[2] = str(round(mean,2))
    # colouring:
    # if mean > 0.5:
    #     subtree._set_color('blue')
    # if mean < 0.5:
    #     subtree._set_color('red')
    # else:
    #     subtree._set_color('magenta')
    # go on with children
    if not subtree.is_terminal():
        parsimony_final(subtree.clades[0], nodelist)
        parsimony_final(subtree.clades[1], nodelist)
    return
