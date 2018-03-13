library(data.table)
# library(ggplot2)
# library(effects)
library(lme4)

format(Sys.time(), "%a %b %d %X %Y")

all.taxa <- fread("../../results/Eukaryota-cross_evaluation-taxa.csv")
# ott_id,originaltag,finaltag,depth,nr_children,run,new_finaltag,correct_predicted,name,rank,uniqname,kingdom,phylum,class,order

### right mode for all
all.taxa$kingdom <- as.factor(all.taxa$kingdom)
all.taxa$phylum <- as.factor(all.taxa$phylum)
all.taxa$class <- as.factor(all.taxa$class)
all.taxa$order <- as.factor(all.taxa$order)

print('----------------------- leaf.taxa$T/F ---------------------------')
leaf.taxa <-  all.taxa[all.taxa$nr_children==0, ]
leaf.taxa <- as.data.frame(leaf.taxa)
table(leaf.taxa$correct_predicted)[order(table(leaf.taxa$correct_predicted))]

leaf.taxa$correct_predicted <- !is.na(leaf.taxa$correct_predicted)

null.correct_predicted.mod <- glm(correct_predicted~1, data=leaf.taxa, family="binomial")

print('------------------------kingdom - phylum - class - order--------------------------')

kingdom.correct_predicted.mod <- glm(correct_predicted~kingdom, data=leaf.taxa, family="binomial")
print(c('BIC=',  BIC(kingdom.correct_predicted.mod)))
# effect("kingdom", kingdom.correct_predicted.mod)
# anova(null.correct_predicted.mod, kingdom.correct_predicted.mod)

# summary(kingdom.correct_predicted.mod)

phylum.correct_predicted.mod <- glm(correct_predicted~phylum, data=leaf.taxa, family="binomial")
print(c('BIC=',  BIC(phylum.correct_predicted.mod)))
# effect("phylum", phylum.correct_predicted.mod)

class.correct_predicted.mod <- glm(correct_predicted~class, data=leaf.taxa, family="binomial")
print(c('BIC=',  BIC(class.correct_predicted.mod)))

order.correct_predicted.mod <- glm(correct_predicted~order, data=leaf.taxa, family="binomial")
print(c('BIC=',  BIC(order.correct_predicted.mod)))

anova(kingdom.correct_predicted.mod, phylum.correct_predicted.mod, class.correct_predicted.mod, order.correct_predicted.mod, test="LRT")

print('-------------------kingdom + depth / * depth-----------------------')

kingdomPdepth.correct_predicted.mod <- glm(correct_predicted~kingdom+depth, data=leaf.taxa, family="binomial")
print(c('BIC=',  BIC(kingdomPdepth.correct_predicted.mod)))
# effect("kingdom", kingdomPdepth.correct_predicted.mod)

kingdomTdepth.correct_predicted.mod <- glm(correct_predicted~kingdom*depth, data=leaf.taxa, family="binomial")
print(c('BIC=',  BIC(kingdomTdepth.correct_predicted.mod)))
# effect("kingdom", kingdomTdepth.correct_predicted.mod)

anova(kingdomPdepth.correct_predicted.mod, kingdomTdepth.correct_predicted.mod, test="LRT")


print('-------------------phylum + depth / * depth-----------------------')

phylumPdepth.correct_predicted.mod <- glm(correct_predicted~phylum+depth, data=leaf.taxa, family="binomial")
print(c('BIC=',  BIC(phylumPdepth.correct_predicted.mod)))
# effect("phylum", phylumPdepth.correct_predicted.mod)

phylumTdepth.correct_predicted.mod <- glm(correct_predicted~phylum*depth, data=leaf.taxa, family="binomial")
print(c('BIC=',  BIC(phylumTdepth.correct_predicted.mod)))
# effect("phylum", phylumTdepth.correct_predicted.mod)

anova(phylumPdepth.correct_predicted.mod, phylumTdepth.correct_predicted.mod, test="LRT")


print('-------------------class + depth / * depth-----------------------')

classPdepth.correct_predicted.mod <- glm(correct_predicted~class+depth, data=leaf.taxa, family="binomial")
print(c('BIC=',  BIC(classPdepth.correct_predicted.mod)))

classTdepth.correct_predicted.mod <- glm(correct_predicted~class*depth, data=leaf.taxa, family="binomial")
print(c('BIC=',  BIC(classTdepth.correct_predicted.mod)))

anova(classPdepth.correct_predicted.mod, classTdepth.correct_predicted.mod, test="LRT")


print('-------------------order + depth / * depth-----------------------')

orderPdepth.correct_predicted.mod <- glm(correct_predicted~order+depth, data=leaf.taxa, family="binomial")
print(c('BIC=',  BIC(orderPdepth.correct_predicted.mod)))

orderTdepth.correct_predicted.mod <- glm(correct_predicted~order*depth, data=leaf.taxa, family="binomial")
print(c('BIC=',  BIC(orderTdepth.correct_predicted.mod)))

anova(orderPdepth.correct_predicted.mod, orderTdepth.correct_predicted.mod, test="LRT")


print('--------------------------------------------------')

format(Sys.time(), "%a %b %d %X %Y")



