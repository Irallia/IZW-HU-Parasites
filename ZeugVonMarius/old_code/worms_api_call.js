'use strict';

const http = require('request-easy').http;
const req = new http({ hostname: 'www.marinespecies.org' });
let inputSpecies = encodeURIComponent('Vibrio cholerae');



async function WORMSCall(inputSpecies) {

    let ID = await getAphiaID(inputSpecies);

    let lineage = await getLineage(ID);
}


async function getAphiaID(inputSpecies) {
    let [status, headers, body] = await req.asyncGet({ path: `/rest/AphiaIDByName/${inputSpecies}` });
    body = body.toString();

    console.log(status, headers);
    console.log(inputSpecies);
    console.log(body);
    let inputID = body;
    return inputID;
}

async function getLineage(inputID) {
    let [status, headers, body] = await req.asyncGet({ path: `/rest/AphiaClassificationByAphiaID/${inputID}` });
    body = JSON.parse(body);
    console.log(JSON.stringify(body, false, 4));

}

WORMSCall(inputSpecies);