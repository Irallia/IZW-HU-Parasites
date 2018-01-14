# Timetable

|Woche|       |                             |done?|weiteres:
|-----|-------|-----------------------------|-----|---------
|Oktober
|1    | 2.- 6.|build random tree + tag it   | x | 
|2    | 9.-13.|implement wagner-parsimony   | x |
|3    |16.-20.|parsimony + Zahlen           | x | change distribution for random trees to beta-dist
|4    |23.-27.|binary -> not binary         | x | parasite examples searched, first introduction written
|November
|5    |30.- 3.|not binary with changing distribution| x | Book: Inferring Phylogenies - Joseph Felsenstein
|6    | 6.-10.|Metadata collection from big phylogenetic tree | x | and Subtrees
|7    |13.-17.|wagner vs fitch vs others??  | x | rglobi, rotl, castor (R packages) -> Sankoff max parsimony
|8    |20.-24.|implement these for not binary| x | (fitch parsimony + parsimony like + Sankoff from castor); Get Interaction Data with rglobi (R package)
|Dezember
|9    |27.- 1.|count origins, compare trees|   |
|10   | 4.- 8.|add empty leaf nodes | x |
|11   |11.-15.|gat some data for evaluation| x | Distanzen zwischen Bäumen, Prozentuale Differenzen
|12   |18.-22.|runtime evaluation, fix algorithms to make them faster | x | 
|13   |25.-29.| ... Chrismas break ... | x |
|Jannuar
|?    | 1.- 7.| ... Chrismas break ... | x |
|?    | 8.-14.|simulation evaluation of different parasite distributions and a different amount of unknown data | x |
|Februar
|März

# ToDos:
* Work with rotl (R package) - rotl: an R package to interact with the Open Tree of Life data
* Origins Zählen
* Distanzen zwischen Bäumen
    * Anzahl Origins
* Daten Sammeln
    * von ges Baum und Subbäumen
    * über:
        * #P, #FL, #untagged
* Parameter für beta-Verteilung -> stability analysis

# Questions:
    * get_synthesis_tree.py : Interne Knoten ignorieren? Ebenfalls taggen? Namen ganz entfernen? Kann man den Originalbaum dann noch rekonstruieren?