# Markdown table of GLoBIs interaction types and which are relevant for us

### parasitic interaction (source)
Source species of this interaction type are certainly parasites.
### parasitic interaction (target)
Target species of this interation type are cerstainly parasites.
### freeliving interaction (source)
Source species of this interaction type are certainly free living.
### freeliving interaction (target)
Target species of this interaction type are certainly free living.
### in question
These interaction types need further evaluation, if they can be used to determine if a species is parasitic or free living.
### not useful
You cannot determine if the species is free living or parasitic with the help of this interaction type.

# Table of all interactions and their parasitic character
Note that we're assuming that no parasit is getting parasited by other parasitic species.

parasitic interaction (source)|parasitic interaction (target)| freeliving interaction (source) | freeliving interaction (target)|in question|not useful
---|---|---|---|---|---
**ectoParasitoid**|**hasParasite**|**visits**|**preyedUponBy**|**eatenBy**|**livesNear**(131)
**parasiteOf**| |**preysOn**| **ectoParasitoid**|**hasHost**|**interactsWith**
**ectoParasiteOf**||**eats**| **parasiteOf**|**kills**|**inhabits**(15)
**kleptoparasiteOf**||**flowersVisitedBy**|**ectoParasiteOf**|**hostOf**|**pollinates**|
**endoparasiteOf**| |**hasPathogen**|**kleptoparasiteOf**|**hasDispersalVector**|**farms** (1)
**parasitoidOf**| |**pollinatedBy**|**visitsFlowersOf**|**hasVector**|**livesUnder**(113)|
**endoparasitoidOf**(1462)| |**hasParasite**||**symbiontOf** |**livesOn**(1073)|
**ectoParasitoid**(61)| | | |**pathogenOf**| **guestOf**(141)
 | | | |**vectorOf**| **livesInsideOf**(583)
 | | | |**dispersalVectorOf**|**adjacentTo**

## Raw interaction type IDs and their definitions

Interaction | ID | Definition
---|---|---
adjacentTo|http://purl.obolibrary.org/obo/RO_0002220%20 | X adjacent to y if and only if x and y share a boundary
dispersalVectorOf|http://eol.org/schema/terms/DispersalVector%20 | A dispersal vector is an agent transporting seeds or other dispersal units. Dispersal vectors may include biotic factors, such as animals, or abiotic factors, such as the wind or the ocean
eatenBy|http://purl.obolibrary.org/obo/RO_0002471%20 | An interaction relationship in which the partners are related via a feeding relationship.
eats|http://purl.obolibrary.org/obo/RO_0002470%20 | An interaction relationship in which the partners are related via a feeding relationship.
ectoParasiteOf|http://purl.obolibrary.org/obo/RO_0002632%20 | A sub-relation of parasite-of in which the parasite lives on or in the integumental system of the host
ectoParasitoid|no:match |
endoparasiteOf|http://purl.obolibrary.org/obo/RO_0002634%20 | A sub-relation of parasite-of in which the parasite lives inside the host, beneath the integumental system; Types
endoparasitoidOf|no:match |
farms|no:match |
flowersVisitedBy|http://purl.obolibrary.org/obo/RO_0002623%20 | No Def
guestOf|no:match |
hasDispersalVector|http://eol.org/schema/terms/HasDispersalVector%20 | a dispersal vector is "an agent transporting seeds or other dispersal units". Dispersal vectors may include biotic factors, such as animals, or abiotic factors, such as the wind or the ocean
hasHost|http://purl.obolibrary.org/obo/RO_0002454%20 | A biotic interaction in which the two organisms live together in more or less intimate association.
hasParasite|http://purl.obolibrary.org/obo/RO_0002445%20 | An interaction relationship between two organisms living together in more or less intimate association in a relationship in which association is disadvantageous or destructive to one of the organisms (GO).
hasPathogen|http://purl.obolibrary.org/obo/RO_0002557%20 | No Def
hasVector|http://purl.obolibrary.org/obo/RO_0002460%20 | No Def
hostOf|http://purl.obolibrary.org/obo/RO_0002453%20 | The term host is usually used for the larger (macro) of the two members of a symbiosis (GO)
inhabits|no:match |
interactsWith|http://purl.obolibrary.org/obo/RO_0002437%20 | An interaction relationship in which at least one of the partners is an organism and the other is either an organism or an abiotic entity with which the organism interacts
kills|http://purl.obolibrary.org/obo/RO_0002626%20 |
kleptoparasiteOf|http://purl.obolibrary.org/obo/RO_0008503%20 | A sub-relation of parasite of in which a parasite steals resources from another organism, usually food or nest material
livesInsideOf|no:match |
livesNear|no:match |
livesOn|no:match |
livesUnder|no:match |
parasiteOf|http://purl.obolibrary.org/obo/RO_0002444%20 | An interaction relationship between two organisms living together in more or less intimate association in a relationship in which association is disadvantageous or destructive to one of the organisms (GO).
parasitoidOf| http://purl.obolibrary.org/obo/RO_0002208%20 | A parasite that kills or sterilizes its host
pathogenOf|http://purl.obolibrary.org/obo/RO_0002556%20 | No Def
pollinatedBy|http://purl.obolibrary.org/obo/RO_0002456%20 | is target of pollination interaction with; has polinator
pollinates|http://purl.obolibrary.org/obo/RO_0002455%20 | This relation is intended to be used for biotic pollination - e.g. a bee pollinating a flowering plant. Some kinds of pollination may be semibiotic - e.g. wind can have the role of pollinator. We would use a separate relation for this.
preyedUponBy|http://purl.obolibrary.org/obo/RO_0002458%20 | Inverse of preys on
preysOn|http://purl.obolibrary.org/obo/RO_0002439%20| An interaction relationship involving a predation process, where the subject kills the target in order to eat it or to feed to siblings, offspring or group members
symbiontOf|http://purl.obolibrary.org/obo/RO_0002440%20 | A biotic interaction in which the two organisms live together in more or less intimate association
vectorOf|http://purl.obolibrary.org/obo/RO_0002459%20 | a is a vector for b if a carries and transmits an infectious pathogen b into another living organism
visitsFlowersOf|http://purl.obolibrary.org/obo/RO_0002622%20 | No Def
visits|http://purl.obolibrary.org/obo/RO_0002618%20 | No Def