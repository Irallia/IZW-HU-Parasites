'use strict';

const crypto = require('crypto');
const https =  require('https');
const http  =  require('http');

const rawRequest = require('./rawRequest');

const httpAgent  = new http.Agent({  keepAlive: true });
const httpsAgent = new https.Agent({ keepAlive: true });

const log = require('./log');


class Request {
    constructor(opts) {
        if (!opts.headers) opts.headers = {};
        this.opts = opts;
    }

    reqOpts(opts = {headers:{}}) {
        const headers = Object.assign({}, this.opts.headers, opts.headers);
        const reqOpts = Object.assign({}, this.opts,         opts);
        reqOpts.headers = headers;
        if ( isNaN(reqOpts.tries)) reqOpts.tries = 0;
        if ( ! reqOpts.id) reqOpts.id = `${Date.now()}.${crypto.randomBytes(4).toString('hex')}`;
        reqOpts.tries++;

        return reqOpts;
    }

    head(opts, cb) { this.doRequest(opts, 'HEAD', cb); }

    get(opts, cb) { this.doRequest(opts, 'GET', cb); }

    post(opts, cb) { this.doRequest(opts, 'POST', cb); }

    put(opts, cb) { this.doRequest(opts, 'PUT', cb); }

    patch(opts, cb) { this.doRequest(opts, 'PATCH', cb); }

    delete(opts, cb) { this.doRequest(opts, 'DELETE', cb); }

    // START async http
    asyncHead(opts, cb) {
        return new Promise((res) => {
            this.doRequest(opts, 'HEAD', (status, headers, body) => {
                res([status, headers, body]);
            });
        });
    }

    asyncGet(opts, cb) {
        return new Promise((res) => {
            this.doRequest(opts, 'GET', (status, headers, body) => {
                res([status, headers, body]);
            });
        });
    }

    asyncPost(opts, cb) {
        return new Promise((res) => {
            this.doRequest(opts, 'POST', (status, headers, body) => {
                res([status, headers, body]);
            });
        });
    }

    asyncPut(opts, cb) {
        return new Promise((res) => {
            this.doRequest(opts, 'PUT', (status, headers, body) => {
                res([status, headers, body]);
            });
        });
    }

    asyncPatch(opts, cb) {
        return new Promise((res) => {
            this.doRequest(opts, 'PATCH', (status, headers, body) => {
                res([status, headers, body]);
            });
        });
    }

    asyncDelete(opts, cb) {
        return new Promise((res) => {
            this.doRequest(opts, 'DELETE', (status, headers, body) => {
                res([status, headers, body]);
            });
        });
    }
    // END async http


    doRequest(opts, method, cb) {
        const reqOpts = this.reqOpts(opts);
        reqOpts.method = method;

        rawRequest(reqOpts, (err, status, headers, body) => {
          this.handleResponse(reqOpts, cb, err, status, headers, body);
        });
    }

    handleResponse(reqOpts, cb, err, status, headers, body = Buffer.alloc(0)) {
        log.line(`${reqOpts.id} - ${reqOpts.method}:${reqOpts.hostname}${reqOpts.path} Tries: ${reqOpts.tries}, Status: ${status}, Length: ${body.length}`);

        const handler = reqOpts.externalHandler || this;

        if (err) {
            if (handler.onError) {
                log.line(`${reqOpts.id} - Request: err handler.onError()`, err);
                handler.onError(reqOpts, cb, err, status, headers, body);
                return;
            } // if

            if (reqOpts.retryOnError) {
                log.line(`${reqOpts.id} - Request: err retry`, err);
                handler[reqOpts.method.toLowerCase()](reqOpts, cb);
                return;
            } // if

            log.line(`${reqOpts.id} - Request: err cb()`, err);
            cb(0, null, null);
            return;
        } // if

        // try status code ranges
        if (200 <= status && status < 300 && handler.on2xx) {
            handler.on2xx(reqOpts, cb, err, status, headers, body);
            return;
        }

        if(300 <= status && status < 400 && handler.on3xx) {
            handler.on3xx(reqOpts, cb, err, status, headers, body);
            return;
        }

        if(400 <= status && status < 500 && handler.on4xx) {
            handler.on4xx(reqOpts, cb, err, status, headers, body);
            return;
        }

        if(500 <= status && status < 600 && handler.on5xx) {
            handler.on5xx(reqOpts, cb, err, status, headers, body);
            return;
        }

        if(600 <= status && handler.on6xx) {
            handler.on6xx(reqOpts, cb, err, status, headers, body);
            return;
        }

        // try one specific status code
        const onStatus = `on${status}`;

        if (handler[onStatus]) {
            log.line(`${reqOpts.id} - Request: handler[${onStatus}]()`);
            handler[onStatus](reqOpts, cb, err, status, headers, body);
            return;
        } // if

        if(500 <= status && status < 600) {
            const enoughtTriesLeft = reqOpts.maxTries ? reqOpts.maxTries >= reqOpts.tries : true;
            if (reqOpts.retryOn5xx && enoughtTriesLeft) {
                log.line(`${reqOpts.id} - Request: callback on 500 <= ${status} < 600`);
                handler[reqOpts.method.toLowerCase()](reqOpts, cb);
                return;
            }
        } // if

        log.line(`${reqOpts.id} - Request: cb()`);
        cb(status, headers, body);
    } // handleResponse()
} // class

class HttpsRequest extends Request {
    constructor(opts = {}) {
        opts.con = https;
        if (!opts.agent) opts.agent = httpsAgent;
        super(opts);
    }
}

class HttpRequest extends Request {
    constructor(opts = {}) {
        opts.con = http;
        if (!opts.agent) opts.agent = httpAgent;
        super(opts);
    }
}

module.exports.http  = HttpRequest;
module.exports.https = HttpsRequest;
