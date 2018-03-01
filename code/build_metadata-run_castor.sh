# -------- -------- Prepare logfile and runtime computation -------- -------- #
echo "Logifle written to: build_metadata.log"
exec 3>&1 1>>build_metadata.log 2>&1            #write stdout 1,2 to logfile 3 to console
echo $(date)
start=$(date +%s)                           #get starting date

mkdir logs

# -------- -------- build metadata files -------- -------- #
python3 -m code.metadata.extract_globi_data > logs/log-extract_globi_data.txt
echo "$(tput setaf 1)$(tput setab 7)------- Free-livings and Parasites extracted (3/7) --------$(tput sgr 0)" 1>&3
python3 -m code.metadata.build_subtree ott304358 Eukaryota > logs/log-build_subtrees.txt
echo "$(tput setaf 1)$(tput setab 7)------- Subtrees builded(4/7) --------$(tput sgr 0)" 1>&3
python3 -m code.metadata.build_nodelist > logs/log-build_nodelist.txt
echo "$(tput setaf 1)$(tput setab 7)------- Nodelists builded(5/7) --------$(tput sgr 0)" 1>&3

# -------- -------- run castor files -------- -------- #
python3 -m code.castor.run_castor > logs/log-run_castor.txt
echo "$(tput setaf 1)$(tput setab 7)------- Maximum Parsimony: Sankoff (Castor) ready(6/7) --------$(tput sgr 0)" 1>&3

# -------- -------- build more metadata files -------- -------- #
python3 -m code.metadata.extend_nodelist_taxa kingdom > logs/log-extend_nodelist_taxa-kingdom.txt
python3 -m code.metadata.extend_nodelist_taxa phylum > logs/log-extend_nodelist_taxa-phylum.txt
python3 -m code.metadata.extend_nodelist_taxa class > logs/log-extend_nodelist_taxa-class.txt
python3 -m code.metadata.extend_nodelist_taxa order > logs/log-extend_nodelist_taxa-order.txt
python3 -m code.metadata.extend_nodelist > logs/log-extend_nodelist.txt

echo "$(tput setaf 1)$(tput setab 7)------- Castor Results and Taxa: Kingdom, Phylum, Class, Order added to nodelist (7/7) --------$(tput sgr 0)" 1>&3

end=$(date +%s)                         #get end-date
runtime=$(((end-start)/60))             #calculate runtime
echo "$runtime minutes" 
echo "$(tput setaf 1)$(tput setab 7)This run took $runtime minutes$(tput sgr 0)" 1>&3