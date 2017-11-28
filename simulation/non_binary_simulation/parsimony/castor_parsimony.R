library(ape)
library(Rcpp)
library(castor)

tree <- read.tree(text = "(((parasite,freeliving,parasite),(freeliving,freeliving)),freeliving);")
# states <- c("parasite", "freeliving", "parasite", NA, "freeliving")
states <- tree$tip.label
plot(tree, edge.width = 2)
tiplabels()
nodelabels()

# map_to_state_space(raw_states, fill_gaps=FALSE, sort_order="natural", include_state_values=FALSE)
mapping <- map_to_state_space(states)

tip_states <- mapping$mapped_states
print(tip_states)

asr_max_parsimony(tree, tip_states, Nstates=2, transition_costs="all_equal", edge_exponent=0, weight_by_scenarios=TRUE, check_input=TRUE)

hsp_max_parsimony(tree, tip_states, Nstates=2, transition_costs="all_equal", edge_exponent=0.0, weight_by_scenarios=TRUE, check_input=TRUE)
