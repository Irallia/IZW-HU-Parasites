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
all.taxa$family <- as.factor(all.taxa$family)


heights <- do.call("rbind", strsplit(gsub("\\[|\\]", "", all.taxa$heights), ", "))

heights <- as.data.frame(apply(heights, 2, as.numeric))

names(heights) <- c("min.height", "max.height", "mean.height")

all.taxa <- cbind(all.taxa, heights)

## list all Kingdoms, Phyla:
# table(all.taxa$kingdom)
# table(all.taxa$phylum)

## which Phylum in which Kingdom:
# table(all.taxa$kingdom, all.taxa$phylum)

# summary(all.taxa$nr_children)
## [Min. 1st Qu.  Median    Mean 3rd Qu.    Max. ] over all phyla - max height
# tapply(all.taxa$max.height, all.taxa$phylum, summary)

### all nodes sorted by rank
# table(all.taxa$rank)[order(table(all.taxa$rank))]

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
print('--------------------------------------------------')
print('----------------------- data of subtrees ---------------------------')
# table(inner.taxa$kingdom)
# table(inner.taxa$phylum)

print('Fungi')
fungi <- all.taxa[all.taxa$kingdom=="['ott352914', 'Fungi']", ]
percentage_multifurcation = 100-(100/(sum(fungi$nr_children==0)-1) * sum(fungi$nr_children>0))
print(
    c('Subtree fungi has', 
        sum(fungi$nr_children>0), 'internal nodes and', 
        sum(fungi$nr_children==0), 'leaf nodes ->', 
        percentage_multifurcation, '% multifurcation'))
percentage_unknown = 100-(100/sum(fungi$nr_children==0) * (sum(fungi$originaltag==1, na.rm=T) + sum(fungi$originaltag==2, na.rm=T)))
print(
    c('Subtree fungi has', 
        sum(fungi$originaltag==1, na.rm=T), 'free-livings and ', 
        sum(fungi$originaltag==2, na.rm=T), 'parasites ->', 
        percentage_unknown, '% unknown states'))
print('--------------------------')

print('Chloroplastida')
chloroplastida <- all.taxa[all.taxa$kingdom=="['ott361838', 'Chloroplastida']", ]
percentage_multifurcation = 100-(100/(sum(chloroplastida$nr_children==0)-1) * sum(chloroplastida$nr_children>0))
print(
    c('Subtree chloroplastida has', 
        sum(chloroplastida$nr_children>0), 'internal nodes and', 
        sum(chloroplastida$nr_children==0), 'leaf nodes ->', 
        percentage_multifurcation, '% multifurcation'))
percentage_unknown = 100-(100/sum(chloroplastida$nr_children==0) * (sum(chloroplastida$originaltag==1, na.rm=T) + sum(chloroplastida$originaltag==2, na.rm=T)))
print(
    c('Subtree chloroplastida has', 
        sum(chloroplastida$originaltag==1, na.rm=T), 'free-livings and ', 
        sum(chloroplastida$originaltag==2, na.rm=T), 'parasites ->', 
        percentage_unknown, '% unknown states'))
print('--------------------------')

print('Metazoa')
metazoa <- all.taxa[all.taxa$kingdom=="['ott691846', 'Metazoa']", ]
percentage_multifurcation = 100-(100/(sum(metazoa$nr_children==0)-1) * sum(metazoa$nr_children>0))
print(
    c('Subtree Metazoa has', 
        sum(metazoa$nr_children>0), 'internal nodes and', 
        sum(metazoa$nr_children==0), 'leaf nodes ->', 
        percentage_multifurcation, '% multifurcation'))
percentage_unknown = 100-(100/sum(metazoa$nr_children==0) * (sum(metazoa$originaltag==1, na.rm=T) + sum(metazoa$originaltag==2, na.rm=T)))
print(
    c('Subtree Metazoa has', 
        sum(metazoa$originaltag==1, na.rm=T), 'free-livings and ', 
        sum(metazoa$originaltag==2, na.rm=T), 'parasites ->', 
        percentage_unknown, '% unknown states'))
print('--------------------------')

print('Chordata')
chordata <- all.taxa[all.taxa$phylum=="['ott125642', 'Chordata']", ]
percentage_multifurcation = 100-(100/(sum(chordata$nr_children==0)-1) * sum(chordata$nr_children>0))
print(
    c('Subtree chordata has', 
        sum(chordata$nr_children>0), 'internal nodes and', 
        sum(chordata$nr_children==0), 'leaf nodes ->', 
        percentage_multifurcation, '% multifurcation'))
percentage_unknown = 100-(100/sum(chordata$nr_children==0) * (sum(chordata$originaltag==1, na.rm=T) + sum(chordata$originaltag==2, na.rm=T)))
print(
    c('Subtree chordata has', 
        sum(chordata$originaltag==1, na.rm=T), 'free-livings and ', 
        sum(chordata$originaltag==2, na.rm=T), 'parasites ->', 
        percentage_unknown, '% unknown states'))
print('--------------------------')

print('Nematoda')
nematoda <- all.taxa[all.taxa$phylum=="['ott395057', 'Nematoda']", ]
percentage_multifurcation = 100-(100/(sum(nematoda$nr_children==0)-1) * sum(nematoda$nr_children>0))
print(
    c('Subtree nematoda has', 
        sum(nematoda$nr_children>0), 'internal nodes and', 
        sum(nematoda$nr_children==0), 'leaf nodes ->', 
        percentage_multifurcation, '% multifurcation'))
percentage_unknown = 100-(100/sum(nematoda$nr_children==0) * (sum(nematoda$originaltag==1, na.rm=T) + sum(nematoda$originaltag==2, na.rm=T)))
print(
    c('Subtree nematoda has', 
        sum(nematoda$originaltag==1, na.rm=T), 'free-livings and ', 
        sum(nematoda$originaltag==2, na.rm=T), 'parasites ->', 
        percentage_unknown, '% unknown states'))
print('--------------------------')

print('Platyhelminthes')
platyhelminthes <- all.taxa[all.taxa$phylum=="['ott555379', 'Platyhelminthes']", ]
percentage_multifurcation = 100-(100/(sum(platyhelminthes$nr_children==0)-1) * sum(platyhelminthes$nr_children>0))
print(
    c('Subtree platyhelminthes has', 
        sum(platyhelminthes$nr_children>0), 'internal nodes and', 
        sum(platyhelminthes$nr_children==0), 'leaf nodes ->', 
        percentage_multifurcation, '% multifurcation'))
percentage_unknown = 100-(100/sum(platyhelminthes$nr_children==0) * (sum(platyhelminthes$originaltag==1, na.rm=T) + sum(platyhelminthes$originaltag==2, na.rm=T)))
print(
    c('Subtree platyhelminthes has', 
        sum(platyhelminthes$originaltag==1, na.rm=T), 'free-livings and ', 
        sum(platyhelminthes$originaltag==2, na.rm=T), 'parasites ->', 
        percentage_unknown, '% unknown states'))
print('--------------------------')

print('Apicomplexa')
apicomplexa <- all.taxa[all.taxa$phylum=="['ott422673', 'Apicomplexa']", ]
percentage_multifurcation = 100-(100/(sum(apicomplexa$nr_children==0)-1) * sum(apicomplexa$nr_children>0))
print(
    c('Subtree apicomplexa has', 
        sum(apicomplexa$nr_children>0), 'internal nodes and', 
        sum(apicomplexa$nr_children==0), 'leaf nodes ->', 
        percentage_multifurcation, '% multifurcation'))
percentage_unknown = 100-(100/sum(apicomplexa$nr_children==0) * (sum(apicomplexa$originaltag==1, na.rm=T) + sum(apicomplexa$originaltag==2, na.rm=T)))
print(
    c('Subtree apicomplexa has', 
        sum(apicomplexa$originaltag==1, na.rm=T), 'free-livings and ', 
        sum(apicomplexa$originaltag==2, na.rm=T), 'parasites ->', 
        percentage_unknown, '% unknown states'))
print('--------------------------')

print('Arthropoda')
arthropoda <- all.taxa[all.taxa$phylum=="['ott632179', 'Arthropoda']", ]
percentage_multifurcation = 100-(100/(sum(arthropoda$nr_children==0)-1) * sum(arthropoda$nr_children>0))
print(
    c('Subtree arthropoda has', 
        sum(arthropoda$nr_children>0), 'internal nodes and', 
        sum(arthropoda$nr_children==0), 'leaf nodes ->', 
        percentage_multifurcation, '% multifurcation'))
percentage_unknown = 100-(100/sum(arthropoda$nr_children==0) * (sum(arthropoda$originaltag==1, na.rm=T) + sum(arthropoda$originaltag==2, na.rm=T)))
print(
    c('Subtree arthropoda has', 
        sum(arthropoda$originaltag==1, na.rm=T), 'free-livings and ', 
        sum(arthropoda$originaltag==2, na.rm=T), 'parasites ->', 
        percentage_unknown, '% unknown states'))
print('--------------------------')

print('Insecta')
insecta <- arthropoda[arthropoda$class=="['ott1062253', 'Insecta']", ]
percentage_multifurcation = 100-(100/(sum(insecta$nr_children==0)-1) * sum(insecta$nr_children>0))
print(
    c('Subtree arthropoda has', 
        sum(insecta$nr_children>0), 'internal nodes and', 
        sum(insecta$nr_children==0), 'leaf nodes ->', 
        percentage_multifurcation, '% multifurcation'))
percentage_unknown = 100-(100/sum(insecta$nr_children==0) * (sum(insecta$originaltag==1, na.rm=T) + sum(insecta$originaltag==2, na.rm=T)))
print(
    c('Subtree arthropoda has', 
        sum(insecta$originaltag==1, na.rm=T), 'free-livings and ', 
        sum(insecta$originaltag==2, na.rm=T), 'parasites ->', 
        percentage_unknown, '% unknown states'))


print('--------------------------------------------------')
print('--------------------------------------------------')

# tapply(inner.taxa$max.height, inner.taxa$rank, summary)

inner.taxa$multifurc <- inner.taxa$nr_children-1

# ggplot(inner.taxa, aes(multifurc)) +
#     geom_histogram(col="black") +
#     scale_y_log10() +
#     labs(x="number of children", y="number of nodes")
# ggsave("multifurc.pdf")

# ggplot(inner.taxa, aes(multifurc)) +
#     geom_histogram( 
#         col="black", 
#         binwidth = 1,
#         aes(fill=..count..)) +
#     xlim(0, 30) +
#     scale_y_log10() +
#     labs(x="number of children", y="number of nodes")
# ggsave("multifurc_small.pdf")

print('--------------------------------------------------')
print('-------------------------multifurc data-------------------------')
print('--------------------------------------------------')
# null.furc.mod <- glm(multifurc~1, data=inner.taxa,
#                    family="poisson")

print('------------------------kingdom - phylum - class - order - family--------------------------')

# kingdom.furc.mod <- glm(multifurc~kingdom, data=inner.taxa,
#                         family="poisson")
# print(c('BIC=',  BIC(kingdom.furc.mod)))

# phylum.furc.mod <- glm(multifurc~phylum, data=inner.taxa,
#                         family="poisson")
# print(c('BIC=',  BIC(phylum.furc.mod)))

# class.furc.mod <- glm(multifurc~class, data=inner.taxa,
#                         family="poisson")
# print(c('BIC=',  BIC(class.furc.mod)))

# order.furc.mod <- glm(multifurc~order, data=inner.taxa,
#                         family="poisson")
# print(c('BIC=',  BIC(order.furc.mod)))

# family.furc.mod <- glm(multifurc~family, data=inner.taxa,
#                         family="poisson")
# print(c('BIC=',  BIC(family.furc.mod)))

# anova(kingdom.furc.mod, phylum.furc.mod, class.furc.mod, order.furc.mod, family.furc.mod, test="LRT")

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

# anova(classPdepth.furc.mod, classPmaxHeightt.furc.mod, classPminHeight.furc.mod, classPmeanHeight.furc.mod, test="LRT")

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


print('-------------------order + depth / min/max/mean.height-----------------------')

# orderPdepth.furc.mod <- glm(multifurc~order+depth, data=inner.taxa,
#                    family="poisson")
# print(c('BIC=',  BIC(orderPdepth.furc.mod)))

# orderPminHeight.furc.mod <- glm(multifurc~order+min.height, data=inner.taxa,
#                    family="poisson")
# print(c('BIC=',  BIC(orderPminHeight.furc.mod)))

# orderPmaxHeightt.furc.mod <- glm(multifurc~order+max.height, data=inner.taxa,
#                    family="poisson")
# print(c('BIC=',  BIC(orderPmaxHeightt.furc.mod)))

# orderPmeanHeight.furc.mod <- glm(multifurc~order+mean.height, data=inner.taxa,
#                    family="poisson")
# print(c('BIC=',  BIC(orderPmeanHeight.furc.mod)))

# anova(orderPdepth.furc.mod, orderPmaxHeightt.furc.mod, orderPminHeight.furc.mod, orderPmeanHeight.furc.mod, test="LRT")

print('-------------------order * depth / min/max/mean.height-----------------------')

# orderTdepth.furc.mod <- glm(multifurc~order*depth, data=inner.taxa,
#                    family="poisson")
# print(c('BIC=',  BIC(orderTdepth.furc.mod)))

# orderTminHeight.furc.mod <- glm(multifurc~order*min.height, data=inner.taxa,
#                    family="poisson")
# print(c('BIC=',  BIC(orderTminHeight.furc.mod)))

# orderTmaxHeightt.furc.mod <- glm(multifurc~order*max.height, data=inner.taxa,
#                    family="poisson")
# print(c('BIC=',  BIC(orderTmaxHeightt.furc.mod)))

# orderTmeanHeight.furc.mod <- glm(multifurc~order*mean.height, data=inner.taxa,
#                    family="poisson")
# print(c('BIC=',  BIC(orderTmeanHeight.furc.mod)))

# anova(orderTdepth.furc.mod, orderTmaxHeightt.furc.mod, orderTminHeight.furc.mod, orderTmeanHeight.furc.mod, test="LRT")

print('-------------------family + depth / min/max/mean.height-----------------------')

# familyPdepth.furc.mod <- glm(multifurc~family+depth, data=inner.taxa,
#                    family="poisson")
# print(c('BIC=',  BIC(familyPdepth.furc.mod)))

# familyPminHeight.furc.mod <- glm(multifurc~family+min.height, data=inner.taxa,
#                    family="poisson")
# print(c('BIC=',  BIC(familyPminHeight.furc.mod)))

# familyPmaxHeightt.furc.mod <- glm(multifurc~family+max.height, data=inner.taxa,
#                    family="poisson")
# print(c('BIC=',  BIC(familyPmaxHeightt.furc.mod)))

# familyPmeanHeight.furc.mod <- glm(multifurc~family+mean.height, data=inner.taxa,
#                    family="poisson")
# print(c('BIC=',  BIC(familyPmeanHeight.furc.mod)))

# anova(familyPdepth.furc.mod, familyPmaxHeightt.furc.mod, familyPminHeight.furc.mod, familyPmeanHeight.furc.mod, test="LRT")

print('-------------------family * depth / min/max/mean.height-----------------------')

# familyTdepth.furc.mod <- glm(multifurc~family*depth, data=inner.taxa,
#                    family="poisson")
# print(c('BIC=',  BIC(familyTdepth.furc.mod)))

# familyTminHeight.furc.mod <- glm(multifurc~family*min.height, data=inner.taxa,
#                    family="poisson")
# print(c('BIC=',  BIC(familyTminHeight.furc.mod)))

# familyTmaxHeightt.furc.mod <- glm(multifurc~family*max.height, data=inner.taxa,
#                    family="poisson")
# print(c('BIC=',  BIC(familyTmaxHeightt.furc.mod)))

# familyTmeanHeight.furc.mod <- glm(multifurc~family*mean.height, data=inner.taxa,
#                    family="poisson")
# print(c('BIC=',  BIC(familyTmeanHeight.furc.mod)))

# anova(familyTdepth.furc.mod, familyTmaxHeightt.furc.mod, familyTminHeight.furc.mod, familyTmeanHeight.furc.mod, test="LRT")

# print('-------------------effect kingdom-----------------------')

# effect("kingdom", kingdom.furc.mod)

# effect("kingdom:mean.height", kingdomPmeanHeight.furc.mod)

# print('-------------------effect phylum-----------------------')

# effect("phylum", phylum.furc.mod)

# effect("phylum:mean.height", phylumPmeanHeight.furc.mod)

# print('-------------------effect class-----------------------')

# effect("class", class.furc.mod)

# effect("class:mean.height", classPmeanHeight)

print('--------------------------------------------------')
print('--------------------------------------------------')

# ggplot(inner.taxa, aes(rank, mean.height)) +
#     geom_boxplot()

# ggplot(inner.taxa, aes(phylum, max.height)) +
#     geom_boxplot() +
#     theme(axis.text.x = element_text(angle = 90, hjust = 1))

# ### if you want look at the package magitr to avoid such nested
# ### parantheses
# ## %>%

print('--------------------------------------------------')
print('-------------------------unknown / globi data-------------------------')
print('--------------------------------------------------')

leaf.taxa$globi.data <- !is.na(leaf.taxa$originaltag)
null.globi.mod <- glm(globi.data~1, data=leaf.taxa, family="binomial")

# phylum.globi.mod$aic

# kingdom.globi.mod$aic


print('------------------------kingdom - phylum - class--------------------------')

# kingdom.globi.mod <- glm(globi.data~kingdom, data=leaf.taxa, family="binomial")
# print(c('BIC=',  BIC(kingdom.globi.mod)))
# effect("kingdom", kingdom.globi.mod)

# phylum.globi.mod <- glm(globi.data~phylum, data=leaf.taxa, family="binomial")
# print(c('BIC=',  BIC(phylum.globi.mod)))
# effect("phylum", phylum.globi.mod)

# class.globi.mod <- glm(globi.data~class, data=leaf.taxa, family="binomial")
# print(c('BIC=',  BIC(class.globi.mod)))

# anova(kingdom.globi.mod, phylum.globi.mod, class.globi.mod, test="LRT")


print('-------------------kingdom + depth / * depth-----------------------')

# kingdomPdepth.globi.mod <- glm(globi.data~kingdom+depth, data=leaf.taxa, family="binomial")
# print(c('BIC=',  BIC(kingdomPdepth.globi.mod)))
# effect("kingdom", kingdomPdepth.globi.mod)

# kingdomTdepth.globi.mod <- glm(globi.data~kingdom*depth, data=leaf.taxa, family="binomial")
# print(c('BIC=',  BIC(kingdomTdepth.globi.mod)))
# effect("kingdom", kingdomTdepth.globi.mod)

# anova(kingdomPdepth.globi.mod, kingdomTdepth.globi.mod, test="LRT")


print('-------------------phylum + depth / * depth-----------------------')

# phylumPdepth.globi.mod <- glm(globi.data~phylum+depth, data=leaf.taxa, family="binomial")
# print(c('BIC=',  BIC(phylumPdepth.globi.mod)))
# effect("phylum", phylumPdepth.globi.mod)

# phylumTdepth.globi.mod <- glm(globi.data~phylum*depth, data=leaf.taxa, family="binomial")
# print(c('BIC=',  BIC(phylumTdepth.globi.mod)))
# effect("phylum", phylumTdepth.globi.mod)

# anova(phylumPdepth.globi.mod, phylumTdepth.globi.mod, test="LRT")


print('-------------------class + depth / * depth-----------------------')

# classPdepth.globi.mod <- glm(globi.data~class+depth, data=leaf.taxa, family="binomial")
# print(c('BIC=',  BIC(classPdepth.globi.mod)))

# classTdepth.globi.mod <- glm(globi.data~class*depth, data=leaf.taxa, family="binomial")
# print(c('BIC=',  BIC(classTdepth.globi.mod)))

# anova(classPdepth.globi.mod, classTdepth.globi.mod, test="LRT")


print('-------Taxa like Order or Family are too expensive to calculate.-------')

format(Sys.time(), "%a %b %d %X %Y")
