"use strict";

Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.default = promisify;
var noop = function noop() {
  return undefined;
};

function promisify(promiseClass) {
  if (promiseClass === false) {
    return function (cb) {
      return { callback: cb || noop };
    };
  }

  return function (cb) {
    var Promise = promiseClass || global.Promise;

    if (cb || !Promise) {
      return { callback: cb || noop };
    }

    var callback = void 0;
    var promise = new Promise(function (resolve, reject) {
      callback = function callback(err, res) {
        if (err) reject(err);else resolve(res);
      };
    });

    return { callback: callback, promise: promise };
  };
}