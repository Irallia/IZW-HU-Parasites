'use strict';

Object.defineProperty(exports, "__esModule", {
  value: true
});

exports.default = function (baseUrl, agentOptions, agent) {
  var baseUrlParts = (0, _url.parse)(baseUrl);
  var isTls = baseUrlParts.protocol === 'https:';

  if (!agent) {
    var Agent = (isTls ? _https2.default : _http2.default).Agent;
    agent = new Agent(agentOptions);
  }

  var queue = new _linkedlist2.default();
  var maxTasks = typeof agent.maxSockets === 'number' ? agent.maxSockets * 2 : Infinity;
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

    var path = baseUrlParts.pathname ? url.pathname ? joinPath(baseUrlParts.pathname, url.pathname) : baseUrlParts.pathname : url.pathname;
    var search = url.search ? baseUrlParts.search ? baseUrlParts.search + '&' + url.search.slice(1) : url.search : baseUrlParts.search;
    if (search) path += search;
    var options = { path: path, method: method, headers: headers, agent: agent };
    options.hostname = baseUrlParts.hostname;
    options.port = baseUrlParts.port;
    options.auth = baseUrlParts.auth;

    queue.push(function (next) {
      var _callback = function callback(err, res) {
        _callback = function callback() {
          return undefined;
        };
        next();
        cb(err, res);
      };
      var req = (isTls ? _https2.default : _http2.default).request(options, function (res) {
        var data = [];
        res.on('data', function (chunk) {
          return data.push(chunk);
        }).on('end', function () {
          res.body = Buffer.concat(data);
          if (!expectBinary) {
            res.body = res.body.toString('utf-8');
          }
          _callback(null, res);
        });
      });
      req.on('error', function (err) {
        err.request = req;
        _callback(err);
      });
      if (body) req.write(body);
      req.end();
    });

    drainQueue();
  }

  var auth = baseUrlParts.auth;
  delete baseUrlParts.auth;
  return { request: request, auth: auth, url: baseUrlParts };
};

var _http = require('http');

var _http2 = _interopRequireDefault(_http);

var _https = require('https');

var _https2 = _interopRequireDefault(_https);

var _url = require('url');

var _linkedlist = require('linkedlist');

var _linkedlist2 = _interopRequireDefault(_linkedlist);

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