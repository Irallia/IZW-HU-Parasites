library(data.table)
# library(ggplot2)

format(Sys.time(), "%a %b %d %X %Y")

all.taxa <- fread("./Sarcopterygii-castor.csv")

print('------------all.taxa$originaltag------------------')
table(all.taxa$originaltag)
print('------------all.taxa$finaltag------------------')
table(all.taxa$finaltag)
print('--------------------------------------------------')

table(all.taxa[all.taxa$finaltag+1 != all.taxa$originaltag, ]$nr_children)



print('--------------------------------------------------')

format(Sys.time(), "%a %b %d %X %Y")
