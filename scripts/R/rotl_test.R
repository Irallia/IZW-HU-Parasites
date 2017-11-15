library(rotl)

print("------------------------Hyla, Salmo, Diadema, Nautilu--------------------------------")

# Step 1: Matching taxonomy to the ott_id
# taxa <-c("Ceratias", "Homo", "Molothrus")
taxa <- c("Hyla", "Salmo", "Diadema", "Nautilus")
# resolved_names <- tnrs_match_names(taxa)
# To ensure that our search is limited to animal names, we could do:
#   Check possible values using: tnrs_contexts()
resolved_names <- tnrs_match_names(taxa, context_name = "Animals")
resolved_names

print("-------------------------------------------------------------------------------------")

# Step 2: Getting the tree corresponding to our taxa
my_tree <- tol_induced_subtree(ott_ids = resolved_names$ott_id)
plot(my_tree, no.margin=TRUE)

print("-------------------------------------------------------------------------------------")

# How to change the ott ids assigned to my taxa?
inspect(resolved_names, taxon_name = "diadema")
resolved_names <- update(resolved_names, taxon_name = "diadema", new_row_number = 2)

print("-------------------------------------------------------------------------------------")

# How do I know that the taxa I’m asking for is the correct one?
diadema_info <- taxonomy_taxon_info(631176)
tax_rank(diadema_info)

print("-------------------------------------------------------------------------------------")

synonyms(diadema_info)

print("-------------------------------------------------------------------------------------")

# In some cases, it might also be useful to investigate the taxonomic tree descending from an ott_id to check that it’s the correct taxon and to determine the species included in the Open Tree Taxonomy:

diadema_tax_tree <- taxonomy_subtree(631176)
diadema_tax_tree

print("-------------------------------------------------------------------------------------")

# How do I get the tree for a particular taxonomic group?

# If you are looking to get the tree for a particular taxonomic group, you need to first identify it by its node id or ott id, and then use the tol_subtree() function:

mono_id <- tnrs_match_names("Monotremata")
mono_tree <- tol_subtree(ott_id = ott_id(mono_id))

## Warning in collapse_singles(tr): Dropping singleton nodes with labels:
## Ornithorhynchidae ott344066, Ornithorhynchus ott962391, Tachyglossus
## ott16047, Tachyglossus aculeatus ott16038

plot(mono_tree)