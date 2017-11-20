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
# Tips must be represented in tip_states in the same order as in tree$tip.label. None of the input vectors or matrixes need include row or column names; if they do, however, they are checked for consistency (if check_input==TRUE).

### asr_max_parsimony - Maximum-parsimony ancestral state reconstruction.
## Description:
# Reconstruct ancestral states for a discrete trait using maximum parsimony. Transition costs can vary between 
# transitions, and can optionally be weighted by edge length.
# The function then applies Sankoff’s (1975) dynamic programming algorithm for ancestral state reconstruction,
# which determinesthesmallestnumber(orleastcostlyiftransitioncostsareuneven)ofstatechangesalong edges needed 
# to reproduce the known tip states. The state probabilities of tips with unknown state are set to those of 
# the most recent ancestor with reconstructed states, as described by Zanefeld and Thurber (2014). This 
# function has asymptotic time complexity O(Ntips+Nnodes x Nstates). 
asr_max_parsimony(tree, tip_states, Nstates=2, transition_costs="all_equal", edge_exponent=0, weight_by_scenarios=TRUE, check_input=TRUE)
### hsp_max_parsimony - Hidden state prediction via maximum parsimony.
## Description:
# Reconstruct ancestral discrete states of nodes and predict unknown (hidden) states of tips on a tree using 
# maximum parsimony. Transition costs can vary between transitions, and can optionally be weighted by edge 
# length.
hsp_max_parsimony(tree, tip_states, Nstates=2, transition_costs="all_equal", edge_exponent=0.0, weight_by_scenarios=TRUE, check_input=TRUE)
# This function is meant for reconstructing ancestral states in all nodes of a tree as well as predicting the states of tips with an a priory unknown state. If the state of all tips is known and only ancestral state reconstruction is needed, consider using the function asr_max_parsimony for improved efﬁciency.



# Arguments:
#     tree - A rooted tree of class "phylo". The root is assumed to be the unique node with no incoming edge.
#     tip_states - An integer vector of size Ntips, specifying the state of each tip in the tree as an integer 
#         from 1 to Nstates, where Nstates is the possible number of states (see below).
#         [...] Any NA entries in tip_states are interpreted as unknown states.  Prior to ancestral state 
#         reconstruction, the tree is temporarily prunned, keeping only tips with known state.[...]
#     Nstates -  Either NULL, or an integer specifying the number of possible states of the trait. If NULL, 
#         then Nstates will be computed based on the maximum value encountered in tip_states
#     transition_costs - Either "all_equal", "sequential", "proportional", "exponential", or a quadratic 
#         non-negatively valued matrix of size Nstates x Nstates, specifying the transition costs between all 
#         possible states (which can include 0 as well as Inf). The [r,c]-th entry of the matrix is the cost 
#         of transitioning from state r to state c.
#         The option "all_equal" specifies that all transitions are permitted and are equally costly. [...]
#     edge_exponent - Non-negative real-valued number. Optional exponent for weighting transition costs by 
#         the inverse length of edge lengths. If 0, edge lengths do not influence the ancestral state 
#         reconstruction (this is the conventional max-parsimony). [...]
#     weight_by_scenarios - Logical, indicating whether to weight each optimal state of a node by the number 
#         of optimal maximum-parsimony scenarios in which the node is in that state. If FALSE, then all 
#         optimal states of a node are weighted equally (i.e. are assigned equal probabilities).
#     check_input - Logical, specifying whether to perform some basic checks on the validity of the input 
#         data. If you are certain that your input data are valid, you can set this to FALSE to reduce 
#         computation.


# ## Examples

# # generate random tree
# Ntips = 10
# tree = generate_random_tree(list(birth_rate_intercept=1),max_tips=Ntips)$tree

# # simulate a discrete trait
# Nstates = 5
# Q = get_random_mk_transition_matrix(Nstates, rate_model="ER")
# tip_states = simulate_mk_model(tree, Q)$tip_states

# # print tip states
# print(tip_states)

# # set half of the tips to unknown state
# tip_states[sample.int(Ntips,size=as.integer(Ntips/2),replace=FALSE)] = NA

# # reconstruct all tip states via MPR
# likelihoods = hsp_max_parsimony(tree, tip_states, Nstates)$likelihoods
# estimated_tip_states = max.col(likelihoods[1:Ntips,])

# # print estimated tip states
# print(estimated_tip_states)