'use strict';
const db = require('arangojs')();

//tag parasites source

db.query(`for doc in interaction_tsv
          filter doc.interactionTypeName == "hasParasite" ||
          doc.interactionTypeName == "hasPathogen"
          return doc`, {}, { ttl: 1000 * 3600 }).then(tagParasT); //filter for interaction; ie isparasyte

function tagParasT(cursor) {
    if (!cursor.hasNext()) { console.log('Finished tagging parasites(target)'); return };
    cursor.next().then(async doc => {
        try {await db.query(`UPDATE "${doc._key}" WITH { parasite: 1,
                                                   directionP: "target",
                                                   pname: @targetTaxonName } IN interaction_tsv`, {targetTaxonName:doc.targetTaxonName});
        } catch (e) { }
        tagParasT(cursor);
    });
}