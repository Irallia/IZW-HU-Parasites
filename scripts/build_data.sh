#!/bin/bash

# Build system for everything this will take about X minutes (8 cores ivy bridge, 64 GB RAM)
echo "Logifle written to: build_data.log"
exec 3>&1 1>>build_data.log 2>&1
echo $(date)
start=$(date +%s)
npm i arangojs fastango3
echo "$(tput setaf 1)$(tput setab 7)------- Node packages installed (1/8) --------$(tput sgr 0)" 1>&3
# rm -rf data
# mkdir data
# cd data
# mkdir interactions
# mkdir tree
# cd interactions
# if wget -q https://s3.amazonaws.com/globi/snapshot/target/data/tsv/interactions.tsv.gz -nv; then echo "GLoBI DL succesful"; else echo "GLoBI DL-link broken" 1>&3; exit 1;  fi
# gunzip interactions.tsv.gz
# cd ../tree
# if wget -q http://files.opentreeoflife.org/synthesis/opentree9.1/opentree9.1_tree.tgz -nv; then echo "OTT DL succesful"; else echo "OTL DL-link broken" 1>&3; exit 1;  fi
# tar -xf ott3.0.tgz 
# rm opentree9.1_tree.tgz 

# mv ott/taxonomy.tsv . 
# rm -rf ott
# sed -i '27272s/kingdom/subkingdom/' taxonomy.tsv #correction rank of Chloroplastida #sed -i '27272s/phylum/no rank/' taxonomy.tsv #Streptophyta #sed -i '27272s/phylum/no rank/' taxonomy.tsv #Tracheophyta #sed -i '27272s/phylum/no rank/' taxonomy.tsv #Magnoliophyta #sed -i '27272s/kingdom/subkingdom/' taxonomy.tsv #Rhodophyta #sed -i '27272s/kingdom/subkingdom/' taxonomy.tsv #Chlorophyta
# wait
# echo "$(tput setaf 1)$(tput setab 7)------- Tree and Interaction-data downloaded (2/8) --------$(tput sgr 0)" 1>&3
# #Initializing the collections
# arangosh --server.authentication false --javascript.execute-string 'db._drop("interaction_tsv");
#                                                                     db._drop("nodes_otl");
#                                                                     db._drop("edges_otl");
#                                                                     db._drop("nodes_otl_bak");
#                                                                     db._drop("edges_otl_bak");
#                                                                     db._drop("counts");
#                                                                     db._drop("nodes_otl_sub");
#                                                                     db._drop("edges_otl_sub");
#                                                                     db._drop("weinstein");
#                                                                     db._drop("weinstein_noott");
#                                                                     db._drop("nodes_otl_sub_bak");
#                                                                     db._drop("edges_otl_sub_bak");
#                                                                     db._createEdgeCollection("edges_otl");
#                                                                     db._create("nodes_otl");
#                                                                     db._createEdgeCollection("edges_otl_bak");
#                                                                     db._createEdgeCollection("edges_otl_sub_bak");
#                                                                     db._create("nodes_otl_sub_bak");
#                                                                     db._create("nodes_otl_bak");
#                                                                     db._create("counts");
#                                                                     db._create("nodes_otl_sub");
#                                                                     db._createEdgeCollection("edges_otl_sub");
#                                                                     db._create("nodes_otl_metazoa")'

# arangoimp --file interactions.tsv --type tsv --collection interaction_tsv --create-collection true --server.authentication false
# wait
# echo "$(tput setaf 1)$(tput setab 7)------- Interactions imported and collections initialized (3/8) --------$(tput sgr 0)" 1>&3
# cd ..
# bash weinstein/build_weinstein-tsv.sh weinstein/weinstein_extract.md data/taxonomy.tsv &
node scripts/marius/tagging/tag_interactionstsv_freelivings.js
node scripts/marius/tagging/tag_interactionstsv_parass.js
node scripts/marius/tagging/tag_interactionstsv_parast.js
node scripts/marius/tagging/tag_interactionstsv_freelivingt.js
# node edgesimport_otl.js &
# node nodesimport_otl.js
wait
# arangosh --server.authentication false --javascript.execute-string 'db._query("FOR doc in nodes_otl INSERT doc IN nodes_otl_bak");
#                                                                     db._query("FOR doc in edges_otl INSERT doc IN edges_otl_bak");' 
echo "$(tput setaf 1)$(tput setab 7)------- Interaction entries tagged; Weinstein2016 data created; OTL Tree imported (4/8) --------$(tput sgr 0)" 1>&3
# node build_freeliving_source.js
# node build_freeliving_target.js
# node build_parasites_source.js
# node build_parasites_target.js
# wait
# arangosh --server.authentication false --javascript.execute-string 'db._query("FOR doc in nodes_otl_sub INSERT doc IN nodes_otl_sub_bak");
#                                                                     db._query("FOR doc in edges_otl_sub INSERT doc IN edges_otl_sub_bak");' 
# wait
# echo "$(tput setaf 1)$(tput setab 7)------- Tagging tree and creating noWein done (5/8) --------$(tput sgr 0)" 1>&3
# arangoimp --file weinstein/weinstein.tsv --type tsv --collection weinstein --create-collection true --server.authentication false
# arangoimp --file weinstein/weinstein_manual.tsv --type tsv --collection weinstein --create-collection false --server.authentication false 
# echo "$(tput setaf 1)$(tput setab 7)------- Done importing weinstein2016 (6/8) --------$(tput sgr 0)" 1>&3
# echo "$(tput setaf 1)$(tput setab 7)------- Done generating counts (7/8) --------$(tput sgr 0)" 1>&3
# node write_pis.js
# node taxonomic_majority_censoring.js
# node find_origins.js
# node tagging/tag_origins_toTree.js
# arangosh --server.authentication false --javascript.execute-string 'db._query(`UPDATE "304358" with {freeliving:1, freelivingw:1} in nodes_otl`);'
# node tagging/tag_ott_pfl.js
# node tagging/tag_ott_pfl_wein.js
# node counting/generate_counts.js
# node weinstein/import_origin_counts.js
# node counting/tag_counts_fulltree.js
# echo "$(tput setaf 1)$(tput setab 7)------- Done generating PIs, calculating origins and tag origin counts (8/8) --------$(tput sgr 0)" 1>&3
# end=$(date +%s)
# runtime=$(((end-start)/60))
# echo "$runtime minutes" 
# echo "$(tput setaf 1)$(tput setab 7)This run took $runtime minutes$(tput sgr 0)" 1>&3