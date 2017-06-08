'use strict';

const http = require('request-easy').http;
const req  = new http({hostname:'api.globalbioticinteractions.org'});

const input = encodeURIComponent('eimeria'); //Input every species from taxdb NCBI
const interaction = 'parasiteOf';

const limit = 1000;
//const printThreshold = 10;

const tree = { _species: {} };





//method get from object req. Input is a object parameter and 3 variables. And the "value" of an annonymous function.
req.get({path: `/interaction?type=json.v2&interactionType=${interaction}&limit=${limit}&offset=0&sourceTaxon=${input}&field=target_taxon_path&field=target_taxon_external_id&field=target_taxon_path_ranks`}, (status, headers, body)=>{
    body = JSON.parse(body);



//api.globalbioticinteractions.org/interaction?type=json.v2&interactionType=parasiteOf&limit=15&offset=0&sourceTaxon=eimeria&field=source_taxon_name&field=source_taxon_external_id&field=target_taxon_name&field=target_taxon_external_id&field=interaction_type&field=number_of_interactions



    for (const interactionResult of body) {
        try {
            if ('|' === interactionResult.target_taxon_path_ranks.slice(-1)) interactionResult.target_taxon_path_ranks += ' ';
            if ('|' === interactionResult.target_taxon_path.slice(-1)) interactionResult.target_taxon_path += ' ';

            if ('|' === interactionResult.target_taxon_path_ranks[0]) interactionResult.target_taxon_path_ranks = ' ' + interactionResult.target_taxon_path_ranks;
            if ('|' === interactionResult.target_taxon_path[0]) interactionResult.target_taxon_path = ' ' + interactionResult.target_taxon_path;

            interactionResult.key = interactionResult.target_taxon_path_ranks.split(' | ');
            interactionResult.val = interactionResult.target_taxon_path.split(' | ');

            // console.log(interactionResult.key, '#', interactionResult.val);
            // console.log(interactionResult.target_taxon_path_ranks, '#', interactionResult.target_taxon_path);
            
        } catch(e) {
            console.log('Rank does not match value for:');
            console.log(interactionResult);
            continue;
        }

        insertIntoTree(tree, interactionResult);
        calcSums(tree);
    }

// 'superkingdom |  |  | family | genus | species |  | '
    
    console.log(JSON.stringify(tree, false, 6));

});


function calcSums(node) {

    node.sum = 0;
    for(const key in node) {
        if (key === 'sum') continue;
        if ('number' === typeof node[key]) {
            node.sum += node[key];
        } else {
            node.sum += calcSums(node[key]);
        }
    }
    return node.sum;
}

function insertIntoTree(tree, speci) {

    if (speci.key.length === 0) {
        console.log('No rank definition for:');
        console.log(speci);
        return;
    } // if

    if ('species' === speci.key[0].toLowerCase() ) {

        let val;
        try {
            val = speci.val.shift().toLowerCase();
        } catch(e) { val = 'unknown'; }

        const genusIdx  = speci.target_taxon_path_ranks.split(' | ').indexOf('genus');
        const genusName = speci.target_taxon_path.split(' | ')[genusIdx];
        
        if (undefined === tree[genusName]) tree[genusName] = {};

        if (undefined === tree[genusName][val]) {
            tree[genusName][val] = 0;
        } // if
        
        tree[genusName][val]++; // .push(speci);

        return;
    } // if

    const key = speci.key.shift();
    speci.val.shift();

    if (!tree[key]) {
        tree[key] = { };
    }

    insertIntoTree(tree[key], speci);
}