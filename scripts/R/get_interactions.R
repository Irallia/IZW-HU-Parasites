library(rglobi)

# List interactions identified in GloBI database
# get_interaction_types()
get_interaction_types(opts = list())

print("-------- Parasites: --------")
# parasites source
# Unsupported interaction type(s): ectoParasiteOf, kleptoparasiteOf, ectoParasitoid, endoparasiteOf, parasitoidOf, endoparasitoidOf
parasite_source <- c("parasiteOf", "pathogenOf")
ps_data <- get_interactions_by_type(interactiontype = parasite_source)
ps_data <- ps_data[c(1:2)]
colnames(ps_data) <- c("taxon_external_id", "taxon_name")

# parasites target
parasite_target <- c("hasParasite", "hasPathogen")
pt_data <- get_interactions_by_type(interactiontype = parasite_target)
pt_data <- pt_data[c(6:7)]
colnames(pt_data) <- c("taxon_external_id", "taxon_name")

# parasite
p_data <- rbind(ps_data, pt_data)
nrow(ps_data)
nrow(pt_data)
nrow(p_data)
p_data <- p_data[!duplicated(p_data),]
nrow(p_data)
write.csv(p_data, file = "data/parasite.csv")

print("-------- Freeliving: --------")

# freeliving source
# Unsupported interaction type(s): visits
freeliving_source <- c("preysOn", "eats", "flowersVisitedBy", "hasPathogen", "pollinatedBy", "hasParasite", "hostOf")
fs_data <- get_interactions_by_type(interactiontype = freeliving_source)
fs_data <- fs_data[c(1:2)]
colnames(fs_data) <- c("taxon_external_id", "taxon_name")

# freeliving target
# Unsupported interaction type(s): ectoParasiteOf, kleptoparasiteOf, ectoParasitoid, endoparasiteOf, parasitoidOf, endoparasitoidOf
freeliving_target <- c("preyedUponBy", "parasiteOf", "visitsFlowersOf", "pathogenOf", "hasHost")
ft_data <- get_interactions_by_type(interactiontype = freeliving_target)
ft_data <- ft_data[c(6:7)]
colnames(ft_data) <- c("taxon_external_id", "taxon_name")

# freeliving
f_data <- rbind(fs_data, ft_data)
nrow(fs_data)
nrow(ft_data)
nrow(f_data)
f_data <- f_data[!duplicated(f_data),]
nrow(f_data)
write.csv(f_data, file = "data/freeliving.csv")
print("--------------------------------------")