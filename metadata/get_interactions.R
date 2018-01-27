library(rglobi)

SKIP_START = 0

path_parasites <- paste("../data/interaction_data/parasite -", SKIP_START, ".csv")
path_freelivings <- paste("../data/interaction_data/freeliving -", SKIP_START, ".csv")

main <- function() {
    # List interactions identified in GloBI database
    # get_interaction_types()
    # get_interaction_types(opts = list())
    start.time <- Sys.time()
    print(start.time)

    print("-------- Parasites: --------")
    print("parasites source:")
    parasite_source <- c("parasiteOf", "pathogenOf")
    ps_data = get_data(parasite_source, c(1:2), start.time)

    start.time <- Sys.time()
    print(start.time)

    print("parasites target:")
    parasite_target <- c("hasParasite", "hasPathogen")
    pt_data = get_data(parasite_target, c(6:7), start.time)

    print(paste("#parasites source=", nrow(ps_data)))
    print(paste("#parasites target=", nrow(pt_data)))
    p_data <- rbind(ps_data, pt_data)
    print(paste("#total=", nrow(p_data)))
    p_data <- p_data[!duplicated(p_data),]
    print(paste("#total without duplicates=", nrow(p_data)))

    print(path_parasites)
    write.csv(p_data, file = path_parasites)

    print("-------- Freeliving: --------")

    start.time <- Sys.time()
    print(start.time)

    print("freeliving source")
    freeliving_source <- c("preysOn", "eats", "flowersVisitedBy", "hasPathogen", "pollinatedBy", "hasParasite", "hostOf")
    fs_data = get_data(freeliving_source, c(1:2), start.time)

    start.time <- Sys.time()
    print(start.time)

    print("freeliving target")
    freeliving_target <- c("preyedUponBy", "parasiteOf", "visitsFlowersOf", "pathogenOf", "hasHost")
    ft_data = get_data(freeliving_target, c(6:7), start.time)

    print(paste("#freeliving source=", nrow(fs_data)))
    print(paste("#freeliving target=", nrow(ft_data)))
    f_data <- rbind(fs_data, ft_data)
    print(paste("#total=", nrow(f_data)))
    f_data <- f_data[!duplicated(f_data),]
    print(paste("#total without duplicates=", nrow(f_data)))
    print(path_freelivings)
    write.csv(f_data, file = path_freelivings)
    print("--------------------------------------")
    return()
}

get_data <- function(interactions, rows, start.time) {
    limit <- 40000
    i <- SKIP_START

    otherkeys = list("limit"=limit, "skip"=i, "taxonIdPrefix"="OTT")
    raw_data <- get_interactions_by_type(interactiontype = interactions, otherkeys = otherkeys)
    reduced_data <- raw_data[rows]
    data <- reduced_data[!duplicated(reduced_data),]
    print(paste(i+1,"th request"))
    print(nrow(data))
    end.time <- Sys.time()
    time.taken <- end.time - start.time
    print(time.taken)

    while((i < SKIP_START + 10) || (nrow(raw_data) >= limit)) {
        i <- i + 1
        skip <- i * limit
        otherkeys = list("limit"=limit, "skip"=skip, "taxonIdPrefix"="OTT")
        raw_data <- get_interactions_by_type(interactiontype = interactions, otherkeys = otherkeys)
        reduced_data <- raw_data[rows]
        reduced_data <- reduced_data[!duplicated(reduced_data),]
        data <- rbind(data, reduced_data)
        # if(nrow(data) > 10000) {
            data <- data[!duplicated(data),]
            print(paste(i+1,"th request:", nrow(data), "rows"))
        # }
    }
    print(paste("i=", i))
    colnames(data) <- c("taxon_external_id", "taxon_name")
    return(data)
}

main()
