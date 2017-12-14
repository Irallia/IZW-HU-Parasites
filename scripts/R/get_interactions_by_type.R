library(rglobi)

main <- function() {
    print("-------- get all Parasites: --------")
    # we have to split our request, first we ask for the parasites as a source of interactions, then as a target
    print("parasites source:")
    # use source of these interactions:
    parasite_source <- c("parasiteOf", "pathogenOf")
    ps_data = get_data(parasite_source, c(1:2))

    print("parasites target:")
    # use target of these interactions:
    parasite_target <- c("hasParasite", "hasPathogen")
    pt_data = get_data(parasite_target, c(6:7))

    print(paste("# parasites source =",nrow(ps_data)))
    print(paste("# parasites target =",nrow(pt_data)))
    p_data <- rbind(ps_data, pt_data)
    p_data <- p_data[!duplicated(p_data),]
    print(paste("# total without duplicates=",nrow(p_data)))

    write.csv(p_data, file = "output.csv")
    return()
}

get_data <- function(interactions, rows) {
    limit <- 5000
    i <- 0
    # use otherkeys to get more than a limited result from the query
    otherkeys = list("limit"=limit, "skip"=i)
    raw_data <- get_interactions_by_type(interactiontype = interactions, otherkeys = otherkeys)
    reduced_data <- raw_data[rows]
    data <- reduced_data[!duplicated(reduced_data),]
    print(paste(i+1,"th request"))
    print(nrow(data))

    while(nrow(raw_data) >= limit) {
        i <- i + 1
        skip <- i * limit
        otherkeys = list("limit"=limit, "skip"=skip, "taxonIdPrefix"="OTT")
        raw_data <- get_interactions_by_type(interactiontype = interactions, otherkeys = otherkeys)
        reduced_data <- raw_data[rows]
        reduced_data <- reduced_data[!duplicated(reduced_data),]
        data <- rbind(data, reduced_data)
        if(nrow(data) > 10000) {
            data <- data[!duplicated(data),]
            print(paste(i+1,"th request"))
            print(nrow(data))
        }
    }
    colnames(data) <- c("taxon_external_id", "taxon_name")
    return(data)
}

main()
