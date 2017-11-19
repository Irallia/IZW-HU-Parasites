# ## load phytools
# library(phytools)

# tree <- read.newick(file = "./tree/labelled_supertree/preparedTree.tre")
# # -> Phylogenetic tree with 228009 tips and 17871 internal nodes.

# ## ok, now let's re-root the tree at node ott304358
# # rr.ott93302 <- root(tree, node = ott304358)
# # rr.1 <- root(tree, node = 1)
# # plotTree(rr.ott304358)

# ## check if binary
# is.binary.tree(tree)
# ## [1] FALSE
# ## randomly resolve polytomies
# # binTree <- multi2di(tree)
# # plot(binTree, type = "cladogram")

# # collapse.singles.reversible(tree)
# collapse.singles(tree)

# plot(tree, type = "cladogram")



library(rotl)
apes <- c("Pongo", "Pan", "Gorilla", "Hoolock", "Homo")
(resolved_names <- tnrs_match_names(apes))

tr <- tol_induced_subtree(ott_ids=ott_id(resolved_names))
plot(tr)

# library(magrittr)
# ## or expressed as a pipe:
# c("Pongo", "Pan", "Gorilla", "Hoolock", "Homo") %>%
#     tnrs_match_names %>%
#     ott_id %>%
#     tol_induced_subtree %>%
#     plot