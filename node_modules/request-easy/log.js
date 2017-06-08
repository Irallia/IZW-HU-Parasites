'use strict';

const fs = require('fs');

if (process.env.logRequestEasy != 'true') {
    module.exports.line = () => {};
    return;
}

const stream = fs.createWriteStream('log.log', {flags:'a'});

const logNow = module.exports.now = () => {
    stream.write(new Date().toISOString()+'\n');
}

module.exports.line = (...args) => {
    logNow();
    for(let arg of args) {
        if (arg instanceof Buffer) {
            try {
                arg = JSON.parse(arg);
            } catch(e) {
                arg = arg.toString('utf8');
            }
        }

        if (arg instanceof Object) {
            try {
                arg = JSON.stringify(arg, false, 2);
            } catch(e) {
                arg = arg.toString('utf8');
            }
        }

        stream.write(`${arg}\n`);
    }
};
