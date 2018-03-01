# IZW-HU-Parasites
Project to find origins of parasitism in a pylogenetic tree of live.

## Getting Started

Clone Project:
```
git clone https://github.com/Irallia/IZW-HU-Parasites.git
```
Get Tree and Interaction data:
```
sh code/build_data.sh
```
Build metadata files (for Eukaryota):
```
sh code/build_metadata-run_castor.sh
```
---
### Prerequisites

Setup arangodb and node_7.9 and install needed packages in package.json

### Installing

1. Clone Repo

```
git clone https://github.com/Irallia/IZW-HU-Parasites.git
```

2. Download globi's .tsv dump:
```
wget https://s3.amazonaws.com/globi/snapshot/target/data/tsv/interactions.tsv.gz
```

Import the extraced tsv-dump with:
```
arangoimp --file interactions.tsv --type tsv --collection interaction_tsv --create-collection true
```

## Authors

* **Lydia Buntrock** - **

See also the list of [contributors](https://github.com/your/project/contributors) who participated in this project.

## Acknowledgments

* Based on ```https://github.com/majuss/globi-parasites.git```.


# Done
- give all nodes without ott ids pseudo ids (higher value than all ott ids)
- rebuild the json to graph style (nodes, edges collections) (json and tsv available)
- Plot: number of children per node
- (Presentation)
- tested Tree for cycles -> no cycles

# ToDo's

**Currently working on:**
- write a motivation (in the thesis)
- TMC to parsimony


- add attributes parasitic / freeliving on every leaf node
- Define possible algorithms for calculating node properties. 
- Have a look at phylogeny programms: Raxml, mrbayes, beast. (http://evolution.genetics.washington.edu/phylip/software.html#systems)
- run Marius Algorithm on my tree
- Analyse Marius Algorithm (cross evaluation / leave one out evaluation)

**In the long run:**

- Use / attach / implement an algorithm to give the inner nodes attribute 'parasite' or 'freeliving'. → Find origins for parasitism.
- Attribute aufteilen, parasitismus von vertebraten/...

**Future work:**

- Add symbiontic or other attributes to the nodes.
- Parsimony analysis of coevolving species associations + recontruction the history of host-parasite associations. Recontruction the history of host-parasite associations.
- enrichment tests. Analyse der Zusammensetzung von Species. Tree über funktionen...
- add Branchlenght: time / DNA / other distances -> DB mit Divergenzzeiten

## Update things
### update arango db:
download Client Tools for Debian 9.0 from https://www.arangodb.com/download-major/debian/

```
wget https://download.arangodb.com/arangodb32/Debian_9.0/amd64/arangodb3-3.2.3-1_amd64.deb
sudo aptitude update
sudo aptitude upgrade
reboot
sudo dpkg -i arangodb3-3.2.3-1_amd64.deb
```
