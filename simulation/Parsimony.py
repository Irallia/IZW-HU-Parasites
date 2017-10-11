import Helpers

def parsimony(tree_clade, nodelist):
    """parsimony implemented from [COO98]"""
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
    left_child = Helpers.find_element_in_nodelist(subtree.clades[0].name, nodelist)
    right_child = Helpers.find_element_in_nodelist(subtree.clades[1].name, nodelist)
    # if not both children are tagged, first tag them:
    if left_child[3] == []:
        parsimony_down(subtree.clades[0], nodelist)
    if right_child[3] == []:
        parsimony_down(subtree.clades[1], nodelist)

    element = Helpers.find_element_in_nodelist(subtree.name, nodelist)

    l_tag = left_child[3][0]
    r_tag = right_child[3][0]
    shared = False
    # RULE 1: share any states in common -> assign shared states
    if ('FL' in l_tag) and ('FL' in r_tag):
        element[3].append('FL')
        shared = True
    if ('P' in l_tag) and ('P' in r_tag):
        if shared:
            element[3][0] = 'FL&P'
        else:
            element[3].append('P')
        shared = True
    # RULE 2: no shared states -> assign union of states
    if not shared:
        element[3].append('FL&P')
    return

def parsimony_up(subtree, nodelist, parent, sibling):
    """parsimony part: up direction -> from root to leafs"""
    # Arguments:
    #   subtree
    #   nodelist    - [id, originaltag, finaltag, calc[taglist]]
    #   parent      - nodelist element
    #   sibling     - nodelist element
    if not subtree.is_terminal():
        p_tag_1 = parent[3][0]
        p_tag_2 = 'FL&P'
        if  len(parent[3]) > 1:
            p_tag_2 = parent[3][1]
        s_tag_1 = sibling[3][0]
        s_tag_2 = 'FL&P'
        if  len(sibling[3]) > 1:
            p_tag_2 = sibling[3][1]
        element = Helpers.find_element_in_nodelist(subtree.name, nodelist)
        shared = False
        # RULE 1: share any states in common -> assign shared states
        if ('FL' in p_tag_1) and ('FL' in p_tag_2) and ('FL' in s_tag_1) and ('FL' in s_tag_2):
            element[3].append('FL')
            shared = True
        if ('P' in p_tag_1) and ('P' in p_tag_2) and ('P' in s_tag_1) and ('P' in s_tag_2):
            if shared:
                element[3][1] = 'FL&P'
            else:
                element[3].append('P')
            shared = True
        # RULE 2: no shared states -> assign union of states
        if not shared:
            element[3].append('FL&P')
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
    if not subtree.is_terminal():
        tags = element[3]
        if len(tags) > 1:
            shared = False
            # RULE 1: share any states in common -> assign shared states
            if ('FL' in tags[0]) and ('FL' in tags[1]):
                element[2] = 'FL'
                # subtree._set_color('blue')
                shared = True
            if ('P' in tags[0]) and ('P' in tags[1]):
                if shared:
                    element[2] = 'FL&P'
                    # subtree._set_color('magenta')
                else:
                    element[2] = 'P'
                    # subtree._set_color('red')
                shared = True
            # RULE 2: no shared states -> assign union of states
            if not shared:
                element[2] = 'FL&P'
                # subtree._set_color('magenta')
    else:
        element[2] = element[3][0]
    # go on with children
    if not subtree.is_terminal():
        parsimony_final(subtree.clades[0], nodelist)
        parsimony_final(subtree.clades[1], nodelist)
    return
