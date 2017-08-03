'use strict';
const db = require('arangojs')();

//tag freeliving target

db.query(`for doc in interaction_tsv
          filter doc.interactionTypeName == "preyedUponBy" ||
          doc.interactionTypeName == "ectoParasitoid" ||
          doc.interactionTypeName == "parasiteOf" ||
          doc.interactionTypeName == "ectoParasiteOf" ||
          doc.interactionTypeName == "kleptoparasiteOf" ||
          doc.interactionTypeName == "visitsFlowersOf" ||
          doc.interactionTypeName == "endoparasitoidOf" ||
          doc.interactionTypeName == "parasitoidOf" ||
          doc.interactionTypeName == "endoparasiteOf" ||
          doc.interactionTypeName == "pathogenOf"
          return doc`, {}, { ttl: 1000 * 3600 }).then(tagFreelivingT); //filter for interaction; ie isparasyte

function tagFreelivingT(cursor) {
    if (!cursor.hasNext()) { console.log('Finished tagging freeliving(target)'); return };
    cursor.next().then(async doc => {
        try {await db.query(`UPDATE "${doc._key}" WITH { freeliving: 1,
                                                   directionF: "target",
                                                   fname: @targetTaxonName } IN interaction_tsv`, {targetTaxonName:doc.targetTaxonName});
        } catch (e) { }
        tagFreelivingT(cursor);
    });
}
