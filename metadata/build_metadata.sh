
# -------- -------- cleanup and build filesystem -------- -------- #
rm -rf data                                 #delete preexisting data dir
mkdir data                                  #make data dir
cd data

# -------- -------- get data and unzip -------- -------- #
mkdir GLoBI_Dump
cd GLoBI_Dump

if wget -q https://depot.globalbioticinteractions.org/datasets/org/globalbioticinteractions/interactions/0.1/interactions-0.1-ott.zip -nv; then echo "GLoBI DL succesful"; else echo "GLoBI DL-link broken" 1>&3; exit 1;  fi
unzip interactions-0.1-ott.zip
gunzip interactions.tsv.gz

# -------- -------- build metadata files -------- -------- #
cd ../../metadata
extract_globi_data.py