"""Maximum parsimony algorithm from Sankoff implemented in the R package castor"""

import rpy2.robjects

def sankoff_parsimony(tree_clade, nodelist):
    """Using rpy2 for forwarding to R code"""
    newick_tree = "(((parasite,freeliving,parasite),(freeliving,freeliving)),freeliving);"

    # -------- R code --------
    
    path = "D:/GitHub/IZW-HU-Parasites/scripts/R/castor_parsimony.R"
    f = open(path, "r")
    code = ''.join(f.readlines())
    result = rpy2.robjects.r(code)
    # assume that...
    X = rpy2.robjects.globalenv['X']
    # r = robjects.r
    # r['source']("castor_parsimony.R")
    # r.source("castor_parsimony.R")
    # r["myfunction(newick_tree)"]

    # robjects.r("""source('castor_parsimony.R')""")

    # r["library(ape)"]
    # r["library(Rcpp)"]
    # r["library(castor)"]

    # r["tree <- read.tree(text = '(((parasite,freeliving,parasite),(freeliving,freeliving)),freeliving);)'"]
    # # states <- c("parasite", "freeliving", "parasite", NA, "freeliving")

    # r["states <- tree$tip.label"]
    # r["plot(tree, edge.width = 2)"]
    # r["tiplabels()"]
    # r["nodelabels()"]
    # # map_to_state_space(raw_states, fill_gaps=FALSE, sort_order="natural", include_state_values=FALSE)
    # r["mapping <- map_to_state_space(states)"]
    # r["tip_states <- mapping$mapped_states"]
    # r["print(tip_states)"]
    # # Tips must be represented in tip_states in the same order as in tree$tip.label. None of the input vectors or matrixes need include row or column names; if they do, however, they are checked for consistency (if check_input==TRUE).

    # r["asr_max_parsimony(tree, tip_states, Nstates=2, transition_costs='all_equal', edge_exponent=0, weight_by_scenarios=TRUE, check_input=TRUE)"]
    # r["hsp_max_parsimony(tree, tip_states, Nstates=2, transition_costs='all_equal', edge_exponent=0.0, weight_by_scenarios=TRUE, check_input=TRUE)"]



    return