'use strict';
 
const db = require('arangojs')();

db.query(`for doc in interaction_tsv
        filter doc.parasite == 1 && doc.directionF == 'target'
        return doc`, {}, { ttl: 1000 * 3600 }).then(testAvailable); //filter for interaction; ie isparasyte

function testAvailable(cursor) {
    if (!cursor.hasNext()) { console.log('Finished building parasite(target)'); return };

    cursor.next().then(doc => {
        try {
            const ottId = doc.targetTaxonIds.match(/OTT\:(\d+)/)[1];
            writeNewRankPath(ottId, doc);
        } catch (e) { } //here goes code to handle entries without OTTID
        testAvailable(cursor);
    });
}

function writeNewRankPath(ott, dok) {   // Eukaryota_ott304358
    db.query(`
        UPDATE '${ott}' WITH {
            parasite: 1,
            interactionTypeNameP: '${dok.interactionTypeName}',
            directionFL: 'target'
        } IN nodes_otl
    `);
}
return;