library(data.table)
library(ggplot2)
library(effects)

all.taxa <- fread("~/Lydia_data/Eukaryota-taxa.csv")

### right mode for all
all.taxa$phylum <- as.factor(all.taxa$phylum)
all.taxa$class <- as.factor(all.taxa$class)
all.taxa$kingdom <- as.factor(all.taxa$kingdom)


heights <- do.call("rbind", strsplit(gsub("\\[|\\]", "", all.taxa$depths), ", "))

heights <- as.data.frame(apply(heights, 2, as.numeric))

names(heights) <- c("min.height", "max.height", "mean.height")

all.taxa <- cbind(all.taxa, heights)

table(all.taxa$kingdom)

table(all.taxa$kingdom, all.taxa$phylum)

summary(all.taxa$nr_children)

tapply(all.taxa$max.height, all.taxa$phylum, summary)

### phyla and kingdom nodes are not in the table
table(all.taxa$rank)[order(table(all.taxa$rank))]

### find out what is going on here...
table(all.taxa[all.taxa$nr_children==1, "rank"])

## pdf(path, width=8, height=6)
ggplot(all.taxa, aes(nr_children)) +
    geom_histogram() +
    scale_y_log10()
## dev.off()

inner.taxa <- all.taxa[all.taxa$nr_children>1, ]

inner.taxa <- as.data.frame(inner.taxa)

table(inner.taxa$rank)

tapply(inner.taxa$max.height, inner.taxa$rank, summary)

inner.taxa$multifurc <- inner.taxa$nr_children-2

ggplot(inner.taxa, aes(multifurc)) +
    geom_histogram() +
    scale_y_log10()


null.furc.mod <- glm(multifurc~1, data=inner.taxa,
                   family="poisson")


kingdomTheight.furc.mod <- glm(multifurc~kingdom*max.height, data=inner.taxa,
                              family="poisson")

kingdomPheight.furc.mod <- glm(multifurc~kingdom+max.height, data=inner.taxa,
                   family="poisson")

kingdom.furc.mod <- glm(multifurc~kingdom, data=inner.taxa,
                        family="poisson")

anova(kingdom.furc.mod, kingdomPheight.furc.mod, kingdomTheight.furc.mod, test="LRT")


phylumTheight.furc.mod <- glm(multifurc~phylum*max.height, data=inner.taxa,
                              family="poisson")

phylumPheight.furc.mod <- glm(multifurc~phylum+max.height, data=inner.taxa,
                   family="poisson")

phylum.furc.mod <- glm(multifurc~phylum, data=inner.taxa,
                        family="poisson")

anova(phylum.furc.mod, phylumPheight.furc.mod, phylumTheight.furc.mod, test="LRT")


classTheight.furc.mod <- glm(multifurc~class*max.height, data=inner.taxa,
                              family="poisson")

classPheight.furc.mod <- glm(multifurc~class+max.height, data=inner.taxa,
                   family="poisson")

class.furc.mod <- glm(multifurc~class, data=inner.taxa,
                      family="poisson")

anova(class.furc.mod, classPheight.furc.mod, classTheight.furc.mod, test="LRT")

effect("class", class.mod)

effect("class:max.height", classPh)


ggplot(inner.taxa, aes(rank, mean.height)) +
    geom_boxplot()

ggplot(inner.taxa, aes(phylum, max.height)) +
    geom_boxplot() +
    theme(axis.text.x = element_text(angle = 90, hjust = 1))

### if you want look at the package magitr to avoid such nested
### parantheses
## %>%

leaf.taxa <-  all.taxa[all.taxa$nr_children==0, ]
leaf.taxa$globi.data <- !is.na(leaf.taxa$originaltag)

null.globi.mod <- glm(globi.data~1,
                         data=leaf.taxa, family="binomial")

kingdom.globi.mod <- glm(globi.data~kingdom,
                         data=leaf.taxa, family="binomial")

summary(kingdom.globi.mod)

effect("kingdom", kingdom.globi.mod)

phylum.globi.mod <- glm(globi.data~phylum,
                        data=leaf.taxa, family="binomial")

summary(phylum.globi.mod)

effect("phylum", phylum.globi.mod)

anova(null.globi.mod, phylum.globi.mod)

phylum.globi.mod$aic

kingdom.globi.mod$aic
