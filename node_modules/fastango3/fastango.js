'use strict';

const url  = require('url');

const http  = require('request-easy').http;
const https = require('request-easy').https;

const setupCollection = (fastango, collectionName) => {
    const docUrl = `/_db/${fastango._currentDb}/_api/document/${collectionName}`;
    const colUrl = `/_db/${fastango._currentDb}/_api/collection`;

    fastango[collectionName] = {
        save(str, opts, callback = () => {}) {
            if (typeof opts == 'function') {
                callback = opts;
                opts = {};
            } // if
            let urlStr = '?';
            for(const key in opts) {
                urlStr += `${key}=${opts[key]}&`;
            } // for
            fastango.req.post({path:`${docUrl}${urlStr}`, buffer:Buffer.from(str)}, callback);
        },

        asyncSave(str, opts = {}) {
            let urlStr = '?';
            for(const key in opts) {
                urlStr += `${key}=${opts[key]}&`;
            } // for
            return fastango.req.asyncPost({path:`${docUrl}${urlStr}`, buffer:Buffer.from(str)});
        },

        document(key, callback = () => {}) {
            fastango.req.get({path:`${docUrl}/${key}`}, callback);
        },

        update(key, str, opts, callback = () => {}) {
            if (typeof opts === 'function') {
                callback = opts;
                opts = {};
            } // if
            let urlStr = '?';
            for(const key in opts) {
                urlStr += `${key}=${opts[key]}&`;
            } // for
            fastango.req.patch({path:`${docUrl}/${key}${urlStr}`, buffer:Buffer.from(str)}, callback);
        },

        replace(key, str, opts, callback = () => {}) {
            if (typeof opts === 'function') {
                callback = opts;
                opts = {};
            } // if
            let urlStr = '?';
            for(const key in opts) {
                urlStr += `${key}=${opts[key]}&`;
            } // for
            fastango.req.put({path:`${docUrl}/${key}${urlStr}`, buffer:Buffer.from(str)}, callback);
        },

        remove(key, opts, callback = () => {}) {
            if (typeof opts === 'function') {
                callback = opts;
                opts = {};
            } // if
            let urlStr = '?';
            for(const key in opts) {
                urlStr += `${key}=${opts[key]}&`;
            } // for
            fastango.req.delete({path:`${docUrl}/${key}${urlStr}`}, callback);
        },

        /* collection operations */

        create(opts, callback = () => {}) {
            if(typeof opts === 'function') {
                callback = opts;
                opts = {};
            } // if
            opts.name = collectionName;
            fastango.req.post({path:colUrl, buffer:Buffer.from(JSON.stringify(opts))}, callback);
        },

        truncate(callback = () => {}) {
            fastango.req.put({path:`${colUrl}/${collectionName}/truncate`}, callback);
        },

        drop(callback = () => {}) {
            fastango.req.delete({path:`${colUrl}/${collectionName}`}, (status, headers, body) => {
                if (200 === status) {
                    fastango[collectionName] = null;
                    delete fastango[collectionName];
                } // if
                callback(status, headers, body);
            });
        }
    }
};

const fastangoCursor = (url, req, status, body) => {
    try {
        body = JSON.parse(body);
    } catch(e) {
        body   = {code: 500, errorMessage:`Can't parse returned JSON`, error:true};
        status = 500;
    }

    return {
        _result:  body.result,
        _hasMore: body.hasMore,
        _count:   body.count,
        _id:      body.id,
        _idx:     0,

        _all(callback) {
            this._more((status) => {
                if (200 !== status || !this._hasMore) {
                    return callback(status);
                } // if
                this._all(callback);
            });
        },

        _more(callback) {
            if (! this._hasMore) {
                return callback(200);
            } // if

            req.put({path:url+this._id}, (status, headers, body) => {
                if (200 !== status) {
                    return callback(status);
                } // if

                try {
                    body = JSON.parse(body);
                } catch(e) {
                    return callback(500);
                }

                this._result.push(...body.result);
                this._hasMore = body.hasMore;

                callback(status);
            });
        },

        all(callback = () => {}) {
            if (201 !== status) {
                return callback(status, [], body);
            } // if

            this._all((status) => {
                this._idx = this._result.length;
                callback(status, this._result, body.extra);
            });
        }
    }
};


const fastangoStarter = {
        _q(aql, bindVars, opts, callback) {
            if (typeof bindVars === 'function') {
                callback = bindVars;
                bindVars = undefined;
            } // if
            if (typeof opts === 'function') {
                callback = opts;
                opts = undefined;
            } // if

            const data = {
                query: aql,
                bindVars: bindVars || undefined
            };

            if (opts) {
                data.batchSize = opts.batchSize || undefined;
                data.ttl =       opts.ttl || undefined;
                data.count =     opts.count || false;

                data.options = {
                    profile:   opts.profile || false,
                    fullCount: opts.fullCount || false,
                    maxPlans:  opts.maxPlans || undefined,
                    'optimizer.rules': opts.optimizerRules || undefined
                };
            } // if

            this.req.post({path:this._cursorUrl, buffer:new Buffer(JSON.stringify(data))}, (status, headers, body) => {
                const cursor = fastangoCursor(`${this._cursorUrl}/`, this.req, status, body);
                if (opts && opts.all) {
                    cursor.all(callback);
                } else {
                    callback(status, cursor);
                }
            });
        },

        _asyncQ(aql, bindVars, opts) {
            if (typeof bindVars === 'function') {
                callback = bindVars;
                bindVars = undefined;
            } // if
            if (typeof opts === 'function') {
                callback = opts;
                opts = undefined;
            } // if

            const data = {
                query: aql,
                bindVars: bindVars || undefined
            };

            if (opts) {
                data.batchSize = opts.batchSize || undefined;
                data.ttl =       opts.ttl || undefined;
                data.count =     opts.count || false;

                data.options = {
                    profile:   opts.profile || false,
                    fullCount: opts.fullCount || false,
                    maxPlans:  opts.maxPlans || undefined,
                    'optimizer.rules': opts.optimizerRules || undefined
                };
            } // if

            return new Promise((resolve) => {
                this.req.post({path:this._cursorUrl, buffer:new Buffer(JSON.stringify(data))}, (status, headers, body) => {
                    const cursor = fastangoCursor(`${this._cursorUrl}/`, this.req, status, body);
                    if (opts && opts.all) {
                        cursor.all((status, result, extra) => resolve([status, result, extra]));
                    } else {
                        resolve([status, cursor]);
                    }
                });
            });
        },

        _txn(opts, func, callback) {
            if (typeof opts === 'function') {
                callback = func;
                func = opts;
                opts = {};
            } // if
            opts.action = String(func);
            this.req.post({path: this._txnUrl, buffer:Buffer.from(JSON.stringify(opts))}, callback);
        },

        _asyncTxn(opts, func) {
            if (typeof opts === 'function') {
                func = opts;
                opts = {collections:{}};
            } // if
            opts.action = String(func);
            return this.req.asyncPost({path: this._txnUrl, buffer:Buffer.from(JSON.stringify(opts))});
        },
    }


// construct new fastango
module.exports = (conUrl, currentDb = '_system') => {
    conUrl = url.parse(conUrl);
    const fastango = Object.create(fastangoStarter);
    if ('https:' === conUrl.protocol) {
        fastango.req = new https({hostname:conUrl.hostname, port:conUrl.port, setContentLength:true});
    } else {
        fastango.req = new http({hostname:conUrl.hostname, port:conUrl.port, setContentLength:true});
    }

    fastango._currentDb = currentDb;
    fastango._txnUrl    = `/_db/${fastango._currentDb}/_api/transaction`;
    fastango._cursorUrl = `/_db/${fastango._currentDb}/_api/cursor`;

    return new Proxy(fastango, {
        get(target, prop, receiver) {
            if (target[prop]) {
                return target[prop];
            } // if

            // init
            setupCollection(target, prop);

            return target[prop];
        } // get()  
    });
}
