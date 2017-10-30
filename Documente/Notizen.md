# Timetable
1.10. Anmeldung, d.h. 31.3. Abgabe
* Oktober: Woche
    1. build random binary tree, tag tree
    2. forget inner nodes, run parsimony
    3. implement parsimony with numbers
    4. prune binary tree -> not binary tree
* November: Woche
    * 5. run parsimony with numbers and TMC
    * 6. -8. Evaluation -> compare computed trees with the origin binary tree
* Dezember: Evaluation of special subtrees of the real synthesis tree from Open Tree of Life 	(using biological knowlege)
* Jannuar: theoretical analysis of the two parsimony like algorithms -> add changes, adjust 	the parameters
* Februar: last Evaluation / Compairing the different algorithms
* März: Proofreading, writing, complete the thesis

# Data
* Open Tree of Life
    * Open Tree of Life aims to construct a comprehensive, dynamic and digitally-available tree of life by synthesizing published phylogenetic trees along with taxonomic data. The project is a collaborative effort between 11 PIs across 10 institutions. Funding is from NSF AVAToL #1208809.
    * Cite the Open Tree of Life: Hinchliff, Cody E., et al. "Synthesis of phylogeny and taxonomy into a comprehensive tree of life." Proceedings of the National Academy of Sciences 112.41 (2015): 12764-12769. + https://doi.org/10.1073/pnas.1423041112

# How to Collapse and Resolve Multichotomies
* "Resolve the multichotomies randomly (the default) or in the order they appear in the tree."

    ```
    https://rdrr.io/cran/ape/man/multi2di.html
    ```

# Algorithmen / Methoden für ``ancestral-state reconstruction`` (ASR)
* maximum parsimony (MP)
* maximum likelihood (ML) / Bayesian
* stochastic mapping (SM)

# Programme

* ``Raxml``: (Randomized Axelerated Maximum Likelihood)
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
* Mapping Mutations on Phylogenies (Rasmus Nielsen - 2002)
    * The common approaches for mapping mutations based on parsimony have lacked a solid statistical foundation. He presents a Bayesian method for mapping mutations on a phylogeny.
* Testing for independence between evolutionary processes (Abdelkader Behdenna, Joel Pothier, Sophie S Abby, Amaury Lambert, Guillaume Achaz - 2016)
    * "Evolutionary events co-occurring along phylogenetic trees usually point to complex adaptive phenomena, sometimes implicating epistasis. While a number of methods have been developed to account for co-occurence of events on the same internal or external branch of an evolutionary tree, there is a need to account for the larger diversity of possible relative positions of events in a tree. Here we propose a method to quantify to what extent two or more evolutionary events are associated on a phylogenetic tree."
* Simple Reconstruction of Binary Near-Perfect Phylogenetic Trees (Srinath Sridhar, Kedar Dhamdhere, Guy E. Blelloch, Eran Halperin, R. Ravi and Russell Schwartz - 2006)
    * Emanuel:
    tree reconstruction. Also das erstellen eines Baumes.
    Ist interessant, da es (vorher, falls das wirklich funktioniert) keine nicht-heuristischen Algorithmen hab die bei Datensätze von relevanter Größe funktionieren.


* http://www.phytools.org/eqg/Exercise_5.2/
    * 5 topics
        * 1. Estimating the ancestral states of continuous characters.
        * 2. Visualizing continuous character ancestral states for one or multiple traits.
        * 3. Estimating ancestral character states for discrete characters under a continuous-time Markov chain.
        * 4. Simulating stochastic character histories for a discrete character (stochastic character mapping).
        * 5. Simultaneously plotting discrete & continuous character reconstructions.

# Vorgeschlagene Paper
Relevant?!:
* Effects of Phylogenetic Signal on Ancestral State Reconstruction - GLENN LITSIOS AND NICOLAS SALAMIN
    Emanuel:
    We then reconstructed the characters on the phylograms and chronograms using a widely used ML algorithm (Pagel 1994) implemented in geiger (Harmon et al. 2008) 
    ... aus dem paper. Vorher haben sie Bäume simuliert und kontinuierliche character darauf evolvieren lassen. Diese Charter änder  sich mehr oder weniger stark mit simulirter Zeit oder DNA korreliert.
    Dann analysieren sie wie gut die Algorithmen noch funktionieren. Da diese die Zeit mit betrachten. Bzw wie gut sie funktionieren wenn man die DNA Distanz statt der Zeit verwendet.
    Der auf das Zitat oben folgende Abschnitt gibt dann noch drei andere Distanz Maße an, zusätzlich zu der einfachen Distanz auf die wir schon selbst gekommen sind. Und zitiert die Quellen dafür:
    For each simulated data set, we summed over the differences between the inferred and the true ancestral states at each node to obtain one value per tree. This gave a relative measure of the error in the character state reconstructed, with higher values meaning larger differences between the inferred and the true values. We also measured the tree imbalance using the Colless index (Colless 1995), the size of the clade originating on Branch B, and the phylogenetic signal using both the K (Blomberg et al. 2003) and λ (Pagel 1999) indices.
    Übrigens: es gibt auch eine Datenbank für Divergenz Zeiten. Die könnten wir falls wir das brauchen auch noch auf unseren baum packen.
    Danach kommen dann sogar noch Primaten für dich in dem Paper vor. Das perfekte Paper für @irallia :monkey:
* Diversity and evolution of ectomycorrhizal host associations in the Sclerodermatineae (Boletales, Basidiomycota) - Andrew W. Wilson, Manfred Binder and David S. Hibbett
    Emanuel:
    Diversity and evolution of ectomycorrhizal host associations in the Sclerodermatineae
    "Binary state coding defined host states as either angiosperms or gymnosperms."
    "Multi-state coding defined host states by host family association. The host families for analyses include: Betulaceae, Cistaceae, Dipterocarpaceae, Ericaceae, Fagaceae, Fabaceae (Mimosoideae and ‘Caesalpinioideae’), Myrtaceae, Nyctaginaceae, Pinaceae, Oleaceae, Polygonaceae, Salicaceae, and Sapindaceae (Notes S2)"
    "Maximum likelihood ASR analysis was implemented in BayesTraits (Pagel et al., 2004). Using the 112-taxon supermatrix data set,"
    D.h. sie haben gleichzeitig auch die phylogenetischen anhand einer DNA supermatrix (= mehrere gene) abgeschätzt.
    Deshalb "Maximum likelihood binary and multi-state analyses were performed on 100 posterior sampled phylogenies produced from Bayesian analyses"
    Nach den Divergenz Zeiten rekonstruieren die dann sogar noch die ancestral ranges vor den ancestal Hosts.
    Das zweite Paper hab ich nicht ganz gelesen.   Ist aber definitiv relevant!

* A Quick Guide to Organizing Computational Biology Projects: http://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1000424
    Emanuel for future work:
    (In a more distant future something like this out of the shit we are sequencing will link @irallia and @victor_h_jarquin work.)
* Inferring species interactions from co-occurrence data with Markov networks
    * "Inferring species interactions from co-occurrence data ... One difficulty is that a single pairwise interaction can ripple through an ecological network and produce surprising indirect consequences. For example, the negative correlation between two competing species can be reversed in the presence of a third species that is capable of outcompeting both of them. Here, I apply models from statistical physics, called Markov networks or Markov random fields, that can predict the direct and indirect consequences of any possible species interaction matrix. Interactions in these models can also be estimated from observed co-occurrence rates via maximum likelihood, controlling for indirect effects."
* Ecological interactions and the Netflix problem
    * Ein etwas anderer Ansatz:
    * "Species interactions are a key component of ecosystems but we generally have an incomplete picture of who-eats-who in a given community. ... Here, we explore the K nearest neighbour approach, with a special emphasis on recommendation, along with a supervised machine learning technique. ... By removing a prey from a predator, we find that recommenders can guess the missing prey around 50% of the times on the first try, with up to 881 possibilities. Traits do not improve significantly the results for the K nearest neighbour, although a simple test with a supervised learning approach (random forests) show we can predict interactions with high accuracy using only three traits per species. This result shows that binary interactions can be predicted without regard to the ecological community given only three variables: body mass and two variables for the species’ phylogeny."

* Emanuel for MA:
    * Eher Aufbau als Inhalt: Algorithmus, Anwendung, Detail-Beispiel aus der Anwendung
    Clusterflock: a flocking algorithm for isolating congruent phylogenomic datasets
    Apurva Narechania  Richard Baker  Rob DeSalle  Barun Mathema Sergios-Orestis Kolokotronis  Barry Kreiswirth  Paul J. Planet
    GigaScience, Volume 5, Issue 1, 1 December 2016, Pages 1–12, https://doi.org/10.1186/s13742-016-0152-3
    Published: 24 October 2016
    https://academic.oup.com/gigascience/article/5/1/1/2737427/Clusterflock-a-flocking-algorithm-for-isolating?searchresult=1
    * Clusterflock: ein Algorithmus für Schwarmverhalten zur Isolierung kongruenter phylogenomischer Datensätze
    * Ergebnisse:
        * In dem hier vorgestellten Tool Clusterflock haben wir einen Algorithmus für Schwarmverhalten implementiert, der dazu dient, Gruppen (Herden) orthologer Genfamilien (OGFs) zu lokalisieren, die eine evolutionäre Geschichte teilen.
        * Paarweise Abstände, die die phylogenetische Inkongruenz zwischen OGFs messen, führen zur Bildung von Flocken/Schwärmen. Wir haben diesen Ansatz auf mehreren simulierten Datensätze getestet, indem wir die Anzahl zugrunde liegender Topologien, den Anteil fehlender Daten und Evolutionsraten variierten und zeigen, dass Clusterflock in Datensätzen, die hohe Werte an fehlenden Daten und Ratenheterogenität enthalten, andere bewährte Clustering-Techniken übertrifft. [...]
    * Schlussfolgerungen: Clusterflock ist ein Open-Source-Tool, mit dem horizontal transferierte Gene, rekombinierte Chromosomenbereiche und der phylogenetische Kern eines Genoms entdeckt werden können. Obwohl wir es hier im evolutionären Kontext verwendet haben, ist es für jedes Clusterproblem verallgemeinerbar. Benutzer können Erweiterungen schreiben, um eine Entfernungsmetrik im Einheitsintervall zu berechnen, und können diese Abstände verwenden, um jegliche Art von Daten zu "schwärmen".


    Emanuel for Parnika:
    (Here are my first reading suggestions for @parnika. Checking these out will give other PhD students @alice @totta @victor_h_jarquin @enas.alkhlifeh an impression what Parnika will do.
    @irallia and @parnika (will) do basically the same thing. Proteins or species doesn't matter.)
* Rapid identification of genes controlling virulence and immunity in malaria parasites
    * "Here we present a rapid genome-wide approach capable of identifying multiple genetic drivers of medically relevant phenotypes within malaria parasites via a single experiment at single gene or allele resolution." ...  "Here we use a novel approach to study two important properties of the parasite; the rate at which parasites grow within a single host, and the means by which parasites are affected by the host immune system."
* Functional Profiling of a Plasmodium Genome Reveals an Abundance of Essential Genes
    * "The genomes of malaria parasites contain many genes of unknown function. To assist drug development through the identification of essential genes and pathways, we have measured competitive growth rates in mice of 2,578 barcoded Plasmodium berghei knockout mutants, representing >50% of the genome, and created a phenotype database."
* Genes involved in host–parasite interactions can be revealed by their correlated expression
    * "Correlated gene expression profiles can be used to identify molecular interactions within a species. Here we have extended the concept to different species, showing that genes with correlated expression are more likely to encode proteins, which directly or indirectly participate in host–parasite interaction."
*   Computational approaches for prediction of pathogen-host protein-protein interactions
    * "Molecular interactions between pathogens and their hosts are the key parts of the infection mechanisms." ... "The computational methods primarily utilize sequence information, protein structure and known interactions. Classic machine learning techniques are used when there are sufficient known interactions to be used as training data. On the opposite case, transfer and multitask learning methods are preferred. Here, we present an overview of these computational approaches for predicting PHI systems, discussing their weakness and abilities, with future directions."


Ecological interactions and the Netflix problem