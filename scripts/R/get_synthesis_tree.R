library(rotl)

# tol_subtree(ott_id = NULL, node_id = NULL, label_format = NULL, file, ...)
# Eukaryota:
# id <- tnrs_match_names("Eukaryota")
# tree <- tol_subtree(ott_id = ott_id(id))
# tree <- tol_subtree(ott_id = 304358)
# Metazoa:
# id <- tnrs_match_names("Metazoa")
# tree <- tol_subtree(ott_id = ott_id(id))

# plot(tree)


mono_id <- tnrs_match_names("Monotremata")
mono_tree <- tol_subtree(ott_id = ott_id(mono_id))
## Warning in collapse_singles(tr): Dropping singleton nodes with labels:
## Ornithorhynchidae ott344066, Ornithorhynchus ott962391, Tachyglossus
## ott16047, Tachyglossus aculeatus ott16038
plot(mono_tree)


# taxa <- c("Hyla", "Salmo", "Diadema", "Nautilus")
# # resolved_names <- tnrs_match_names(taxa)

# resolved_names <- tnrs_match_names(taxa, context_name = "Animals")

# my_tree <- tol_induced_subtree(ott_ids = resolved_names$ott_id)
# plot(my_tree, no.margin=TRUE)