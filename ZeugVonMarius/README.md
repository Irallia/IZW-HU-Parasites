connect to the VM:
```
ssh h -L 127.0.0.1:8529:127.0.0.1:8529 -p 15350 -q
```
---
1. Setup arangodb and node_7.9 and install needed packages in package.json

2. Download globi's .tsv dump:
```
wget https://s3.amazonaws.com/globi/snapshot/target/data/tsv/interactions.tsv.gz
```

Import the extraced tsv-dump with:
```
arangoimp --file interactions.tsv --type tsv --collection interaction_tsv --create-collection true
```

3. **import open tree of life dump**

```
http://files.opentreeoflife.org/ott/ott3.0/ott3.0.tgz
```
Extract it and create the collections for the edges (edges_otl) and nodes (nodes_otl)
The run the importer with node_7.9!
```
node nodesimport_otl.js
node edgesimport_otl.js
```

4. Now we create 2 subsetted collections containing all parasites (according to interactionTypeName) with:
```
node build_parasites-collection.js
```

# ToDo's

**Currently working on:**
- find out which interactionTypeName determines if a species is free living or parasitic (in documents/interaction_table.md)
- create collection with all free living species (write a builder)
- import the parasite-data from weinstein 2016 (in weinstein_extract.md)

**In the long run:**
- use simple parsimony algorithm to determine how often parasitism occurred in the evolution (of Eukaryota?)

**May?**
- write master thesis as git-book? Create new book and add basic ToC and points what to include

**Future work:**
- draw the graph database with sigma.js(?)
- look at the opentree for phylogeny `https://tree.opentreeoflife.org/opentree/argus/opentree9.1@ott93302`