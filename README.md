# IZW-HU-Parasites
Project to find origins of parasitism in a pylogenetic tree of live.

## Getting Started

connect to the VM (via Cygwin64):
```
ssh ***REMOVED*** -L 127.0.0.1:8529:127.0.0.1:8529 -p 15351 -q
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

* **Lydia Buntrock** - *Initial work*

See also the list of [contributors](https://github.com/your/project/contributors) who participated in this project.

## Acknowledgments

* Based on ```https://github.com/majuss/globi-parasites.git```.

# ToDo's

**Currently working on:**

- give all nodes without ott ids pseudo ids (higher value than all ott ids)
- rebuild the json to graph style (nodes, edges collections)

**In the long run:**

- add attributes parasitic / freeliving on every node
- Implement an algorithm to give the nodes attribute 'parasite' or 'freeliving'.

**Future work:**

- Find origins for parasitism.
- Add symbiontic or other attributes to the nodes.
