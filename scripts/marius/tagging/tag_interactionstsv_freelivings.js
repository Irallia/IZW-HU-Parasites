'use strict';
const db = require('arangojs')();

//tag freeliving source

db.query(`for doc in interaction_tsv
          filter doc.interactionTypeName == "visits" ||
          doc.interactionTypeName == "preysOn" ||
          doc.interactionTypeName == "eats" ||
          doc.interactionTypeName == "flowersVisitedBy" ||
          doc.interactionTypeName == "hasPathogen" ||
          doc.interactionTypeName == "pollinatedBy" ||
          doc.interactionTypeName == "hasParasite"
          return doc`, {}, { ttl: 1000 * 3600 }).then(tagFreelivingS); //filter for interaction; ie isparasyte

function tagFreelivingS(cursor) {
    if (!cursor.hasNext()) { console.log('Finished tagging freeliving(source)'); return };
    cursor.next().then(async doc => {
        try {await db.query(`UPDATE "${doc._key}" WITH { freeliving: 1,
                                                   directionF: "source",
                                                   fname: @sourceTaxonName } IN interaction_tsv`, {sourceTaxonName:doc.sourceTaxonName});
        } catch (e) { }
        tagFreelivingS(cursor);
    });
}
