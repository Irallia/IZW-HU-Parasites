'use strict';
const db = require('arangojs')();

//tag the full tree with origins and losses

db.query(`  FOR doc IN nodes_otl_sub
            FILTER doc.origin_to == 1
            return doc`, {}, { ttl: 1000 * 3600 }).then(tagorigins);

function tagorigins(cursor) {
    if (!cursor.hasNext()) { console.log('Finished tagging origins_to'); return };
    cursor.next().then(async doc => {
        try {await db.query(`UPDATE "${doc._key}" WITH { origin: 1 } IN nodes_otl`);
        } catch (e) { }
        tagorigins(cursor);
    });
}

db.query(`  FOR doc IN nodes_otl_sub
            FILTER doc.loss_to == 1
            return doc`, {}, { ttl: 1000 * 3600 }).then(tagloss);

function tagloss(cursor) {
    if (!cursor.hasNext()) { console.log('Finished tagging loss_to'); return };
    cursor.next().then(async doc => {
        try {await db.query(`UPDATE "${doc._key}" WITH { loss: 1 } IN nodes_otl`);
        } catch (e) { }
        tagloss(cursor);
    });
}

db.query(`  FOR doc IN weinstein
            return doc`, {}, { ttl: 1000 * 3600 }).then(tagwein);

function tagwein(cursor) {
    if (!cursor.hasNext()) { console.log('Finished tagging origins weinstein'); return };
    cursor.next().then(async doc => {
        try {await db.query(`UPDATE "${doc._key}" WITH { originw: 1 } IN nodes_otl`);
        } catch (e) { }
        tagwein(cursor);
    });
}

db.query(`  FOR doc IN nodes_otl_sub
            FILTER doc.origin_from == 1
            return doc`, {}, { ttl: 1000 * 3600 }).then(tagoriginfrom);

function tagoriginfrom(cursor) {
    if (!cursor.hasNext()) { console.log('Finished tagging origins from'); return };
    cursor.next().then(async doc => {
        try {await db.query(`UPDATE "${doc._key}" WITH { origin_from: 1 } IN nodes_otl`);
        } catch (e) { }
        tagoriginfrom(cursor);
    });
}

db.query(`  FOR doc IN nodes_otl_sub
            FILTER doc.loss_from == 1
            return doc`, {}, { ttl: 1000 * 3600 }).then(taglossfrom);

function taglossfrom(cursor) {
    if (!cursor.hasNext()) { console.log('Finished tagging losses from'); return };
    cursor.next().then(async doc => {
        try {await db.query(`UPDATE "${doc._key}" WITH { loss_from: 1 } IN nodes_otl`);
        } catch (e) { }
        taglossfrom(cursor);
    });
}
