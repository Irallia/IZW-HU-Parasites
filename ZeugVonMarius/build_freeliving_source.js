'use strict';

const db = require('arangojs')();
const collection = db.collection('otl_parasites_nodes');

db.query(`for doc in interaction_tsv
          filter doc.interactionTypeName == 'visits' ||
          doc.interactionTypeName == 'preysOn' ||
          doc.interactionTypeName == 'eats' ||
          doc.interactionTypeName == 'flowersVisitedBy' ||
          doc.interactionTypeName == 'hasPathogen' ||
          doc.interactionTypeName == 'pollinatedBy' ||
          doc.interactionTypeName == 'hasParasite'
          return doc`, {}, { ttl: 1000 * 3600 }).then(testAvailable); //filter for interaction; ie isparasyte

function testAvailable(cursor) {
    if (!cursor.hasNext()) { console.log('Finished / reached last entry'); return };

    cursor.next().then(doc => {
        try {
            const ottId = doc.sourceTaxonIds.match(/OTT\:(\d+)/)[1];
            writeNewRankPath(ottId);
        } catch (e) { } //here goes code to handle entries without OTTID
        testAvailable(cursor);
    });
}

function writeNewRankPath(ott) {
    console.log('writing' + ott);
    db.query(`for doc in (FOR v,e IN OUTBOUND SHORTEST_PATH 'nodes_otl/304358' TO 'nodes_otl/${ott}' GRAPH 'otl' return e)
    filter doc
    insert merge(doc, {_id:concat('otl_parasites_edges/', doc._key),
                    _from:concat('otl_parasites_nodes/', SPLIT(doc._from, '/')[1] ),
                    _to:concat('otl_parasites_nodes/',   SPLIT(doc._to,   '/')[1] )
            }) in otl_parasites_edges OPTIONS { ignoreErrors: true }`);
    db.query(`for doc in (FOR v,e IN OUTBOUND SHORTEST_PATH 'nodes_otl/304358' TO 'nodes_otl/${ott}' GRAPH 'otl' return v)
    filter doc
    insert merge(doc, {_id:concat('otl_parasites_nodes/', doc._key),
                        freeliving: doc._key == '${ott}' ? 1 : 0 }) in otl_parasites_nodes OPTIONS { ignoreErrors: true }`); //if doc.key == searched OTTID update state to parasite
}
return;