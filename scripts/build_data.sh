#!/bin/bash

# Build system for everything. This will take about 60 minutes (8 cores ivy bridge, 64 GB RAM)
# -------- -------- Prepare logfile and runtime computation -------- -------- #
echo "Logifle written to: build_data.log"
exec 3>&1 1>>build_data.log 2>&1            #write stdout 1,2 to logfile 3 to console
echo $(date)
start=$(date +%s)                           #get starting date
# -------- -------- install node packages -------- -------- #
npm i arangojs fastango3 bfj jsonexport     #install js packages
echo "$(tput setaf 1)$(tput setab 7)------- Node packages installed (1/8) --------$(tput sgr 0)" 1>&3
# -------- -------- cleanup and build filesystem -------- -------- #
rm -rf data                                 #delete preexisting data dir
mkdir data                                  #make data dir
cd data                                     #change dir into data

# -------- -------- get data and unzip -------- -------- #
if wget -q https://s3.amazonaws.com/globi/snapshot/target/data/tsv/interactions.tsv.gz -nv; then echo "GLoBI DL succesful"; else echo "GLoBI DL-link broken" 1>&3; exit 1;  fi
gunzip interactions.tsv.gz
if wget -q http://files.opentreeoflife.org/synthesis/opentree9.1/opentree9.1_tree.tgz -nv; then echo "OTT DL succesful"; else echo "OTT DL-link broken" 1>&3; exit 1;  fi    # download OTT and post error msg if link is unreachable
tar -xf opentree9.1_tree.tgz                #untar OTT
rm opentree9.1_tree.tgz                     #remove .tar
wait
echo "$(tput setaf 1)$(tput setab 7)------- Tree and Interaction-data downloaded (2/8) --------$(tput sgr 0)" 1>&3
# -------- -------- interactions: add to arangodb and tag entries -------- -------- #
arangosh --server.authentication false --javascript.execute-string 'db._drop("interaction_tsv");
                                                                    db._drop("nodes_otl");
                                                                    db._drop("edges_otl")'
#dropping and creating all nec. collections inside arangoDB (moved partially into create_cols)
arangoimp --file interactions.tsv --type tsv --collection interaction_tsv --create-collection true --server.authentication false
wait
echo "$(tput setaf 1)$(tput setab 7)------- Interactions imported and collections initialized (3/8) --------$(tput sgr 0)" 1>&3
# node ../scripts/marius/tag_interactionstsv_freelivings.js
# node ../scripts/marius/tag_interactionstsv_parass.js
# node ../scripts/marius/tag_interactionstsv_parast.js
# node ../scripts/marius/tag_interactionstsv_freelivingt.js
node ../scripts/marius/tag_interactionsts.js    #tag all queried interaction entries in interacion_tsv
echo "$(tput setaf 1)$(tput setab 7)------- interactions tagged (3,5/8) --------$(tput sgr 0)" 1>&3
# -------- -------- tree: prepare and add to arangodb -------- -------- #
npm install newick
npm install biojs-io-newick
mkdir tree
mkdir tree/labelled_supertree
node --max_old_space_size=4096 ../scripts/buildTree/prepareJson.js
echo "$(tput setaf 1)$(tput setab 7)------- tree prepared (3,75/8) --------$(tput sgr 0)" 1>&3
arangoimp --file tree/labelled_supertree/ottnames-nodes.tsv --type tsv --collection nodes_otl --create-collection true --server.authentication false
arangoimp --file tree/labelled_supertree/ottnames-edges.tsv --type tsv --collection edges_otl --create-collection-type edge --create-collection true --server.authentication false
wait
echo "$(tput setaf 1)$(tput setab 7)------- Interaction entries tagged; OTL Tree imported (4/8) --------$(tput sgr 0)" 1>&3
# # node build_freeliving_source.js
# node build_freeliving_target.js
# node build_parasites_source.js
# node build_parasites_target.js
node ../scripts/tagTree/tag_tree_freeliving_source.js   #build sub-tree from freeliving (source) tagged interaction_tsv entries
node ../scripts/tagTree/tag_tree_freeliving_target.js   #build sub-tree from freeliving (target) tagged interaction_tsv entries
node ../scripts/tagTree/tag_tree_parasites_source.js    #build sub-tree from parasites (source) tagged interaction_tsv entries
node ../scripts/tagTree/tag_tree_parasites_target.js    #build sub-tree from parasites (target) tagged interaction_tsv entries
wait
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
end=$(date +%s)                         #get end-date
runtime=$(((end-start)/60))             #calculate runtime
echo "$runtime minutes" 
echo "$(tput setaf 1)$(tput setab 7)This run took $runtime minutes$(tput sgr 0)" 1>&3