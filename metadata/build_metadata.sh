
# -------- -------- Prepare logfile and runtime computation -------- -------- #
echo "Logifle written to: build_data.log"
exec 3>&1 1>>build_data.log 2>&1            #write stdout 1,2 to logfile 3 to console
echo $(date)
start=$(date +%s)                           #get starting date
# -------- -------- install node packages -------- -------- #
# ToDo!
echo "$(tput setaf 1)$(tput setab 7)------- packages installed (1/7) --------$(tput sgr 0)" 1>&3
# -------- -------- cleanup and build filesystem -------- -------- #
rm -rf data                                 #delete preexisting data dir
mkdir data                                  #make data dir
cd data
# -------- -------- get data and unzip -------- -------- #
if wget -q http://files.opentreeoflife.org/synthesis/opentree9.1/opentree9.1_tree.tgz -nv; then echo "OTT DL succesful"; else echo "OTT DL-link broken" 1>&3; exit 1;  fi    # download OTT and post error msg if link is unreachable
tar -xf opentree9.1_tree.tgz                #untar OTT
rm opentree9.1_tree.tgz                     #remove .tar
wait
mkdir GLoBI_Dump
cd GLoBI_Dump
if wget -q https://depot.globalbioticinteractions.org/datasets/org/globalbioticinteractions/interactions/0.1/interactions-0.1-ott.zip -nv; then echo "GLoBI DL succesful"; else echo "GLoBI DL-link broken" 1>&3; exit 1;  fi
unzip interactions-0.1-ott.zip
gunzip interactions.tsv.gz
echo "$(tput setaf 1)$(tput setab 7)------- Tree and Interaction-data downloaded (2/7) --------$(tput sgr 0)" 1>&3
# -------- -------- build metadata files -------- -------- #
cd ../../metadata
extract_globi_data.py > log-extract_globi_data.txt
echo "$(tput setaf 1)$(tput setab 7)------- Free-livings and Parasites extracted (3/7) --------$(tput sgr 0)" 1>&3
python3 build_subtrees.py > log-build_subtrees.txt
echo "$(tput setaf 1)$(tput setab 7)------- Subtrees builded(4/7) --------$(tput sgr 0)" 1>&3
python3 build_nodelist.py > log-build_nodelist.txt
echo "$(tput setaf 1)$(tput setab 7)------- Nodelists builded(5/7) --------$(tput sgr 0)" 1>&3
mkdir bufferfiles
python3 run_castor.py > log-run_castor.txt
echo "$(tput setaf 1)$(tput setab 7)------- Maximum Parsimony: Sankoff (Castor) ready(6/7) --------$(tput sgr 0)" 1>&3
# ToDo: Result analysis...
echo "$(tput setaf 1)$(tput setab 7)------- Results....(7/7) --------$(tput sgr 0)" 1>&3

end=$(date +%s)                         #get end-date
runtime=$(((end-start)/60))             #calculate runtime
echo "$runtime minutes" 
echo "$(tput setaf 1)$(tput setab 7)This run took $runtime minutes$(tput sgr 0)" 1>&3