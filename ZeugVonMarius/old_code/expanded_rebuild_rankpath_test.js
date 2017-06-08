'use strict';

const db = require('arangojs')();
db.query(`for doc in interaction_tsv return doc`, {}, { ttl: 1000 * 3600 }).then(testAvailable);

function testAvailable(cursor) {

    if (!cursor.hasNext()) { console.log('Finished'); return };

    cursor.next().then(currentDoc => {
        if (!currentDoc.sourceTaxonPathRankNames || !currentDoc.sourceTaxonPathNames) {
            let failedSpecies = currentDoc.sourceTaxonName.split(' ').slice(0, 2).join(' ').replace(/[^A-z0-9\ ]/g, '');
            console.log(failedSpecies);
            if (failedSpecies.indexOf(' ') !== -1) {
                db.query(`for doc in names filter contains(doc.name, '${failedSpecies}') return doc._id`, {}, { ttl: 1 * 3600 }).then(getFailedID);
            } else {
                db.query(`for doc in names filter doc.name == '${failedSpecies}' return doc._id`, {}, { ttl: 1 * 3600 }).then(getFailedID);
            }
        }
        testAvailable(cursor);
    });
}

function getFailedID(cursor) {
    if (!cursor.hasNext()) { console.log('Finished getFailedID'); return };
    cursor.next().then(failedID => {
        db.query(`FOR node, edge IN OUTBOUND SHORTEST_PATH "names/1" TO '${failedID}' GRAPH "ncbi" RETURN [node.name, edge.rank]`, {}, { ttl: 1 * 3600 }).then(getRankPath);
    });
}

function getRankPath(cursor) {
    if (!cursor.hasNext()) { console.log('Finished getRankPath'); return };
    cursor.next().then(rankPath => {
        console.log(typeof(RankPath), rankPath, Object.keys(rankPath));
    });
}




return;