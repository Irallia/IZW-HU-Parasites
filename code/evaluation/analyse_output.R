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

table(all.taxa[all.taxa$finaltag+1 != all.taxa$originaltag, ]$kingdom)
print('--------------------------------------------------')

leaf.taxa <-  all.taxa[all.taxa$nr_children==0, ]
extendedLeaf.taxa <- all.taxa[all.taxa$nr_children<2 & min.height==max.height, ]
inner.taxa <- all.taxa[all.taxa$nr_children>1 | (all.taxa$nr_children==1 & min.height!=max.height), ]

print('----------------------- leaf.taxa$rank ---------------------------')
leaf.taxa <- as.data.frame(leaf.taxa)
# table(leaf.taxa$rank)[order(table(leaf.taxa$rank))]
print('----------------------- extendedLeaf.taxa$rank ---------------------------')
extendedLeaf.taxa <- as.data.frame(extendedLeaf.taxa)
# table(extendedLeaf.taxa$rank)[order(table(extendedLeaf.taxa$rank))]
print('----------------------- inner.taxa$rank ---------------------------')
inner.taxa <- as.data.frame(inner.taxa)
# table(inner.taxa$rank)[order(table(inner.taxa$rank))]
print('--------------------------------------------------')

# tapply(inner.taxa$max.height, inner.taxa$rank, summary)


print('-----------------------leaf.taxa$originaltag---------------------------')
table(leaf.taxa$originaltag, leaf.taxa$rank)
print('--------------------------------------------------')



leaf.taxa$globi.data <- !is.na(leaf.taxa$originaltag)

print('-----------Metazoa-------------')
metazoa <- all.taxa[all.taxa$kingdom=="['ott691846', 'Metazoa']", ]
# table(metazoa$phylum, metazoa$originaltag)

print('-----------Nematoda-------------')
nematoda <- all.taxa[all.taxa$phylum=="['ott395057', 'Nematoda']", ]
table(nematoda$order, nematoda$originaltag)
table(nematoda$rank)

print('-----------Chordata-------------')
chordata <- all.taxa[all.taxa$phylum=="['ott125642', 'Chordata']", ]
# chordata[chordata$originaltag==2, ]

print('-----------Platyhelminthes-------------')
platyhelminthes <- all.taxa[all.taxa$phylum=="['ott555379', 'Platyhelminthes']", ]
# platyhelminthes[platyhelminthes$originaltag==1, ]




format(Sys.time(), "%a %b %d %X %Y")
