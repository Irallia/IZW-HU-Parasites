# from Bio import Phylo

def parsimony(subtree):
# def parsimony(subtree, tree):
    # down:
    parsimony_down(subtree)
    # tree.name = 'parsimony down'
    # Phylo.draw(tree)
    # up:
    parsimony_up(subtree.clades[0], subtree.name, subtree.clades[1].name)
    parsimony_up(subtree.clades[1], subtree.name, subtree.clades[0].name)
    # tree.name = 'parsimony up'
    # Phylo.draw(tree)
    # final:
    parsimony_final(subtree)
    return

def parsimony_down(subtree):
    """parsimony part: down direction -> from leafs to root"""
    clade0_name = subtree.clades[0].name.split('-')
    clade1_name = subtree.clades[1].name.split('-')
    if len(clade0_name) == 1:
        parsimony_down(subtree.clades[0])
        clade0_name = subtree.clades[0].name.split('-')
    if len(clade1_name) == 1:
        parsimony_down(subtree.clades[1])
        clade1_name = subtree.clades[1].name.split('-')
    l_tag = clade0_name[1]
    r_tag = clade1_name[1]
    shared = False
    # RULE 1: share any states in common -> assign shared states
    if ('FL' in l_tag) & ('FL' in r_tag):
        subtree.name = subtree.name + '-FL'
        shared = True
    if ('P' in l_tag) & ('P' in r_tag):
        if shared:
            subtree.name = subtree.name + '&P'
        else:
            subtree.name = subtree.name + '-P'
        shared = True
    # RULE 2: no shared states -> assign union of states
    if not shared:
        subtree.name = subtree.name + '-FL&P'
    return

def parsimony_up(subtree, parent_name, siblings_name):
    """parsimony part: up direction -> from root to leafs"""
    if not subtree.is_terminal():
        p_tag_1 = parent_name.split('-')[1]
        p_tag_2 = 'FL&P'
        if  len(parent_name.split('-')) > 2:
            p_tag_2 = parent_name.split('-')[2]
        s_tag_1 = siblings_name.split('-')[1]
        s_tag_2 = 'FL&P'
        if len(siblings_name.split('-')) > 2:
            s_tag_2 = siblings_name.split('-')[2]
        shared = False
        # RULE 1: share any states in common -> assign shared states
        if ('FL' in p_tag_1) & ('FL' in p_tag_2) & ('FL' in s_tag_1) & ('FL' in s_tag_2):
            subtree.name = subtree.name + '-FL'
            shared = True
        if ('P' in p_tag_1) & ('P' in p_tag_2) & ('P' in s_tag_1) & ('P' in s_tag_2):
            if shared:
                subtree.name = subtree.name + '&P'
            else:
                subtree.name = subtree.name + '-P'
            shared = True
        # RULE 2: no shared states -> assign union of states
        if not shared:
            subtree.name = subtree.name + '-FL&P'
        # go on with children
        parsimony_up(subtree.clades[0], subtree.name, subtree.clades[1].name)
        parsimony_up(subtree.clades[1], subtree.name, subtree.clades[0].name)
    return

def parsimony_final(subtree):
    """parsimony final part: combine multiple tags of node to one final tag"""
    if not subtree.is_terminal():
        tags = subtree.name.split('-')
        if len(tags) > 2:
            shared = False
            # RULE 1: share any states in common -> assign shared states
            if ('FL' in tags[1]) & ('FL' in tags[2]):
                subtree.name = tags[0] + '-FL'
                # subtree._set_color('blue')
                shared = True
            if ('P' in tags[1]) & ('P' in tags[2]):
                if shared:
                    subtree.name = subtree.name + '&P'
                    # subtree._set_color('magenta')
                else:
                    subtree.name = tags[0] + '-P'
                    # subtree._set_color('red')
                shared = True
            # RULE 2: no shared states -> assign union of states
            if not shared:
                subtree.name = tags[0] + '-FL&P'
                # subtree._set_color('magenta')
    # go on with children
    if not subtree.is_terminal():
        parsimony_final(subtree.clades[0])
        parsimony_final(subtree.clades[1])
    return
