library(ape)
library(Rcpp)
library(castor)

# -------- Original tree: --------
# path_tree <- "../../data/opentree9.1_tree/grafted_solution/grafted_solution.tre"
# path_tree <- "../../data/opentree9.1_tree/labelled_supertree/labelled_supertree_ottnames.tre"
# tree <- read.tree(file = path_tree)

# -------- Tagged tree: --------
path_tagged_tree <- "../../data/tagged_tree.tre"
# read.tree(file = "", text = NULL, tree.names = NULL, skip = 0, comment.char = "", keep.multi = FALSE, ...)
tagged_tree <- read.tree(path_tagged_tree)

# ---- get the tagged tips of the tree ----
states <- tagged_tree$tip.label
# print(states)

# ---- map them to numbers (NA for unknown states) ----
# map_to_state_space(raw_states, fill_gaps=FALSE, sort_order="natural", include_state_values=FALSE)
mapping <- map_to_state_space(states, include_state_values = TRUE)
tip_states <- mapping$mapped_states
print("State names:")
print(mapping$state_names)
x <- replace(tip_states, tip_states==3, NA)
# print(tip_states)

print("run parsimony algorithm...")

# ---- run parsimony algorithm ----
# Reconstruct ancestral discrete states of nodes and predict unknown (hidden) states of tips on a tree using maximum parsimony. Transition costs can vary between transitions, and can optionally be weighted by edge length.
# likelihoods = hsp_max_parsimony(tree, tip_states, Nstates=2, transition_costs="all_equal", edge_exponent=0.0, weight_by_scenarios=TRUE, check_input=TRUE)
likelihoods = hsp_max_parsimony(tagged_tree, tip_states, Nstates=NULL, transition_costs="all_equal", edge_exponent=0.0, weight_by_scenarios=TRUE, check_input=TRUE)
print("--------")
print(likelihoods)
# estimated_tip_states = max.col(likelihoods[1:Ntips,])
# # print estimated tip states
# print(estimated_tip_states)