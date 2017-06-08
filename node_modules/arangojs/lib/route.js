'use strict';

Object.defineProperty(exports, "__esModule", {
  value: true
});

var _extends = Object.assign || function (target) { for (var i = 1; i < arguments.length; i++) { var source = arguments[i]; for (var key in source) { if (Object.prototype.hasOwnProperty.call(source, key)) { target[key] = source[key]; } } } return target; };

var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

var Route = function () {
  function Route(connection, path, headers) {
    _classCallCheck(this, Route);

    if (!path) path = '';else if (path.charAt(0) !== '/') path = '/' + path;
    this._connection = connection;
    this._path = path;
    this._headers = headers;
  }

  _createClass(Route, [{
    key: 'route',
    value: function route(path, headers) {
      if (!path) path = '';else if (path.charAt(0) !== '/') path = '/' + path;
      return new Route(this._connection, this._path + path, _extends({}, this._headers, headers));
    }
  }, {
    key: 'request',
    value: function request(opts, callback) {
      opts = _extends({}, opts);
      opts.basePath = this._path;
      opts.headers = _extends({}, this._headers, opts.headers);
      opts.method = opts.method ? opts.method.toUpperCase() : 'GET';
      return this._connection.request(opts, callback);
    }
  }, {
    key: 'get',
    value: function get(path, qs, headers, callback) {
      if (typeof path !== 'string') {
        callback = qs;
        qs = path;
        path = undefined;
      }
      if (typeof qs === 'function') {
        callback = qs;
        qs = undefined;
      }
      if (typeof headers === 'function') {
        callback = headers;
        headers = undefined;
      }
      if (!path) path = '';else if (this._path && path.charAt(0) !== '/') path = '/' + path;
      headers = headers ? _extends({}, this._headers, headers) : _extends({}, this._headers);
      return this._connection.request({
        basePath: this._path,
        path: path,
        qs: qs,
        headers: headers,
        method: 'GET'
      }, callback);
    }
  }, {
    key: 'post',
    value: function post(path, body, qs, headers, callback) {
      if (typeof path !== 'string') {
        callback = qs;
        qs = body;
        body = path;
        path = undefined;
      }
      if (typeof qs === 'function') {
        callback = qs;
        qs = undefined;
      }
      if (typeof body === 'function') {
        callback = body;
        body = undefined;
      }
      if (typeof headers === 'function') {
        callback = headers;
        headers = undefined;
      }
      if (!path) path = '';else if (this._path && path.charAt(0) !== '/') path = '/' + path;
      headers = headers ? _extends({}, this._headers, headers) : _extends({}, this._headers);
      return this._connection.request({
        basePath: this._path,
        path: path,
        body: body,
        qs: qs,
        headers: headers,
        method: 'POST'
      }, callback);
    }
  }, {
    key: 'put',
    value: function put(path, body, qs, headers, callback) {
      if (typeof path !== 'string') {
        callback = body;
        body = qs;
        qs = path;
        path = undefined;
      }
      if (typeof qs === 'function') {
        callback = qs;
        qs = undefined;
      }
      if (typeof body === 'function') {
        callback = body;
        body = undefined;
      }
      if (typeof headers === 'function') {
        callback = headers;
        headers = undefined;
      }
      if (!path) path = '';else if (this._path && path.charAt(0) !== '/') path = '/' + path;
      headers = headers ? _extends({}, this._headers, headers) : _extends({}, this._headers);
      return this._connection.request({
        basePath: this._path,
        path: path,
        body: body,
        qs: qs,
        headers: headers,
        method: 'PUT'
      }, callback);
    }
  }, {
    key: 'patch',
    value: function patch(path, body, qs, headers, callback) {
      if (typeof path !== 'string') {
        callback = body;
        body = qs;
        qs = path;
        path = undefined;
      }
      if (typeof qs === 'function') {
        callback = qs;
        qs = undefined;
      }
      if (typeof body === 'function') {
        callback = body;
        body = undefined;
      }
      if (typeof headers === 'function') {
        callback = headers;
        headers = undefined;
      }
      if (!path) path = '';else if (this._path && path.charAt(0) !== '/') path = '/' + path;
      headers = headers ? _extends({}, this._headers, headers) : _extends({}, this._headers);
      return this._connection.request({
        basePath: this._path,
        path: path,
        body: body,
        qs: qs,
        headers: headers,
        method: 'PATCH'
      }, callback);
    }
  }, {
    key: 'delete',
    value: function _delete(path, qs, headers, callback) {
      if (typeof path !== 'string') {
        callback = qs;
        qs = path;
        path = undefined;
      }
      if (typeof qs === 'function') {
        callback = qs;
        qs = undefined;
      }
      if (typeof headers === 'function') {
        callback = headers;
        headers = undefined;
      }
      if (!path) path = '';else if (this._path && path.charAt(0) !== '/') path = '/' + path;
      headers = headers ? _extends({}, this._headers, headers) : _extends({}, this._headers);
      return this._connection.request({
        basePath: this._path,
        path: path,
        qs: qs,
        headers: headers,
        method: 'DELETE'
      }, callback);
    }
  }, {
    key: 'head',
    value: function head(path, qs, headers, callback) {
      if (typeof path !== 'string') {
        callback = qs;
        qs = path;
        path = undefined;
      }
      if (typeof qs === 'function') {
        callback = qs;
        qs = undefined;
      }
      if (typeof headers === 'function') {
        callback = headers;
        headers = undefined;
      }
      if (!path) path = '';else if (this._path && path.charAt(0) !== '/') path = '/' + path;
      headers = headers ? _extends({}, this._headers, headers) : _extends({}, this._headers);
      return this._connection.request({
        basePath: this._path,
        path: path,
        qs: qs,
        headers: headers,
        method: 'HEAD'
      }, callback);
    }
  }]);

  return Route;
}();

exports.default = Route;