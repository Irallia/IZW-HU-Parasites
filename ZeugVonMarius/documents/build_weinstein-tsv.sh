#!/bin/bash
#
#This file takes the extracted species/parasites list from Weinstein 2016
#and is getting the OTT-IDs for every entry from the taxonomy.tsv
#Format for Weinstein extract:
#
#Species A
#Species B
#Species C
#
#You have to create this file manually with word 2013+ and the advaced search. Then search for bold printed strings inside the Weinstein2016
#supplementary data: http://datadryad.org/resource/doi:10.5061/dryad.70628
#
#
#Second input file is the taxonomy.tsv from openTreeofLife
#
rm weinstein.txt
while IFS='' read -r line || [[ -n "$line" ]]; do
    grep "$line" "$2" | head -1 >> ../data/weinstein.tsv
done < "$1"
