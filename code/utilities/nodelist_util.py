import csv


current_freelivings = []
current_parasites = []

def read_tags(path):
    tag_array = []
    nr_tags = 0
    with open(path) as csv_file:
        reader = csv.reader(csv_file, delimiter=',')
        for row in reader:
            if row != []:
                id_array = row[0]
                nr_tags += 1
                tag_array.append("ott" + id_array)
        print('number of tag:', nr_tags)
    return tag_array

def tag_node(nodelist, current_list_index, ott, species_lists, stats):
    #                   0    1              2       3       4           5
    # nodelist      - [id, originaltag, finaltag, depth, heights, nr_children]
    # current_list_index - index of current node
    # ott
    # species_lists - [freelivings, parasites]
    # stats         - [nr_leave_nodes, nr_used_parasites, nr_used_freelivings, unknown, doubleTagged]
    
    global current_freelivings
    global current_parasites
    current_freelivings = species_lists[0]
    current_parasites = species_lists[1]

    nr_leave_nodes = stats[0]
    nr_used_parasites = stats[1]
    nr_used_freelivings = stats[2]
    unknown = stats[3]
    doubleTagged = stats[4]

    nr_leave_nodes += 1
    tag_boolp = get_tag(ott, 'P')
    if tag_boolp:
        nr_used_parasites += 1
        nodelist[current_list_index][1] = "2"
        if (get_tag(ott, 'FL')):
            doubleTagged += 1
    else:
        tag_boolf = get_tag(ott, 'FL')
        if tag_boolf:
            nr_used_freelivings += 1
            nodelist[current_list_index][1] = "1"
        else:
            nodelist[current_list_index][1] = "NA"
            unknown += 1
    return

def get_tag(name, tag):
    global current_freelivings
    global current_parasites
    if tag == 'FL':
        species_list = current_freelivings
    else:
        species_list = current_parasites
    # Checks for the presence of name in any string in the list
    for item in species_list:
        # mrcaott_item = 'mrca' + item + 'ott'
        if item == name or name.endswith(item): # or name.startswith(mrcaott_item):
            species_list.remove(item)
            return True
    return False