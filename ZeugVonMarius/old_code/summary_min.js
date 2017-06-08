'use strict';

const http = require('request-easy').http;
const req  = new http({hostname:'api.globalbioticinteractions.org'});

const input = encodeURIComponent('homo sapiens');
const interaction = 'hasPathogen';

const limit = 10;
const printThreshold = 10;

const tree = { _species: {} };

req.get({path: `/interaction?type=json.v2&interactionType=${interaction}&limit=${limit}&offset=0&sourceTaxon=${input}&field=target_taxon_path&field=target_taxon_external_id&field=target_taxon_path_ranks`}, (status, headers, body)=>{
    body = JSON.parse(body);

    for (const interactionResult of body) {        
        try {
            if ('|' === interactionResult.target_taxon_path_ranks.slice(-1))
            interactionResult.target_taxon_path_ranks += ' ';
            interactionResult.key = interactionResult.target_taxon_path_ranks.split(' | ');
            interactionResult.val = interactionResult.target_taxon_path.split(' | ');
        } catch(e) { continue; }
        insertIntoTree(tree, interactionResult);
    }
    
    console.log(JSON.stringify(tree, false, 6));

});

function insertIntoTree(tree, speci) {

    if (speci.key.length === 0) {
        return;
    }

    if ('species' === speci.key[0].toLowerCase() ) {

        let val;
        try {
            val = speci.val.shift().toLowerCase();
        } catch(e) { val = 'unknown'; }

        if (undefined === tree._species[val]) {
            tree._species[val] = 0;
        }
        tree._species[val]++;
        return; //when last speci is reached
    }

    const key = speci.key.shift();
    speci.val.shift();

    if (!tree[key]) {
        tree[key] = { _species:{} };
    }

    insertIntoTree(tree[key], speci);
}