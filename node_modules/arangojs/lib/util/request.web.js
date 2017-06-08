'use strict';

Object.defineProperty(exports, "__esModule", {
  value: true
});

var _extends = Object.assign || function (target) { for (var i = 1; i < arguments.length; i++) { var source = arguments[i]; for (var key in source) { if (Object.prototype.hasOwnProperty.call(source, key)) { target[key] = source[key]; } } } return target; };

exports.default = function (baseUrl, options) {
  if (!options) options = {};
  var baseUrlParts = (0, _url.parse)(baseUrl);

  var queue = [];
  var maxTasks = typeof options.maxSockets === 'number' ? options.maxSockets * 2 : Infinity;
  var activeTasks = 0;

  function drainQueue() {
    if (!queue.length || activeTasks >= maxTasks) return;
    var task = queue.shift();
    activeTasks += 1;
    task(function () {
      activeTasks -= 1;
      drainQueue();
    });
  }

  function request(_ref, cb) {
    var method = _ref.method,
        url = _ref.url,
        headers = _ref.headers,
        body = _ref.body,
        expectBinary = _ref.expectBinary;

    var urlParts = _extends({}, baseUrlParts, {
      pathname: url.pathname ? baseUrlParts.pathname ? joinPath(baseUrlParts.pathname, url.pathname) : url.pathname : baseUrlParts.pathname,
      search: url.search ? baseUrlParts.search ? baseUrlParts.search + '&' + url.search.slice(1) : url.search : baseUrlParts.search
    });

    queue.push(function (next) {
      var _callback = function callback(err, res) {
        _callback = function callback() {
          return undefined;
        };
        next();
        cb(err, res);
      };
      var req = (0, _xhr2.default)(_extends({
        responseType: expectBinary ? 'blob' : 'text'
      }, options, {
        url: (0, _url.format)(urlParts),
        withCredentials: true,
        useXDR: true,
        body: body,
        method: method,
        headers: headers
      }), function (err, res) {
        if (!err) _callback(null, res);else {
          err.request = req;
          _callback(err);
        }
      });
    });

    drainQueue();
  }

  var auth = baseUrlParts.auth;
  delete baseUrlParts.auth;
  return { request: request, auth: auth, url: baseUrlParts };
};

var _xhr = require('xhr');

var _xhr2 = _interopRequireDefault(_xhr);

var _url = require('url');

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

function joinPath() {
  var a = arguments.length > 0 && arguments[0] !== undefined ? arguments[0] : '';
  var b = arguments.length > 1 && arguments[1] !== undefined ? arguments[1] : '';

  if (!a && !b) return '';
  var leadingSlash = a.charAt(0) === '/';
  var trailingSlash = b.charAt(b.length - 1) === '/';
  var tokens = (a + '/' + b).split('/').filter(Boolean);
  for (var i = 0; i < tokens.length; i++) {
    var token = tokens[i];
    if (token === '..') {
      tokens.splice(i - 1, 2);
      i--;
    } else if (token === '.') {
      tokens.splice(i, 1);
      i--;
    }
  }
  var path = tokens.join('/');
  if (leadingSlash) path = '/' + path;
  if (trailingSlash) path = path + '/';
  return path;
}