library(ape)
library(Rcpp)
library(castor)

# -------- Tree: --------
path_tree <- "code/bufferfiles/simulated_tree.tre"
# read.tree(file = "", text = NULL, tree.names = NULL, skip = 0, comment.char = "", keep.multi = FALSE, ...)
tree <- read.tree(path_tree)

# -------- Tagged tree: --------
path_tagged_tree <- "code/bufferfiles/simulated_tagged_tree.tre"
tagged_tree <- read.tree(path_tagged_tree)

# ---- get the tagged tips of the tree ----
state_ids <- tree$tip.label
states <- tagged_tree$tip.label
# print("tip states:")
# print(states)
# print(state_ids)
number_of_tips <- length(state_ids)
internal_nodes <- tree$node.label

# ---- map them to numbers (NA for unknown states) ----
# map_to_state_space(raw_states, fill_gaps=FALSE, sort_order="natural", include_state_values=FALSE)
mapping <- map_to_state_space(states, include_state_values = TRUE)
tip_states <- mapping$mapped_states
# print("State names:")
# print(mapping$state_names)
x <- replace(tip_states, tip_states==3, NA)
# print("run parsimony algorithm...")

# ---- run parsimony algorithm ----
# Reconstruct ancestral discrete states of nodes and predict unknown (hidden) states of tips on a tree using maximum parsimony. Transition costs can vary between transitions, and can optionally be weighted by edge length.
likelihoods = hsp_max_parsimony(tree, tip_states, Nstates=3, transition_costs="all_equal", edge_exponent=0.0, weight_by_scenarios=TRUE, check_input=TRUE)
