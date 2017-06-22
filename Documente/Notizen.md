# Algorithmen / Methoden
* Parsimony
* Likelihood / Bayesian

# Programme

* ``Raxml``:
* ``mrbayes``:
* ``beast``:
* ``MacClade``: computer program for phylogenetic analysis ... Its analytical strength is in studies of character evolution. ...
    ```
    http://macclade.org/macclade.html
    ```
    (Paper: Compositional bias, character-state bias and character-state reconstruction using parsimony)
    compositional bias: the occurence of the properties in unequal proportions

# Algorithms for calculating node properties:

# Studied papers

* Independent origins of parasitism in Animalia (Sara B. Weinstein and Armand M. Kuris)
    * "Parasitism has evolved at least 223 times in Animalia."
* Global biotic interactions: An open infrastructure to share and analyze sepcies-interaction datasets (Jorrit H. Poelen, James D. Simons, Chris J. Mungall)
    * Global Biotic Interactions (GloBI): an extesible, open-source infrastructure that was tailored for importing, searching, and exporting species ineraction data.
    * implemented in Java Gosling (2000) and uses (Neo4j) as a persistent data store and query system.
    * Using interaction terms from the OBO Relations Ontology (Smith et al., 2005)
        * specific biotic or abiotic term (taxon of appropriate rank e.g. Homo sapiens, Elasmobranchii)
        * functional group (e.g. algae, plankton)
        * enviroment (e.g. rocks, sediment)
    * existing ontologies: EnvO, Uberon, OBO Relations Ontology (RO), habitat classification vocabulaies
    * GloBI's data collection is also available as an RDF triple dump, which can be queried via SPARQL endpoint.
    * 700,000 interactions, across 50,000 taxa, over 1100 studies, from 19 data sources
* Tangled trees - Phylogeny, Cospeciation, and Coevolution (Book by Roderic D. M. Page)
    * Def.: Cospeciation is the joint speciation of two or more lineages that are ecologically associated, the paradigm example being a host and its parasite.
    * Def.: It is important to distinguish between cospeciation and coevolution. If we define coevolution as the evolution of reciprocal adaptations (gegenseitige Anpassung) in hosts and parasites, then it is clear that lineages can coevolve without cospeciating.
    * Possible processes may occur: cospeciation, host swich, independent speciation, extinction, "missing the boat" and failure to speciate (Figure 1.1)
    * The use of phylogenies in studeies of cospeciation rests on the notion that congruent phylogenies implies cospeciation, whereas incongruence implies host switching.
    * Chapter: Parsimony analysis of coevolving species associations
    * Chapter: A statistical perspective for recontruction the history of host-parasite associations.
* Choosing the best ancestral character state reconstruction method ( Manuela Royer-Carenzi, Pierre Pontarotti, Gilles Didier - 2012)
    * Given:
        * whole phylogenic history -> tree
        * character states (binary) of contemporary organisms -> leaves (tips of the tree)
    * two major classes
        * parsimonious
            * based on predefined parameters (generalized parsimony)
            * ot strong & controversial assumptions (like irreversibility -> Dollo parsimony)
        * Markov model + likelihood
            * allow to take into account divergence times (branch lenght)
            * natural answers to the same question for stochastic methods
        * p vs l: [26, 19, 22, 21, 8]
* Synthesis of phylogeny and taxonomy into a comprehensive tree of life (Cody E. Hinchliff, ..., and Karen A. Cranson)
    * reconstruction the tree of life
    * ~ 1.8 million named species
    * Most recognized species have never been included in a phylogenetic analysis because no appropriate molecular or morphological data have been collected
    * first comprehensive tree of life through the integration of published phylogenies with taxonomic information
    * Open Tree Taxonomy (OTT) is open, extensible and updatable, and reflects the overall phylogeny of life
    * 2.3 million operational taxonomic units (OTUs) from the reference taxonomy
    * Taxonomies contribute to the structure only where we do not have phylogenetic trees.
    * tree alignment graph (graph of life)
        * 2,339,460 leaf nodes
        * 229,801 internal nodes
    * The tree preserves conflict among phylogenies and between phylogenies an the taxonomy.
