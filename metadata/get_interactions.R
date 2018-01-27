library(rglobi)

SKIP_START = 0

path_parasites <- paste("../data/interaction_data/parasite -", SKIP_START, ".csv")
path_freelivings <- paste("../data/interaction_data/freeliving -", SKIP_START, ".csv")

# List interactions identified in GloBI database
# get_interaction_types()
# get_interaction_types(opts = list())
start.time <- Sys.time()
print(start.time)

main <- function(property, path) {
    print(paste("-------- ", property, ": --------"))
    print(paste(property, "source:"))
    if (property == "Parasites") {
        source <- c("parasiteOf", "pathogenOf")
        target <- c("hasParasite", "hasPathogen")
    } else {
        source <- c("preysOn", "eats", "flowersVisitedBy", "hasPathogen", "pollinatedBy", "hasParasite", "hostOf")
        target <- c("preyedUponBy", "parasiteOf", "visitsFlowersOf", "pathogenOf", "hasHost")
    }

    s_data = get_data(source, c(1:2), start.time)

    start.time <- Sys.time()
    print(start.time)

    print(paste(property, "target:"))
    
    t_data = get_data(target, c(6:7), start.time)

    print(paste("#", property, "source=", nrow(s_data)))
    print(paste("#", property, "target=", nrow(s_data)))
    data <- rbind(s_data, t_data)
    print(paste("#total=", nrow(data)))
    data <- data[!duplicated(data),]
    print(paste("#total without duplicates=", nrow(data)))

    print(path)
    write.csv(data, file = path)

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

# main("Parasites", path_parasites)
main("Freeliving", path_freelivings)
