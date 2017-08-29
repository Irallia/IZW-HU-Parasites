'use strict';
const db = require('arangojs')();

//tag parasites source

db.query(`FOR doc IN interaction_tsv
          FILTER doc.interactionTypeName == "parasiteOf" ||
          doc.interactionTypeName == "ectoParasiteOf" ||
          doc.interactionTypeName == "kleptoparasiteOf" ||
          doc.interactionTypeName == "ectoParasitoid" ||
          doc.interactionTypeName == "endoparasiteOf" ||
          doc.interactionTypeName == "parasitoidOf" ||
          doc.interactionTypeName == "endoparasitoidOf" ||
          doc.interactionTypeName == "pathogenOf"
          UPDATE doc WITH { parasite: 1,
                            directionP: "source",
                            pname: doc.sourceTaxonName } IN interaction_tsv`)

//tag parasites target

db.query(`  FOR doc IN interaction_tsv
            FILTER doc.interactionTypeName == "hasParasite" ||
            doc.interactionTypeName == "hasPathogen"
            UPDATE doc WITH {   parasite: 1,
                                directionP: "target",
                                pname: doc.targetTaxonName } IN interaction_tsv`)

//tag freeliving source

db.query(`  FOR doc IN interaction_tsv
            FILTER doc.interactionTypeName == "visits" ||
            doc.interactionTypeName == "preysOn" ||
            doc.interactionTypeName == "eats" ||
            doc.interactionTypeName == "flowersVisitedBy" ||
            doc.interactionTypeName == "hasPathogen" ||
            doc.interactionTypeName == "pollinatedBy" ||
            doc.interactionTypeName == "hasParasite" ||
            doc.interactionTypeName == "hostOf"
            UPDATE doc WITH {   freeliving: 1,
                                directionF: "source",
                                fname: doc.sourceTaxonName } IN interaction_tsv`)

//tag freeliving target

db.query(`  FOR doc IN interaction_tsv
            FILTER doc.interactionTypeName == "preyedUponBy" ||
            doc.interactionTypeName == "ectoParasitoid" ||
            doc.interactionTypeName == "parasiteOf" ||
            doc.interactionTypeName == "ectoParasiteOf" ||
            doc.interactionTypeName == "kleptoparasiteOf" ||
            doc.interactionTypeName == "visitsFlowersOf" ||
            doc.interactionTypeName == "endoparasitoidOf" ||
            doc.interactionTypeName == "parasitoidOf" ||
            doc.interactionTypeName == "endoparasiteOf" ||
            doc.interactionTypeName == "pathogenOf" ||
            doc.interactionTypeName == "hasHost"
            UPDATE doc WITH {   freeliving: 1,
                                directionF: "target",
                                fname: doc.targetTaxonName } IN interaction_tsv`)