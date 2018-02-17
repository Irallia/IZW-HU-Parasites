library(data.table)
library(ggplot2)
library(effects)

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

summary(all.taxa$nr_children)
## [Min. 1st Qu.  Median    Mean 3rd Qu.    Max. ] over all phyla - max height
# tapply(all.taxa$max.height, all.taxa$phylum, summary)

### all nodes sorted by rank
table(all.taxa$rank)[order(table(all.taxa$rank))]

### find out what is going on here...
# print('------------------------ all.taxa$nr_children==1 --------------------------')
# table(all.taxa[all.taxa$nr_children==1, "finaltag"])
# print('---------------- nr_children==1 ---------------------')
# table(all.taxa[all.taxa$nr_children==1, "rank"])
# print('---------------- nr_children==1 & max.height>2 ---------------------')
# table(all.taxa[all.taxa$nr_children==1 & all.taxa$max.height>2, "rank"])
# print('--------------------------------------------------')
# table(all.taxa[all.taxa$nr_children==1 & all.taxa$max.height>2, "finaltag"])
# print('--------------------------------------------------')
# table(all.taxa[all.taxa$nr_children==1 & all.taxa$max.height==2, "finaltag"])
print('--------------------------------------------------')


## pdf(path, width=8, height=6)
# ggplot(all.taxa, aes(nr_children)) +
#     geom_histogram() +
#     scale_y_log10()
# ggsave("nr_children.pdf")
## dev.off()

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

inner.taxa$multifurc <- inner.taxa$nr_children-1

# ggplot(inner.taxa, aes(multifurc)) +
#     geom_histogram() +
#     scale_y_log10()
# ggsave("multifurc.pdf")

print('--------------------------------------------------')

null.furc.mod <- glm(multifurc~1, data=inner.taxa,
                   family="poisson")

print(null.furc.mod)


print('------------------------kingdom - phylum - class - order--------------------------')

kingdom.furc.mod <- glm(multifurc~kingdom, data=inner.taxa,
                        family="poisson")

phylum.furc.mod <- glm(multifurc~phylum, data=inner.taxa,
                        family="poisson")

class.furc.mod <- glm(multifurc~class, data=inner.taxa,
                        family="poisson")

order.furc.mod <- glm(multifurc~order, data=inner.taxa,
                        family="poisson")

anova(kingdom.furc.mod, phylum.furc.mod, class.furc.mod, order.furc.mod, test="LRT")
# anova(kingdom.furc.mod, phylum.furc.mod, test="LRT")


# print('-------------------phylum + depth / min/max/mean.height-----------------------')

# phylumPdepth.furc.mod <- glm(multifurc~phylum+depth, data=inner.taxa,
#                    family="poisson")

# phylumPminHeight.furc.mod <- glm(multifurc~phylum+min.height, data=inner.taxa,
#                    family="poisson")

# phylumPmaxHeightt.furc.mod <- glm(multifurc~phylum+max.height, data=inner.taxa,
#                    family="poisson")

# phylumPmeanHeight.furc.mod <- glm(multifurc~phylum+mean.height, data=inner.taxa,
#                    family="poisson")

# anova(phylumPdepth.furc.mod, phylumPmaxHeightt.furc.mod, phylumPminHeight.furc.mod, phylumPmeanHeight.furc.mod, test="LRT")

# print('-------------------phylum * depth / min/max/mean.height-----------------------')

# phylumTdepth.furc.mod <- glm(multifurc~phylum*depth, data=inner.taxa,
#                    family="poisson")

# phylumTminHeight.furc.mod <- glm(multifurc~phylum*min.height, data=inner.taxa,
#                    family="poisson")

# phylumTmaxHeightt.furc.mod <- glm(multifurc~phylum*max.height, data=inner.taxa,
#                    family="poisson")

# phylumTmeanHeight.furc.mod <- glm(multifurc~phylum*mean.height, data=inner.taxa,
#                    family="poisson")

# anova(phylumTmaxHeightt.furc.mod, phylumTdepth.furc.mod, phylumTminHeight.furc.mod, phylumTmeanHeight.furc.mod, test="LRT")

# print('-------------------phylum mean.height-----------------------')

# anova(phylum.furc.mod, phylumPmeanHeight.furc.mod, phylumTmeanHeight.furc.mod, test="LRT")

print('-------------------order + depth / min/max/mean.height-----------------------')

orderPdepth.furc.mod <- glm(multifurc~order+depth, data=inner.taxa,
                   family="poisson")

orderPminHeight.furc.mod <- glm(multifurc~order+min.height, data=inner.taxa,
                   family="poisson")

orderPmaxHeightt.furc.mod <- glm(multifurc~order+max.height, data=inner.taxa,
                   family="poisson")

orderPmeanHeight.furc.mod <- glm(multifurc~order+mean.height, data=inner.taxa,
                   family="poisson")

anova(orderPdepth.furc.mod, orderPmaxHeightt.furc.mod, orderPminHeight.furc.mod, orderPmeanHeight.furc.mod, test="LRT")

print('-------------------order * depth / min/max/mean.height-----------------------')

orderTdepth.furc.mod <- glm(multifurc~order*depth, data=inner.taxa,
                   family="poisson")

orderTminHeight.furc.mod <- glm(multifurc~order*min.height, data=inner.taxa,
                   family="poisson")

orderTmaxHeightt.furc.mod <- glm(multifurc~order*max.height, data=inner.taxa,
                   family="poisson")

orderTmeanHeight.furc.mod <- glm(multifurc~order*mean.height, data=inner.taxa,
                   family="poisson")

anova(orderTmaxHeightt.furc.mod, orderTdepth.furc.mod, orderTminHeight.furc.mod, orderTmeanHeight.furc.mod, test="LRT")

print('-------------------order mean.height-----------------------')

anova(order.furc.mod, orderPmeanHeight.furc.mod, orderTmeanHeight.furc.mod, test="LRT")

print('--------------------------------------------------')


# print('-------------------effect class-----------------------')

# effect("class", class.mod)

# effect("class:max.height", classPh)


# ggplot(inner.taxa, aes(rank, mean.height)) +
#     geom_boxplot()

# ggplot(inner.taxa, aes(phylum, max.height)) +
#     geom_boxplot() +
#     theme(axis.text.x = element_text(angle = 90, hjust = 1))

# ### if you want look at the package magitr to avoid such nested
# ### parantheses
# ## %>%

# leaf.taxa$globi.data <- !is.na(leaf.taxa$originaltag)

# null.globi.mod <- glm(globi.data~1,
#                          data=leaf.taxa, family="binomial")

# kingdom.globi.mod <- glm(globi.data~kingdom,
#                          data=leaf.taxa, family="binomial")

# summary(kingdom.globi.mod)

# effect("kingdom", kingdom.globi.mod)

# phylum.globi.mod <- glm(globi.data~phylum,
#                         data=leaf.taxa, family="binomial")

# summary(phylum.globi.mod)

# effect("phylum", phylum.globi.mod)

# anova(null.globi.mod, phylum.globi.mod)

# phylum.globi.mod$aic

# kingdom.globi.mod$aic

format(Sys.time(), "%a %b %d %X %Y")
