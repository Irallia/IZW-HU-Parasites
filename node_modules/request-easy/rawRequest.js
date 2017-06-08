'use strict';

const zlib  =  require('zlib');
const crypto = require('crypto');

const log = require('./log');

module.exports = (opts, cb) => {
    const reqId = crypto.randomBytes(4).toString('hex');
    log.line(`${opts.id} - ${reqId} - RawRequest: do ${opts.method}`);


    let doneCallback = false;

    if (opts.setContentLength && (opts.buffer instanceof Buffer)) {
        opts.headers['content-length'] = opts.buffer.length;
    } // if

    const req = opts.con.request(opts);
  
    req.on('error', (err) => {
        if (doneCallback) {
            log.line(`${opts.id} - ${reqId} - RawRequest: req.on.error doneCallback is true, return`);
            return;
        } // if
        doneCallback = true;

        log.line(`${opts.id} - ${reqId} - RawRequest: req.on.error callback`, err);
        cb(err);
    });

    req.on('response', (res) => {
        log.line(`${opts.id} - ${reqId} - RawRequest: req.on.response`);

        const length = Number(res.headers['content-length']);
        let buf;
        let i = 0;
  
        if (length) {
            buf = Buffer.alloc(length);
        } else {
            buf = Buffer.alloc(0);
        }

        res.on('error', (err) => {
            if (doneCallback) {
                log.line(`${opts.id} - ${reqId} - RawRequest: res.on.error doneCallback is true, return`);
                return;
            } // if
            doneCallback = true;

            log.line(`${opts.id} - ${reqId} - RawRequest: res.on.error callback`, err);
            cb(err, res.statusCode, res.headers, buf);
        });

        res.on('data', (d) => {
            if(length) {
                d.copy(buf, i);
                i += d.length;
            } else {
                buf = Buffer.concat([buf, d]);
            }
        });
        res.on('end', () => {
            log.line(`${opts.id} - ${reqId} - RawRequest: res.on.end`);
            if (doneCallback) {
                log.line(`${opts.id} - ${reqId} - RawRequest: res.on.end doneCallback is true, return`);
                return;
            } // if
            doneCallback = true;

            if (opts.method === 'HEAD') {
                cb(null, res.statusCode, res.headers, buf);
                return;
            } // if

            switch(res.headers['content-encoding']) {
                case 'gzip':
                    zlib.unzip(buf, (err, buf) => {
                        log.line(`${opts.id} - ${reqId} - RawRequest: res.on.end gzip zlib.unzip callback`);
                        cb(err, res.statusCode, res.headers, buf);
                    });
                    break;

                default:
                    log.line(`${opts.id} - ${reqId} - RawRequest: res.on.end default callback`);
                    cb(null, res.statusCode, res.headers, buf);
                    break;
            } // switch
        });
    });
  
    if (opts.buffer) {
        req.write(opts.buffer);
        req.end();

    } else if (opts.stream) {
        opts.stream.pipe(req);

    } else if (opts.externalWrite) {
        opts.externalWrite(req, opts, reqId);

    } else {
        req.end();
    }
}
