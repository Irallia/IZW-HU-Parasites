#!/bin/bash

# Build system for everything this will take about X minutes (8 cores ivy bridge, 64 GB RAM)
# -------- -------- Prepare logfile and runtime computation -------- -------- #
echo "Logifle written to: build_data.log"
exec 3>&1 1>>build_data.log 2>&1
echo $(date)
start=$(date +%s)
# -------- -------- install node packages -------- -------- #
npm i arangojs fastango3
echo "$(tput setaf 1)$(tput setab 7)------- Node packages installed (1/8) --------$(tput sgr 0)" 1>&3
# -------- -------- cleanup and build filesystem -------- -------- #
rm -rf data # delete old stuff
mkdir data
cd data
# -------- -------- get data and unzip -------- -------- #
if wget -q https://s3.amazonaws.com/globi/snapshot/target/data/tsv/interactions.tsv.gz -nv; then echo "GLoBI DL succesful"; else echo "GLoBI DL-link broken" 1>&3; exit 1;  fi
gunzip interactions.tsv.gz
if wget -q http://files.opentreeoflife.org/synthesis/opentree9.1/opentree9.1_tree.tgz -nv; then echo "OTT DL succesful"; else echo "OTL DL-link broken" 1>&3; exit 1;  fi
tar -xf opentree9.1_tree.tgz 
rm opentree9.1_tree.tgz 
wait
echo "$(tput setaf 1)$(tput setab 7)------- Tree and Interaction-data downloaded (2/8) --------$(tput sgr 0)" 1>&3
#Initializing the collections (and delete old stuff)
# -------- -------- interactions: add to arangodb and tag entries -------- -------- #
arangosh --server.authentication false --javascript.execute-string 'db._drop("interaction_tsv");
                                                                    db._drop("nodes_otl");
                                                                    db._drop("edges_otl")'
arangoimp --file interactions.tsv --type tsv --collection interaction_tsv --create-collection true --server.authentication false
wait
echo "$(tput setaf 1)$(tput setab 7)------- Interactions imported and collections initialized (3/8) --------$(tput sgr 0)" 1>&3
node ../scripts/marius/tagging/tag_interactionstsv_freelivings.js
node ../scripts/marius/tagging/tag_interactionstsv_parass.js
node ../scripts/marius/tagging/tag_interactionstsv_parast.js
node ../scripts/marius/tagging/tag_interactionstsv_freelivingt.js
echo "$(tput setaf 1)$(tput setab 7)------- interactions tagged (3,5/8) --------$(tput sgr 0)" 1>&3
# -------- -------- tree: prepare and add to arangodb -------- -------- #
npm install newick
mkdir tree
mkdir tree/labelled_supertree
node --max_old_space_size=4096 ../scripts/buildTree/prepareJson.js
echo "$(tput setaf 1)$(tput setab 7)------- tree prepared (3,75/8) --------$(tput sgr 0)" 1>&3
arangoimp --file tree/labelled_supertree/ottnames-nodes.tsv --type tsv --collection nodes_otl --create-collection true --server.authentication false
arangoimp --file tree/labelled_supertree/ottnames-edges.tsv --type tsv --collection edges_otl --create-collection-type edge --create-collection true --server.authentication false
wait
echo "$(tput setaf 1)$(tput setab 7)------- Interaction entries tagged; OTL Tree imported (4/8) --------$(tput sgr 0)" 1>&3
# # node build_freeliving_source.js
# # node build_freeliving_target.js
# # node build_parasites_source.js
# # node build_parasites_target.js
# node ../scripts/marius/tagging/tag_tree_freeliving_source.js
# node ../scripts/marius/tagging/tag_tree_freeliving_target.js
# node ../scripts/marius/tagging/tag_tree_parasites_source.js
# node ../scripts/marius/tagging/tag_tree_parasites_target.js
# wait
# arangosh --server.authentication false --javascript.execute-string 'db._query("FOR doc in nodes_otl_sub INSERT doc IN nodes_otl_sub_bak");
#                                                                     db._query("FOR doc in edges_otl_sub INSERT doc IN edges_otl_sub_bak");' 
# wait
# echo "$(tput setaf 1)$(tput setab 7)------- Done generating counts (7/8) --------$(tput sgr 0)" 1>&3
# node write_pis.js
# node taxonomic_majority_censoring.js
# node find_origins.js
# arangosh --server.authentication false --javascript.execute-string 'db._query(`UPDATE "304358" with {freeliving:1, freelivingw:1} in nodes_otl`);'
# node counting/tag_counts_fulltree.js
# echo "$(tput setaf 1)$(tput setab 7)------- Done generating PIs, calculating origins and tag origin counts (8/8) --------$(tput sgr 0)" 1>&3
end=$(date +%s)
runtime=$(((end-start)/60))
echo "$runtime minutes" 
echo "$(tput setaf 1)$(tput setab 7)This run took $runtime minutes$(tput sgr 0)" 1>&3