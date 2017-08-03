'use strict';

const fastango3 = require('fastango3');
const db = fastango3('http://127.0.0.1:8529');

const convert = () => {
    const db = require('@arangodb').db;

    const childsToProcess = ['nodes_otl/304358'];

    while (childsToProcess.length) {

        const parent = db._document(childsToProcess.shift());

        const childs = db._query(`FOR v IN OUTBOUND '${parent._id}' edges_otl RETURN v`).toArray();

        for (const child of childs) {
            const upDoc = {};
            if (child.originw == 1 || parent.parasitew == 1 && child.lossw == null) upDoc.parasitew = 1;
            else if (child.lossw == 1 || parent.freelivingw == 1) upDoc.freelivingw = 1;

            db._update(child._id, upDoc);
            childsToProcess.push(child._id);
        }
    }

    return 'done'; // res[0];
};

db._txn({
    collections: {
        read:['nodes_otl'],
        write:['nodes_otl'],
    }}, convert, (status, headers, body) => {
        // console.log(status);
        body = JSON.parse(body);
        console.log(body);
        console.log("Finished tagging weinstein parasites/freeliving on full tree");
    });