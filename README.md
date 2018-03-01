# IZW-HU-Parasites
Project to find origins of parasitism in a pylogenetic tree of live.

## Getting Started

### Prerequisites

<!-- Setup node_7.9 and install needed packages in package.json -->

Install python 3 and R:
Install needed packages, see:
```
installed packages.md
```

### Installing

1. Clone Project:
```
git clone https://github.com/Irallia/IZW-HU-Parasites.git
```

2. Get Tree and Interaction data:
```
sh code/build_data.sh
```

### Metadata analysis, Maximum Parsimony, Evaluation

1. Build metadata files and run a Sankoff algorithm via castor package (for Eukaryota):
```
sh code/build_metadata-run_castor.sh
```

## Authors

* **Lydia Buntrock** - **

See also the list of [contributors](https://github.com/your/project/contributors) who participated in this project.

## Acknowledgments

* See also:
```https://github.com/majuss/globi-parasites.git```.

<!-- 
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
- Attribute aufteilen, parasitismus von vertebraten/... -->

**Future work:**

- Add symbiontic or other attributes to the nodes.
- Parsimony analysis of coevolving species associations + recontruction the history of host-parasite associations. Recontruction the history of host-parasite associations.
- enrichment tests. Analyse der Zusammensetzung von Species. Tree über funktionen...
- add Branchlenght: time / DNA / other distances -> DB mit Divergenzzeiten
