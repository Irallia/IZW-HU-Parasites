'use strict';

//const fastango = require('fastango3')('http://127.0.0.1:8529');

const arangojs = require('arangojs');
const http = require('request-easy').http;
const req = new http({ hostname: 'api.globalbioticinteractions.org' });

const db = arangojs();

db.query(

`for doc in 1..50
outbound 'names/131567' nodes options {uniqueVertices:'global', bfs:true}
filter doc.rank == 'species'
return doc`, {}, { ttl: 1000 * 3600 })
    .then(testIfSpeciesIsParasyte);



   /* `for doc in names
filter doc.rank=='species'
return doc`, {}, { ttl: 1000 * 3600 })
    .then(testIfSpeciesIsParasyte);
*/



const limit = 3;

let parasiteCount = 0;
let anyInteractionCount = 0;
let noHit = 0;

function testIfSpeciesIsParasyte(cursor) {
    if (!cursor.hasNext()) {                      //reached last species; if cursor has no next
        console.log(parasiteCount);
        console.log(anyInteractionCount);
        console.log(noHit);
        return;
    };
    console.log('- - - - - -- - - - - - -');


    cursor.next().then(speci => {
        speci.name = speci.name.split(' ').slice(0, 2).join(' ').replace(/[^A-z0-9\ ]/g, '');
        console.log(encodeURIComponent(speci.name));
        req.get({ path: `/interaction?type=json.v2&interactionType=parasiteOf&limit=${limit}&sourceTaxon=${encodeURIComponent(speci.name)}&field=target_taxon_path&field=target_taxon_external_id&field=target_taxon_path_ranks` },
            (status, headers, body) => {
                console.log(status);
                body = JSON.parse(body);

                if (body.length) { parasiteCount++ } //

                else {
                    req.get({ path: `/interaction?type=json.v2&interactionType=interactsWith&limit=${limit}&sourceTaxon=${encodeURIComponent(speci.name)}&field=target_taxon_path&field=target_taxon_external_id&field=target_taxon_path_ranks` },
                        (status, headers, body) => {
                            console.log(status);
                            body = JSON.parse(body);

                            if (body.length) { anyInteractionCount++ }
                            else { noHit++ }
                        });
                }

                for (const interactionResult of body) {
                    try {
                        if ('|' === interactionResult.target_taxon_path_ranks.slice(-1))
                            interactionResult.target_taxon_path_ranks += ' ';
                        interactionResult.key = interactionResult.target_taxon_path_ranks.split(' | ');
                        interactionResult.val = interactionResult.target_taxon_path.split(' | ');
                    } catch (e) { continue; }

                }
                console.log(body);
                console.log(parasiteCount);
                console.log(anyInteractionCount);
                console.log(noHit);
                testIfSpeciesIsParasyte(cursor);
            })
    });
};


return;




var species = ["plasmodium", "homo%20sapiens", "yersinia%20pestis"];

for (let i = 0; i < species.length; i++) {
    console.log("Now searching for :" + species[i]);
    testIfSpeciesIsParasyte(species[i], interaction);
};



// get names without foo split whitespace slice 0,2
//programm a recursive function instead of for loop

//api.globalbioticinteractions.org/interaction?type=json.v2&interactionType=parasiteOf&limit=15&offset=0&sourceTaxon=Yersinia%20pestis&   field=source_taxon_name&field=source_taxon_external_id&field=target_taxon_name&field=target_taxon_external_id&field=interaction_type&field=number_of_interactions
//api.globalbioticinteractions.org/interaction?type=json.v2&interactionType=parasiteOf&limit=15&offset=0&sourceTaxon=eimeria&             field=source_taxon_name&field=source_taxon_external_id&field=target_taxon_name&field=target_taxon_external_id&field=interaction_type&field=number_of_interactions


//api.globalbioticinteractions.org/interaction?type=json.v2&interactionType=interactsWith&limit=15&offset=0&sourceTaxon=Lasioglossum%20zonulum&field=source_taxon_name&field=source_taxon_external_id&field=target_taxon_name&field=target_taxon_external_id&field=interaction_type&field=number_of_interactions