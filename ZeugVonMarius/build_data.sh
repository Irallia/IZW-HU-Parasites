#!/bin/bash

# Build system for the required data

mkdir data
cd data
wget https://s3.amazonaws.com/globi/snapshot/target/data/tsv/interactions.tsv.gz
gunzip interactions.tsv.gz
wget http://files.opentreeoflife.org/ott/ott3.0/ott3.0.tgz
tar -xvf ott3.0.tgz
rm ott3.0.tgz
mv ott/taxonomy.tsv .
rm -rf ott