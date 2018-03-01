# -------- -------- Prepare logfile and runtime computation -------- -------- #
echo "Logifle written to: build_data.log"
exec 3>&1 1>>build_data.log 2>&1            #write stdout 1,2 to logfile 3 to console
echo $(date)
start=$(date +%s)                           #get starting date

# -------- -------- get data and unzip -------- -------- #
cd data

if wget -q http://files.opentreeoflife.org/synthesis/opentree9.1/opentree9.1_tree.tgz -nv; then echo "OTT DL succesful"; else echo "OTT DL-link broken" 1>&3; exit 1;  fi    # download OTT and post error msg if link is unreachable
tar -xf opentree9.1_tree.tgz                #untar OTT
rm opentree9.1_tree.tgz
wait

if wget -q http://files.opentreeoflife.org/ott/ott3.0/ott3.0.tgz -nv; then echo "OTT DL succesful"; else echo "OTT DL-link broken" 1>&3; exit 1;  fi    # download OTT and post error msg if link is unreachable
tar -xf ott3.0.tgz
rm ott3.0.tgz
mv ott opentree3.1_taxonomic_tree
wait

cd GloBI_Dump
if wget -q https://depot.globalbioticinteractions.org/datasets/org/globalbioticinteractions/interactions/0.1/interactions-0.1-ott.zip -nv; then echo "GLoBI DL succesful"; else echo "GLoBI DL-link broken" 1>&3; exit 1;  fi
gunzip interactions.tsv.gz
wait

# -------- -------- remove zipped files -------- -------- #


echo "$(tput setaf 1)$(tput setab 7)------- Tree and Interaction-data downloaded --------$(tput sgr 0)" 1>&3