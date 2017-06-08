# How to generate the number of parasites in GLoBIs databse

## List of used parasitic interactions:
- parasiteOf
- ectoParasiteOf
- kleptoparasiteOf
- ectoParasitoid


## Example AQL queries

### Return count of eucaryotic parasites 
```
return count(
FOR v,e IN 1..100 outbound 'otl_parasites_nodes/304358' otl_parasites_edges
  FILTER v.parasite == 1
RETURN v)
```
Note that the OTT-ID 304358 represents the Eukaryota-node.

# Table

Note that this table should get visualized in a better way later on (tree with number).


taxonomic group | count of parasites
---|---
Eukaryota | 11.030
- Fungi | 2.385
- Metazoa | 8.207
- Archaeplastida | 126
- Chloroplastida | 125