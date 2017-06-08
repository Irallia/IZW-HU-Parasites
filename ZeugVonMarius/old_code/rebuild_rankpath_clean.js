'use strict';

const fastango = require('fastango3')('http://127.0.0.1:8529');

const convert = () => {
    const db = require("@arangodb").db;

    const rankDefs = ['kingdom', 'phylum', 'class', 'order', 'family', 'genus', 'species'];

    const allowed = {'kingdom':'phylum', 'phylum':'class', 'class':'order', 'order':'family', 'family':'genus', 'genus':'species'};

    const it = db._query('for doc in interaction_tsv return doc._key'); // 36005964

    while (it.hasNext()) {
        const doc = db.interaction_tsv.document(it.next());

        if (!doc.sourceTaxonPathRankNames || !doc.sourceTaxonPathNames) continue;

        if ('|' === doc.sourceTaxonPathRankNames[0]) doc.sourceTaxonPathRankNames = ' ' + doc.sourceTaxonPathRankNames;
        if ('|' === doc.sourceTaxonPathRankNames[-1]) doc.sourceTaxonPathRankNames = doc.sourceTaxonPathRankNames + ' ';

        if ('|' === doc.sourceTaxonPathNames[0]) doc.sourceTaxonPathNames = ' ' + doc.sourceTaxonPathNames;
        if ('|' === doc.sourceTaxonPathNames[-1]) doc.sourceTaxonPathNames = doc.sourceTaxonPathNames + ' ';

        const rankNames = doc.sourceTaxonPathRankNames.toLowerCase().split(' | ');
        const pathNames = doc.sourceTaxonPathNames.toLowerCase().split(' | ');

        let rankOut = [];
        let pathOut = [];

        for (const idx in rankNames) {
            const rankName = rankNames[idx];

            if (!~rankDefs.indexOf(rankName)) continue;

            rankOut.push(rankNames[idx]);
            pathOut.push(pathNames[idx]);
        }

        if (1 < rankOut.filter(b => b == 'genus').length) {
            const i = rankOut.indexOf('genus');
            rankOut = rankOut.slice(0, i);
            pathOut = pathOut.slice(0, i);

            rankOut.push('genus');
            pathOut.push(doc.sourceTaxonName);
        }

        if (1 < rankOut.filter(b => b == 'species').length) {
            const i = rankOut.indexOf('species');
            rankOut = rankOut.slice(0, i);
            pathOut = pathOut.slice(0, i);

            rankOut.push('species');
            pathOut.push(doc.sourceTaxonName);
        }

        if (rankOut[0] == 'kingdom' && rankOut[1] == 'kingdom') {
            pathOut.shift(); // animalia
            rankOut.shift(); // kingdom
        } // if

        //return [pathOut, rankOut];



        //db.interaction_tsv.update(doc._id, { simplePath: pathOut.join(' | '), simpleRank: rankOut.join(' | ') });

        for(const idx in pathOut) {
            const keyFrom = `${rankOut[idx]}_${pathOut[idx]}`.replace(/\ +/g, '_');
            let interaction = null;
            if (idx == pathOut.length -1) interaction = doc.interactionTypeName;
            try{
            //db.nodes_interaction.save({_key:keyFrom, rank:rankOut[idx], rankName:pathOut[idx], interaction:interaction});
            }catch(e) {}
            const idxPlus = 1 + Number(idx);
            if (pathOut[idxPlus]) {
                if (allowed[rankOut[idx]] != rankOut[idxPlus]) continue;

                const keyTo   = `${rankOut[idxPlus]}_${pathOut[idxPlus]}`.replace(/\ +/g, '_');
                try {
                db.edges_interaction.save({_from: 'nodes_interaction/' + keyFrom,
                                             _to: 'nodes_interaction/' + keyTo});
                }catch (e) {}
            }
        }
    }



    return true;
}

fastango._txn({ collections: { read: ['interaction_tsv'], write: ['interaction_tsv', 'nodes_interaction', 'edges_interaction'] } }, convert, (status, headers, body) => {
    console.log(status);
    console.log(body.toString());
});


// Loop throught interaction_tsv; every doc
// split doc.sourceTaxonPathRankNames ( | )