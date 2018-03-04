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

leaf.taxa <-  all.taxa[all.taxa$nr_children==0, ]
inner.taxa <- all.taxa[all.taxa$nr_children>1, ]
extendedInner.taxa <- all.taxa[all.taxa$nr_children>0, ]

print('----------------------- leaf.taxa$rank ---------------------------')
leaf.taxa <- as.data.frame(leaf.taxa)
# table(leaf.taxa$rank)[order(table(leaf.taxa$rank))]
print('----------------------- inner.taxa$rank ---------------------------')
inner.taxa <- as.data.frame(inner.taxa)
# table(inner.taxa$rank)[order(table(inner.taxa$rank))]
print('----------------------- extendedInner.taxa$rank ---------------------------')
extendedInner.taxa <- as.data.frame(extendedInner.taxa)
# table(extendedLeaf.taxa$rank)[order(table(extendedLeaf.taxa$rank))]
print('--------------------------------------------------')

# tapply(inner.taxa$max.height, inner.taxa$rank, summary)

inner.taxa$multifurc <- inner.taxa$nr_children-1

# ggplot(inner.taxa, aes(multifurc)) +
#     geom_histogram( 
#         col="black", 
#         aes(fill=..count..)) +
#     scale_y_log10() +
#     labs(x="number of children", y="number of nodes")
# ggsave("multifurc.pdf")

print('--------------------------------------------------')

null.furc.mod <- glm(multifurc~1, data=inner.taxa,
                   family="poisson")

print('------------------------kingdom - phylum - class - order--------------------------')

kingdom.furc.mod <- glm(multifurc~kingdom, data=inner.taxa,
                        family="poisson")
print(c('BIC=',  BIC(kingdom.furc.mod)))

# phylum.furc.mod <- glm(multifurc~phylum, data=inner.taxa,
#                         family="poisson")
# print(c('BIC=',  BIC(phylum.furc.mod)))

# class.furc.mod <- glm(multifurc~class, data=inner.taxa,
#                         family="poisson")
# print(c('BIC=',  BIC(class.furc.mod)))

order.furc.mod <- glm(multifurc~order, data=inner.taxa,
                        family="poisson")
print(c('BIC=',  BIC(order.furc.mod)))

# anova(kingdom.furc.mod, phylum.furc.mod, class.furc.mod, order.furc.mod, test="LRT")
# anova(kingdom.furc.mod, phylum.furc.mod, test="LRT")

print('-------------------kingdom + depth / min/max/mean.height-----------------------')

# kingdomPdepth.furc.mod <- glm(multifurc~kingdom+depth, data=inner.taxa,
#                    family="poisson")
# print(c('BIC=',  BIC(kingdomPdepth.furc.mod)))

# kingdomPminHeight.furc.mod <- glm(multifurc~kingdom+min.height, data=inner.taxa,
#                    family="poisson")
# print(c('BIC=',  BIC(kingdomPminHeight.furc.mod)))

# kingdomPmaxHeightt.furc.mod <- glm(multifurc~kingdom+max.height, data=inner.taxa,
#                    family="poisson")
# print(c('BIC=',  BIC(kingdomPmaxHeightt.furc.mod)))

# kingdomPmeanHeight.furc.mod <- glm(multifurc~kingdom+mean.height, data=inner.taxa,
#                    family="poisson")
# print(c('BIC=',  BIC(kingdomPmeanHeight.furc.mod)))

# anova(kingdomPdepth.furc.mod, kingdomPmaxHeightt.furc.mod, kingdomPminHeight.furc.mod, kingdomPmeanHeight.furc.mod, test="LRT")

print('-------------------kingdom * depth / min/max/mean.height-----------------------')

# kingdomTdepth.furc.mod <- glm(multifurc~kingdom*depth, data=inner.taxa,
#                    family="poisson")
# print(c('BIC=',  BIC(kingdomTdepth.furc.mod)))

# kingdomTminHeight.furc.mod <- glm(multifurc~kingdom*min.height, data=inner.taxa,
#                    family="poisson")
# print(c('BIC=',  BIC(kingdomTminHeight.furc.mod)))

# kingdomTmaxHeightt.furc.mod <- glm(multifurc~kingdom*max.height, data=inner.taxa,
#                    family="poisson")
# print(c('BIC=',  BIC(kingdomTmaxHeightt.furc.mod)))

# kingdomTmeanHeight.furc.mod <- glm(multifurc~kingdom*mean.height, data=inner.taxa,
#                    family="poisson")
# print(c('BIC=',  BIC(kingdomTmeanHeight.furc.mod)))

# anova(kingdomTdepth.furc.mod, kingdomTmaxHeightt.furc.mod, kingdomTminHeight.furc.mod, kingdomTmeanHeight.furc.mod, test="LRT")


print('-------------------phylum + depth / min/max/mean.height-----------------------')

# phylumPdepth.furc.mod <- glm(multifurc~phylum+depth, data=inner.taxa,
#                    family="poisson")
# print(c('BIC=',  BIC(phylumPdepth.furc.mod)))

# phylumPminHeight.furc.mod <- glm(multifurc~phylum+min.height, data=inner.taxa,
#                    family="poisson")
# print(c('BIC=',  BIC(phylumPminHeight.furc.mod)))

# phylumPmaxHeightt.furc.mod <- glm(multifurc~phylum+max.height, data=inner.taxa,
#                    family="poisson")
# print(c('BIC=',  BIC(phylumPmaxHeightt.furc.mod)))

# phylumPmeanHeight.furc.mod <- glm(multifurc~phylum+mean.height, data=inner.taxa,
#                    family="poisson")
# print(c('BIC=',  BIC(phylumPmeanHeight.furc.mod)))

# anova(phylumPdepth.furc.mod, phylumPmaxHeightt.furc.mod, phylumPminHeight.furc.mod, phylumPmeanHeight.furc.mod, test="LRT")

print('-------------------phylum * depth / min/max/mean.height-----------------------')

# phylumTdepth.furc.mod <- glm(multifurc~phylum*depth, data=inner.taxa,
#                    family="poisson")
# print(c('BIC=',  BIC(phylumTdepth.furc.mod)))

# phylumTminHeight.furc.mod <- glm(multifurc~phylum*min.height, data=inner.taxa,
#                    family="poisson")
# print(c('BIC=',  BIC(phylumTminHeight.furc.mod)))

# phylumTmaxHeightt.furc.mod <- glm(multifurc~phylum*max.height, data=inner.taxa,
#                    family="poisson")
# print(c('BIC=',  BIC(phylumTmaxHeightt.furc.mod)))

# phylumTmeanHeight.furc.mod <- glm(multifurc~phylum*mean.height, data=inner.taxa,
#                    family="poisson")
# print(c('BIC=',  BIC(phylumTmeanHeight.furc.mod)))

# anova(phylumTdepth.furc.mod, phylumTmaxHeightt.furc.mod, phylumTminHeight.furc.mod, phylumTmeanHeight.furc.mod, test="LRT")

# print('-------------------phylum mean.height-----------------------')

# anova(phylum.furc.mod, phylumPmeanHeight.furc.mod, phylumTmeanHeight.furc.mod, test="LRT")

print('-------------------class + depth / min/max/mean.height-----------------------')

# classPdepth.furc.mod <- glm(multifurc~class+depth, data=inner.taxa,
#                    family="poisson")
# print(c('BIC=',  BIC(classPdepth.furc.mod)))

# classPminHeight.furc.mod <- glm(multifurc~class+min.height, data=inner.taxa,
#                    family="poisson")
# print(c('BIC=',  BIC(classPminHeight.furc.mod)))

# classPmaxHeightt.furc.mod <- glm(multifurc~class+max.height, data=inner.taxa,
#                    family="poisson")
# print(c('BIC=',  BIC(classPmaxHeightt.furc.mod)))

# classPmeanHeight.furc.mod <- glm(multifurc~class+mean.height, data=inner.taxa,
#                    family="poisson")
# print(c('BIC=',  BIC(classPmeanHeight.furc.mod)))

# # anova(classPdepth.furc.mod, classPmaxHeightt.furc.mod, classPminHeight.furc.mod, classPmeanHeight.furc.mod, test="LRT")

print('-------------------class * depth / min/max/mean.height-----------------------')

# classTdepth.furc.mod <- glm(multifurc~class*depth, data=inner.taxa,
#                    family="poisson")
# print(c('BIC=',  BIC(classTdepth.furc.mod)))

# classTminHeight.furc.mod <- glm(multifurc~class*min.height, data=inner.taxa,
#                    family="poisson")
# print(c('BIC=',  BIC(classTminHeight.furc.mod)))

# classTmaxHeightt.furc.mod <- glm(multifurc~class*max.height, data=inner.taxa,
#                    family="poisson")
# print(c('BIC=',  BIC(classTmaxHeightt.furc.mod)))

# classTmeanHeight.furc.mod <- glm(multifurc~class*mean.height, data=inner.taxa,
#                    family="poisson")
# print(c('BIC=',  BIC(classTmeanHeight.furc.mod)))

# anova(classTdepth.furc.mod, classTmaxHeightt.furc.mod, classTminHeight.furc.mod, classTmeanHeight.furc.mod, test="LRT")

# print('-------------------class mean.height-----------------------')

# anova(class.furc.mod, classPmeanHeight.furc.mod, classTmeanHeight.furc.mod, test="LRT")


print('-------------------order + depth / min/max/mean.height-----------------------')

orderPdepth.furc.mod <- glm(multifurc~order+depth, data=inner.taxa,
                   family="poisson")
print(c('BIC=',  BIC(orderPdepth.furc.mod)))

orderPminHeight.furc.mod <- glm(multifurc~order+min.height, data=inner.taxa,
                   family="poisson")
print(c('BIC=',  BIC(orderPminHeight.furc.mod)))

orderPmaxHeightt.furc.mod <- glm(multifurc~order+max.height, data=inner.taxa,
                   family="poisson")
print(c('BIC=',  BIC(orderPmaxHeightt.furc.mod)))

orderPmeanHeight.furc.mod <- glm(multifurc~order+mean.height, data=inner.taxa,
                   family="poisson")
print(c('BIC=',  BIC(orderPmeanHeight.furc.mod)))

anova(orderPdepth.furc.mod, orderPmaxHeightt.furc.mod, orderPminHeight.furc.mod, orderPmeanHeight.furc.mod, test="LRT")

print('-------------------order * depth / min/max/mean.height-----------------------')

orderTdepth.furc.mod <- glm(multifurc~order*depth, data=inner.taxa,
                   family="poisson")
print(c('BIC=',  BIC(orderTdepth.furc.mod)))

orderTminHeight.furc.mod <- glm(multifurc~order*min.height, data=inner.taxa,
                   family="poisson")
print(c('BIC=',  BIC(orderTminHeight.furc.mod)))

orderTmaxHeightt.furc.mod <- glm(multifurc~order*max.height, data=inner.taxa,
                   family="poisson")
print(c('BIC=',  BIC(orderTmaxHeightt.furc.mod)))

orderTmeanHeight.furc.mod <- glm(multifurc~order*mean.height, data=inner.taxa,
                   family="poisson")
print(c('BIC=',  BIC(orderTmeanHeight.furc.mod)))

anova(orderTdepth.furc.mod, orderTmaxHeightt.furc.mod, orderTminHeight.furc.mod, orderTmeanHeight.furc.mod, test="LRT")



# print('--------------------------------------------------')

# print('-------------------effect phylum-----------------------')

# effect("phylum", phylum.furc.mod)

# effect("phylum:mean.height", phylumPmeanHeight)


# print('-------------------effect class-----------------------')

# classTmeanHeight.furc.mod <- glm(multifurc~class*mean.height, data=inner.taxa,
#                    family="poisson")

# effect("class", class.furc.mod)

# effect("class:mean.height", classPmeanHeight)

print('--------------------------------------------------')


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
