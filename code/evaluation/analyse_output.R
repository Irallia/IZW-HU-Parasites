library(data.table)
# library(ggplot2)

format(Sys.time(), "%a %b %d %X %Y")

all.taxa <- fread("../../results/Eukaryota-taxa.csv")
# ott_id,originaltag,finaltag,depth,heights,nr_children,name,rank,uniqname,kingdom,phylum,class,order,family

### right mode for all
all.taxa$kingdom <- as.factor(all.taxa$kingdom)
all.taxa$phylum <- as.factor(all.taxa$phylum)
all.taxa$class <- as.factor(all.taxa$class)
all.taxa$order <- as.factor(all.taxa$order)


heights <- do.call("rbind", strsplit(gsub("\\[|\\]", "", all.taxa$heights), ", "))

heights <- as.data.frame(apply(heights, 2, as.numeric))

names(heights) <- c("min.height", "max.height", "mean.height")

all.taxa <- cbind(all.taxa, heights)

# print('------------all.taxa$originaltag------------------')
# table(all.taxa$originaltag)
# print('------------all.taxa$finaltag------------------')
# table(all.taxa$finaltag)

print('--------------------------------------------------')

leaf.taxa <-  all.taxa[all.taxa$nr_children==0, ]

print('--------------------------------------------------')




# print('-------------Are the changed originaltags?--------------')
# table(leaf.taxa[leaf.taxa$finaltag+1 != leaf.taxa$originaltag, ]$kingdom)


print('-----------Analyse some Phyla about their prediciton-------------')
print('-----------Metazoa-------------')
metazoa <- leaf.taxa[leaf.taxa$kingdom=="['ott691846', 'Metazoa']", ]
# # table(metazoa$phylum, metazoa$originaltag)
print('--------Leaf nodes:------------')
# table(droplevels(all.taxa[all.taxa$nr_children==0, ]$phylum))
print('----------Parasites / Free-livings - original states:---------------')

print('-----------Chordata-------------')
chordata <- metazoa[metazoa$phylum=="['ott125642', 'Chordata']", ]
table(chordata$originaltag)
print('----------final:--------------')
table(chordata$finaltag)

print('-----------Nematoda-------------')
nematoda <- metazoa[metazoa$phylum=="['ott395057', 'Nematoda']", ]
table(nematoda$originaltag)
print('----------final:--------------')
table(nematoda$finaltag)

print('-----------Platyhelminthes-------------')
platyhelminthes <- metazoa[metazoa$phylum=="['ott555379', 'Platyhelminthes']", ]
table(platyhelminthes$originaltag)
print('----------final:--------------')
table(platyhelminthes$finaltag)
print('------------------------')
# table(platyhelminthes[platyhelminthes$finaltag==0, ]$name)

print('-----------Apicomplexa-------------')
apicomplexa <- leaf.taxa[leaf.taxa$phylum=="['ott422673', 'Apicomplexa']", ]
table(apicomplexa$originaltag)
table(apicomplexa[apicomplexa$originaltag==1, ]$name)

print('----------final:--------------')
table(apicomplexa$finaltag)
print('------------------------')
table(apicomplexa[apicomplexa$finaltag==0, ]$name)



print('-------------More about Chordata:-----------')
print('--------Classes with parasites:-------')
table(droplevels(chordata[chordata$finaltag==1, ]$class))
Actinopteri <- chordata[chordata$class=="['ott285821', 'Actinopteri']", ]
Sarcopterygii <- chordata[chordata$class=="['ott458402', 'Sarcopterygii']", ]
print('--------Orders with parasites:-------')
table(droplevels(Actinopteri[Actinopteri$originaltag==2, ]$order))
table(droplevels(Actinopteri[Actinopteri$finaltag==1, ]$order))
print('------------')
table(droplevels(Sarcopterygii[Sarcopterygii$originaltag==2, ]$order))
table(droplevels(Sarcopterygii[Sarcopterygii$finaltag==1, ]$order))

Cypriniformes <- chordata[chordata$order=="['ott1005931', 'Cypriniformes']", ]
Sauria <- chordata[chordata$order=="['ott329823', 'Sauria']", ]
Anura <- chordata[chordata$order=="['ott991547', 'Anura']", ]
Acanthomorphata <- chordata[chordata$order=="['ott108720', 'Acanthomorphata']", ]
Siluriformes <- chordata[chordata$order=="['ott701516', 'Siluriformes']", ]
print('--------Families with parasites:-------')

table(Cypriniformes[Cypriniformes$finaltag==1, ]$family)
table(Cypriniformes[Cypriniformes$finaltag==1, ]$name)
print('------------------------')
table(Sauria[Sauria$finaltag==1, ]$family)
print('------------------------')
table(Anura[Anura$finaltag==1, ]$name)
print('------------------------')
table(Acanthomorphata[Acanthomorphata$finaltag==1, ]$name)
Blenniidae <- Acanthomorphata[Acanthomorphata$family=="['ott867524', 'Blenniidae']", ]
table(Blenniidae[Blenniidae$finaltag==1, ]$name)
print('------------------------')
table(Siluriformes[Siluriformes$finaltag==1, ]$name)
print('------------------------')
table(Sauria[Sauria$finaltag==1, ]$family)
table(Sauria[Sauria$finaltag==1, ]$name)




format(Sys.time(), "%a %b %d %X %Y")
