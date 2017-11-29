library(ape)
library(Rcpp)
library(castor)

path_tree <- "../../data/opentree9.1_tree/grafted_solution/grafted_solution.tre"
# path_tree = <- "../../data/opentree9.1_tree/labelled_supertree/labelled_supertree_ottnames.tre"
path_tagged_tree <- "../../data/tagged_tree.tre"

# read.tree(file = "", text = NULL, tree.names = NULL, skip = 0, comment.char = "", keep.multi = FALSE, ...)
tree <- read.tree(file = path_tree)
tagged_tree <- read.tree(path_tagged_tree)
# tree <- read.tree(text = "(((parasite,freeliving,parasite),(freeliving,freeliving)),freeliving);")
# states <- c("parasite", "freeliving", "parasite", NA, "freeliving")
states <- tagged_tree$tip.label
typeof(states)
# rapply(states, function(x) ifelse(x=="NA", NA, x), how = "replace")
gsub("NA", NA, states)
# print(states)

# # map_to_state_space(raw_states, fill_gaps=FALSE, sort_order="natural", include_state_values=FALSE)
mapping <- map_to_state_space(states)
tip_states <- mapping$mapped_states
# print(tip_states)

# asr_max_parsimony(tree, tip_states, Nstates=2, transition_costs="all_equal", edge_exponent=0, weight_by_scenarios=TRUE, check_input=TRUE)

hsp_max_parsimony(tree, tip_states, Nstates=2, transition_costs="all_equal", edge_exponent=0.0, weight_by_scenarios=TRUE, check_input=TRUE)
