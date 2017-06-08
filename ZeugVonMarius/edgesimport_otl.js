'use strict';

const fastango = require('fastango3')('http://127.0.0.1:8529');
const fs       = require('fs');
const instream = fs.createReadStream('data/taxonomy.tsv');

const bufs = [];

instream.on('data', async function(d) {
    instream.pause();
    bufs.push(d);
    await readNames();
    instream.resume();
});
instream.on('end', () => {
    readLast();
});

async function readNames() {
    const b = Buffer.concat(bufs);

    let start = 0;
    let idx;

    while(true) {
        idx = b.indexOf('\n', start);
        if (-1 === idx) {
            bufs.length = 0;
            bufs.push(b.slice(start));
            break;
        }
        await parseLine(b.slice(start, idx).toString());
        start = idx + 1;
    }
};

async function readLast() {
    const b = Buffer.concat(bufs);
    if (0 === b.length) return;
    await parseLine(b.toString());
};

async function parseLine(line) {
    line = line.split('\t|\t');
    await fastango.edges_otl.asyncSave(JSON.stringify({ _key:`${line[0]}`, _to:`nodes_otl/${line[0]}`, _from:`nodes_otl/${line[1]}`, rank:`${line[3]}`, name:`${line[2]}` }));


    // await fastango._asyncQ(`for doc in names
    // filter doc._key == '${line[0]}'
    // update doc with {rank:'${line[2]}'} in names`);

    console.log(line[0], line[1]);
};


