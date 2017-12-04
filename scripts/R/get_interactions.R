library(rglobi)

path_parasites <- "../../data/interaction_data/parasite.csv"
path_freelivings <- "../../data/interaction_data/freeliving.csv"

main <- function() {
    # List interactions identified in GloBI database
    # get_interaction_types()
    # get_interaction_types(opts = list())

    print(Sys.time())

    print("-------- Parasites: --------")
    print("parasites source:")
    # Unsupported interaction type(s): ectoParasiteOf, kleptoparasiteOf, ectoParasitoid, endoparasiteOf, parasitoidOf, endoparasitoidOf
    parasite_source <- c("parasiteOf", "pathogenOf")
    ps_data = get_data(parasite_source, c(1:2))

    print("parasites target:")
    parasite_target <- c("hasParasite", "hasPathogen")
    pt_data = get_data(parasite_target, c(6:7))

    # parasite
    p_data <- rbind(ps_data, pt_data)
    print(nrow(ps_data))
    print(nrow(pt_data))
    print(nrow(p_data))
    p_data <- p_data[!duplicated(p_data),]
    print(nrow(p_data))
    write.csv(p_data, file = path_parasites)

    print(Sys.time())
    print("-------- Freeliving: --------")

    # freeliving source
    # Unsupported interaction type(s): visits
    freeliving_source <- c("preysOn", "eats", "flowersVisitedBy", "hasPathogen", "pollinatedBy", "hasParasite", "hostOf")
    fs_data = get_data(freeliving_source, c(1:2))

    # freeliving target
    # Unsupported interaction type(s): ectoParasiteOf, kleptoparasiteOf, ectoParasitoid, endoparasiteOf, parasitoidOf, endoparasitoidOf
    freeliving_target <- c("preyedUponBy", "parasiteOf", "visitsFlowersOf", "pathogenOf", "hasHost")
    ft_data = get_data(freeliving_target, c(6:7))

    # freeliving
    f_data <- rbind(fs_data, ft_data)
    print(nrow(fs_data))
    print(nrow(ft_data))
    print(nrow(f_data))
    f_data <- f_data[!duplicated(f_data),]
    print(nrow(f_data))
    write.csv(f_data, file = path_freelivings)
    print("--------------------------------------")
    return()
}

get_data <- function(interactions, rows) {
    limit <- 500000
    i <- 0

    otherkeys = list("limit"=limit, "skip"=i)
    raw_data <- get_interactions_by_type(interactiontype = interactions, otherkeys = otherkeys)
    reduced_data <- raw_data[rows]
    data <- reduced_data[!duplicated(reduced_data),]
    print(paste(i+1,"th request"))
    print(nrow(data))

    while(nrow(raw_data) >= limit) {
        i <- i + 1
        otherkeys = list("limit"=limit, "skip"=i)
        raw_data <- get_interactions_by_type(interactiontype = interactions, otherkeys = otherkeys)
        reduced_data <- raw_data[rows]
        reduced_data <- reduced_data[!duplicated(reduced_data),]
        data <- rbind(data, reduced_data)
        if(nrow(data) > 40000) {
            data <- data[!duplicated(data),]
            print(paste(i+1,"th request"))
            print(nrow(data))
        }
    }
    colnames(data) <- c("taxon_external_id", "taxon_name")
    return(data)
}

main()
