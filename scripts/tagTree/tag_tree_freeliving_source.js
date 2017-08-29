'use strict';
 
const db = require('arangojs')();

db.query(`for doc in interaction_tsv
        filter doc.freeliving == 1 && doc.directionF == 'source'
        return doc`, {}, { ttl: 1000 * 3600 }).then(testAvailable); //filter for interaction; ie isparasyte
 
function testAvailable(cursor) {
    if (!cursor.hasNext()) { console.log('Finished building freeliving(source)'); return };

    cursor.next().then(doc => {
        try {
            const ottId = doc.sourceTaxonIds.match(/OTT\:(\d+)/)[1];
            writeNewRankPath(ottId, doc);
        } catch (e) { } //here goes code to handle entries without OTTID
        testAvailable(cursor);
    });
}

function writeNewRankPath(ott, dok) {   // Eukaryota_ott304358
    db.query(`
        UPDATE '${ott}' WITH {
            freeliving: 1,
            interactionTypeNameFL: '${dok.interactionTypeName}',
            directionFL: 'source'
        } IN nodes_otl
    `);
}
return;