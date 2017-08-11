'use strict';
 
const db = require('arangojs')();

db.query(`for doc in interaction_tsv
        filter doc.parasite == 1 && doc.directionF == 'source'
        return doc`, {}, { ttl: 1000 * 3600 }).then(testAvailable); //filter for interaction; ie isparasyte

function testAvailable(cursor) {
    if (!cursor.hasNext()) { console.log('Finished building parasites(source)'); return };

    cursor.next().then(doc => {
        try {
            const ottId = doc.sourceTaxonIds.match(/OTT\:(\d+)/)[1];
            writeNewRankPath(ottId, doc);
        } catch (e) { } //here goes code to handle entries without OTTID
        testAvailable(cursor);
    });
}

function writeNewRankPath(ott, dok) {
    db.query(`for doc in (FOR v,e IN OUTBOUND SHORTEST_PATH 'nodes_otl/304358' TO 'nodes_otl/${ott}' edges_otl return v)
    FILTER doc
    UPDATE doc WITH {
        parasite: doc._key == '${ott}' ? 1 : 0,
        globi: doc._key == '${ott}' ? 1 : 0,
        interactionTypeNameP: doc._key == '${ott}' ? '${dok.interactionTypeName}' : 'null',
        directionP: 'source' } IN nodes_otl`);
}
return; 