'use strict';

Object.defineProperty(exports, "__esModule", {
  value: true
});

var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

function _toConsumableArray(arr) { if (Array.isArray(arr)) { for (var i = 0, arr2 = Array(arr.length); i < arr.length; i++) { arr2[i] = arr[i]; } return arr2; } else { return Array.from(arr); } }

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

var ArrayCursor = function () {
  function ArrayCursor(connection, body) {
    _classCallCheck(this, ArrayCursor);

    this.extra = body.extra;
    this._connection = connection;
    this._api = this._connection.route('/_api');
    this._result = body.result;
    this._hasMore = Boolean(body.hasMore);
    this._id = body.id;
    this.count = body.count;
  }

  _createClass(ArrayCursor, [{
    key: '_drain',
    value: function _drain(cb) {
      var _this = this;

      var _connection$promisify = this._connection.promisify(cb),
          promise = _connection$promisify.promise,
          callback = _connection$promisify.callback;

      this._more(function (err) {
        return err ? callback(err) : !_this._hasMore ? callback(null, _this) : _this._drain(cb);
      });
      return promise;
    }
  }, {
    key: '_more',
    value: function _more(callback) {
      var _this2 = this;

      if (!this._hasMore) callback(null, this);else {
        this._api.put('/cursor/' + this._id, function (err, res) {
          if (err) callback(err);else {
            var _result;

            (_result = _this2._result).push.apply(_result, _toConsumableArray(res.body.result));
            _this2._hasMore = res.body.hasMore;
            callback(null, _this2);
          }
        });
      }
    }
  }, {
    key: 'all',
    value: function all(cb) {
      var _this3 = this;

      var _connection$promisify2 = this._connection.promisify(cb),
          promise = _connection$promisify2.promise,
          callback = _connection$promisify2.callback;

      this._drain(function (err) {
        if (err) callback(err);else {
          var result = _this3._result;
          _this3._result = [];
          callback(null, result);
        }
      });
      return promise;
    }
  }, {
    key: 'next',
    value: function next(cb) {
      var _this4 = this;

      var _connection$promisify3 = this._connection.promisify(cb),
          promise = _connection$promisify3.promise,
          callback = _connection$promisify3.callback;

      var next = function next() {
        var value = _this4._result.shift();
        callback(null, value);
      };
      if (this._result.length) next();else {
        if (!this._hasMore) callback(null);else {
          this._more(function (err) {
            return err ? callback(err) : next();
          });
        }
      }
      return promise;
    }
  }, {
    key: 'hasNext',
    value: function hasNext() {
      return Boolean(this._hasMore || this._result.length);
    }
  }, {
    key: 'each',
    value: function each(fn, cb) {
      var _this5 = this;

      var _connection$promisify4 = this._connection.promisify(cb),
          promise = _connection$promisify4.promise,
          callback = _connection$promisify4.callback;

      var index = 0;
      var loop = function loop() {
        try {
          var result = void 0;
          while (_this5._result.length) {
            result = fn(_this5._result.shift(), index, _this5);
            index++;
            if (result === false) break;
          }
          if (!_this5._hasMore || result === false) callback(null, result);else {
            _this5._more(function (err) {
              return err ? callback(err) : loop();
            });
          }
        } catch (e) {
          callback(e);
        }
      };
      loop();
      return promise;
    }
  }, {
    key: 'every',
    value: function every(fn, cb) {
      var _this6 = this;

      var _connection$promisify5 = this._connection.promisify(cb),
          promise = _connection$promisify5.promise,
          callback = _connection$promisify5.callback;

      var index = 0;
      var loop = function loop() {
        try {
          var result = true;
          while (_this6._result.length) {
            result = fn(_this6._result.shift(), index, _this6);
            index++;
            if (!result) break;
          }
          if (!_this6._hasMore || !result) callback(null, Boolean(result));else {
            _this6._more(function (err) {
              return err ? callback(err) : loop();
            });
          }
        } catch (e) {
          callback(e);
        }
      };
      loop();
      return promise;
    }
  }, {
    key: 'some',
    value: function some(fn, cb) {
      var _this7 = this;

      var _connection$promisify6 = this._connection.promisify(cb),
          promise = _connection$promisify6.promise,
          callback = _connection$promisify6.callback;

      var index = 0;
      var loop = function loop() {
        try {
          var result = false;
          while (_this7._result.length) {
            result = fn(_this7._result.shift(), index, _this7);
            index++;
            if (result) break;
          }
          if (!_this7._hasMore || result) callback(null, Boolean(result));else {
            _this7._more(function (err) {
              return err ? callback(err) : loop();
            });
          }
        } catch (e) {
          callback(e);
        }
      };
      loop();
      return promise;
    }
  }, {
    key: 'map',
    value: function map(fn, cb) {
      var _this8 = this;

      var _connection$promisify7 = this._connection.promisify(cb),
          promise = _connection$promisify7.promise,
          callback = _connection$promisify7.callback;

      var index = 0;
      var result = [];
      var loop = function loop() {
        try {
          while (_this8._result.length) {
            result.push(fn(_this8._result.shift(), index, _this8));
            index++;
          }
          if (!_this8._hasMore) callback(null, result);else {
            _this8._more(function (err) {
              return err ? callback(err) : loop();
            });
          }
        } catch (e) {
          callback(e);
        }
      };
      loop();
      return promise;
    }
  }, {
    key: 'reduce',
    value: function reduce(fn, accu, cb) {
      var _this9 = this;

      if (typeof accu === 'function') {
        cb = accu;
        accu = undefined;
      }
      var index = 0;

      var _connection$promisify8 = this._connection.promisify(cb),
          promise = _connection$promisify8.promise,
          callback = _connection$promisify8.callback;

      var loop = function loop() {
        try {
          while (_this9._result.length) {
            accu = fn(accu, _this9._result.shift(), index, _this9);
            index++;
          }
          if (!_this9._hasMore) callback(null, accu);else {
            _this9._more(function (err) {
              return err ? callback(err) : loop();
            });
          }
        } catch (e) {
          callback(e);
        }
      };
      if (accu !== undefined) {
        loop();
      } else if (this._result.length > 1) {
        accu = this._result.shift();
        index = 1;
        loop();
      } else {
        this._more(function (err) {
          if (err) callback(err);else {
            accu = _this9._result.shift();
            index = 1;
            loop();
          }
        });
      }
      return promise;
    }
  }]);

  return ArrayCursor;
}();

exports.default = ArrayCursor;