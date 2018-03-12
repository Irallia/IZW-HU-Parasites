library(data.table)
# library(ggplot2)

format(Sys.time(), "%a %b %d %X %Y")

all.taxa <- fread("../../results/Eukaryota-taxa.csv")

### right mode for all
all.taxa$kingdom <- as.factor(all.taxa$kingdom)
all.taxa$phylum <- as.factor(all.taxa$phylum)
all.taxa$class <- as.factor(all.taxa$class)
all.taxa$order <- as.factor(all.taxa$order)


heights <- do.call("rbind", strsplit(gsub("\\[|\\]", "", all.taxa$heights), ", "))

heights <- as.data.frame(apply(heights, 2, as.numeric))

names(heights) <- c("min.height", "max.height", "mean.height")

all.taxa <- cbind(all.taxa, heights)

## list all Kingdoms, Phyla:
# table(all.taxa$kingdom)
# table(all.taxa$phylum)

## which Phylum in which Kingdom:
# table(all.taxa$kingdom, all.taxa$phylum)

### all nodes sorted by rank
# table(all.taxa$rank)[order(table(all.taxa$rank))]

print('------------all.taxa$originaltag------------------')
table(all.taxa$originaltag)
print('------------all.taxa$finaltag------------------')
table(all.taxa$finaltag)

# table(all.taxa[all.taxa$finaltag+1 != all.taxa$originaltag, ]$kingdom)

print('---------------------------')

table(droplevels(all.taxa[all.taxa$finaltag+1 != all.taxa$originaltag, ]$phylum))

print('-----------Ascomycota-------------')
ascomycota <- all.taxa[all.taxa$phylum=="['ott439373', 'Ascomycota']", ]
bug_data.ascomycota <- ascomycota[ascomycota$finaltag+1 != ascomycota$originaltag, ]
table(droplevels(bug_data.ascomycota$class))
dim(ascomycota)

print('---------------------------')

print('-----------Chordata-------------')
chordata <- all.taxa[all.taxa$phylum=="['ott125642', 'Chordata']", ]
bug_data.chordata <- chordata[chordata$finaltag+1 != chordata$originaltag, ]
table(droplevels(bug_data.chordata$class))
dim(chordata)

print('-----------Sarcopterygii-------------')
sarcopterygii <- chordata[chordata$class=="['ott458402', 'Sarcopterygii']", ]
bug_data.sarcopterygii <- sarcopterygii[sarcopterygii$finaltag+1 != sarcopterygii$originaltag, ]
table(droplevels(bug_data.sarcopterygii$order))
dim(sarcopterygii)

print('---------------------------')

print('-----------Arthropoda-------------')
arthropoda <- all.taxa[all.taxa$phylum=="['ott632179', 'Arthropoda']", ]
bug_data.arthropoda <- arthropoda[arthropoda$finaltag+1 != arthropoda$originaltag, ]
table(droplevels(bug_data.arthropoda$class))

print('-----------Insecta-------------')
insecta <- arthropoda[arthropoda$class=="['ott1062253', 'Insecta']", ]
bug_data.insecta <- insecta[insecta$finaltag+1 != insecta$originaltag, ]
table(droplevels(bug_data.insecta$order))

diptera <- insecta[insecta$order=="['ott661378', 'Diptera']", ]
dim(diptera)

hemiptera <- insecta[insecta$order=="['ott603650', 'Hemiptera']", ]
dim(hemiptera)

# coleoptera <- insecta[insecta$order=="['ott865243', 'Coleoptera']", ]
# dim(coleoptera)

# lepidoptera <- insecta[insecta$order=="['ott965954', 'Lepidoptera']", ]
# dim(lepidoptera)

hymenoptera <- insecta[insecta$order=="['ott753726', 'Hymenoptera']", ]
dim(hymenoptera)
# bug_data.hymenoptera <- hymenoptera[hymenoptera$finaltag+1 != hymenoptera$originaltag, ]
# print(bug_data.hymenoptera)


print('--------------------------------------------------')

# leaf.taxa <-  all.taxa[all.taxa$nr_children==0, ]
# extendedLeaf.taxa <- all.taxa[all.taxa$nr_children<2 & min.height==max.height, ]
# inner.taxa <- all.taxa[all.taxa$nr_children>1 | (all.taxa$nr_children==1 & min.height!=max.height), ]

# print('----------------------- leaf.taxa$rank ---------------------------')
# leaf.taxa <- as.data.frame(leaf.taxa)
# # table(leaf.taxa$rank)[order(table(leaf.taxa$rank))]
# print('----------------------- extendedLeaf.taxa$rank ---------------------------')
# extendedLeaf.taxa <- as.data.frame(extendedLeaf.taxa)
# # table(extendedLeaf.taxa$rank)[order(table(extendedLeaf.taxa$rank))]
# print('----------------------- inner.taxa$rank ---------------------------')
# inner.taxa <- as.data.frame(inner.taxa)
# # table(inner.taxa$rank)[order(table(inner.taxa$rank))]
# print('--------------------------------------------------')

# tapply(inner.taxa$max.height, inner.taxa$rank, summary)


# print('-----------------------leaf.taxa$originaltag---------------------------')
# table(leaf.taxa$originaltag, leaf.taxa$rank)
# print('--------------------------------------------------')



# leaf.taxa$globi.data <- !is.na(leaf.taxa$originaltag)

# print('-----------Metazoa-------------')
# metazoa <- all.taxa[all.taxa$kingdom=="['ott691846', 'Metazoa']", ]
# # table(metazoa$phylum, metazoa$originaltag)

# print('-----------Nematoda-------------')
# nematoda <- all.taxa[all.taxa$phylum=="['ott395057', 'Nematoda']", ]
# # table(nematoda$order, nematoda$originaltag)
# # table(nematoda$rank)

# print('-----------Chordata-------------')
# chordata <- all.taxa[all.taxa$phylum=="['ott125642', 'Chordata']", ]
# # chordata[chordata$originaltag==2, ]

# print('-----------Platyhelminthes-------------')
# platyhelminthes <- all.taxa[all.taxa$phylum=="['ott555379', 'Platyhelminthes']", ]
# # platyhelminthes[platyhelminthes$originaltag==1, ]




format(Sys.time(), "%a %b %d %X %Y")
