#!/bin/bash

# Build system for everything this will take about X minutes (8 cores ivy bridge, 64 GB RAM)
echo "Logifle written to: build_data.log"
exec 3>&1 1>>build_data.log 2>&1
echo $(date)
start=$(date +%s)
npm i arangojs fastango3
echo "$(tput setaf 1)$(tput setab 7)------- Node packages installed (1/8) --------$(tput sgr 0)" 1>&3
rm -rf data # delete old stuff
mkdir data
cd data
if wget -q https://s3.amazonaws.com/globi/snapshot/target/data/tsv/interactions.tsv.gz -nv; then echo "GLoBI DL succesful"; else echo "GLoBI DL-link broken" 1>&3; exit 1;  fi
gunzip interactions.tsv.gz
if wget -q http://files.opentreeoflife.org/synthesis/opentree9.1/opentree9.1_tree.tgz -nv; then echo "OTT DL succesful"; else echo "OTL DL-link broken" 1>&3; exit 1;  fi
tar -xf ott3.0.tgz 
rm opentree9.1_tree.tgz 
mv ott/taxonomy.tsv . 
rm -rf ott
sed -i '27272s/kingdom/subkingdom/' taxonomy.tsv #correction rank of Chloroplastida #sed -i '27272s/phylum/no rank/' taxonomy.tsv #Streptophyta #sed -i '27272s/phylum/no rank/' taxonomy.tsv #Tracheophyta #sed -i '27272s/phylum/no rank/' taxonomy.tsv #Magnoliophyta #sed -i '27272s/kingdom/subkingdom/' taxonomy.tsv #Rhodophyta #sed -i '27272s/kingdom/subkingdom/' taxonomy.tsv #Chlorophyta
wait
echo "$(tput setaf 1)$(tput setab 7)------- Tree and Interaction-data downloaded (2/8) --------$(tput sgr 0)" 1>&3
#Initializing the collections (and delete old stuff)
arangosh --server.authentication false --javascript.execute-string 'db._drop("interaction_tsv")'
arangoimp --file interactions.tsv --type tsv --collection interaction_tsv --create-collection true --server.authentication false
wait
echo "$(tput setaf 1)$(tput setab 7)------- Interactions imported and collections initialized (3/8) --------$(tput sgr 0)" 1>&3
cd ../scripts
node marius/tagging/tag_interactionstsv_freelivings.js
node marius/tagging/tag_interactionstsv_parass.js
node marius/tagging/tag_interactionstsv_parast.js
node marius/tagging/tag_interactionstsv_freelivingt.js
# TODO:
# node buildTree/prepareJson.js

# wait
# arangosh --server.authentication false --javascript.execute-string 'db._query("FOR doc in nodes_otl INSERT doc IN nodes_otl_bak");
#                                                                     db._query("FOR doc in edges_otl INSERT doc IN edges_otl_bak");' 
# echo "$(tput setaf 1)$(tput setab 7)------- Interaction entries tagged; Weinstein2016 data created; OTL Tree imported (4/8) --------$(tput sgr 0)" 1>&3
# node build_freeliving_source.js
# node build_freeliving_target.js
# node build_parasites_source.js
# node build_parasites_target.js
# wait
# arangosh --server.authentication false --javascript.execute-string 'db._query("FOR doc in nodes_otl_sub INSERT doc IN nodes_otl_sub_bak");
#                                                                     db._query("FOR doc in edges_otl_sub INSERT doc IN edges_otl_sub_bak");' 
# wait
# echo "$(tput setaf 1)$(tput setab 7)------- Done generating counts (7/8) --------$(tput sgr 0)" 1>&3
# node write_pis.js
# node taxonomic_majority_censoring.js
# node find_origins.js
# node tagging/tag_origins_toTree.js
# arangosh --server.authentication false --javascript.execute-string 'db._query(`UPDATE "304358" with {freeliving:1, freelivingw:1} in nodes_otl`);'
# node tagging/tag_ott_pfl.js
# node tagging/tag_ott_pfl_wein.js
# node counting/generate_counts.js
# node counting/tag_counts_fulltree.js
# echo "$(tput setaf 1)$(tput setab 7)------- Done generating PIs, calculating origins and tag origin counts (8/8) --------$(tput sgr 0)" 1>&3
# end=$(date +%s)
# runtime=$(((end-start)/60))
# echo "$runtime minutes" 
# echo "$(tput setaf 1)$(tput setab 7)This run took $runtime minutes$(tput sgr 0)" 1>&3