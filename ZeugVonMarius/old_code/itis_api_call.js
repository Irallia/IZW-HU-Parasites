'use strict';

const https = require('request-easy').https;
const req = new https({ hostname: 'www.itis.gov' });
const fastango = require('fastango3')('http://127.0.0.1:8529');
const db = require("@arangodb").db;


let counter = 0;
//let input_species = encodeURIComponent('homo sapiens');
const it = db._query('for doc in interaction_tsv return distinct doc.sourceTaxonName');

while (it.hasNext()) {
    const doc = db.interaction_tsv.document(it.next());
    let input_species = doc.sourceTaxonName


    req.get({ path: `/ITISWebService/jsonservice/searchForAnyMatch?srchKey=${input_species}` }, (status, headers, body) => {
        body = JSON.parse(body);
        try {
            if (body.anyMatchList[0].tsn == null) console.log('fail')
            counter++;
        }
        catch (e) { console.log('no entry for this shit') }
        console.log(counter);
    })
}




// fastango._txn({ collections: { read: ['interaction_tsv'], write: ['species_tsn'] } }, convert, (status, headers, body) => {
//     console.log(status);
//     console.log(body.toString());
// });


