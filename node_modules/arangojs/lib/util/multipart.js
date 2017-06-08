'use strict';

Object.defineProperty(exports, "__esModule", {
  value: true
});

var _typeof = typeof Symbol === "function" && typeof Symbol.iterator === "symbol" ? function (obj) { return typeof obj; } : function (obj) { return obj && typeof Symbol === "function" && obj.constructor === Symbol && obj !== Symbol.prototype ? "symbol" : typeof obj; };

exports.default = toForm;

var _multiPart = require('multi-part');

var _multiPart2 = _interopRequireDefault(_multiPart);

var _stream = require('stream');

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

function toForm(fields, callback) {
  var called = false;
  try {
    var form = new _multiPart2.default();
    var _iteratorNormalCompletion = true;
    var _didIteratorError = false;
    var _iteratorError = undefined;

    try {
      for (var _iterator = Object.keys(fields)[Symbol.iterator](), _step; !(_iteratorNormalCompletion = (_step = _iterator.next()).done); _iteratorNormalCompletion = true) {
        var key = _step.value;

        var value = fields[key];
        if (value === undefined) continue;
        if (!(value instanceof _stream.Readable) && !(value instanceof global.Buffer) && ((typeof value === 'undefined' ? 'undefined' : _typeof(value)) === 'object' || typeof value === 'function')) {
          value = JSON.stringify(value);
        }
        form.append(key, value);
      }
    } catch (err) {
      _didIteratorError = true;
      _iteratorError = err;
    } finally {
      try {
        if (!_iteratorNormalCompletion && _iterator.return) {
          _iterator.return();
        }
      } finally {
        if (_didIteratorError) {
          throw _iteratorError;
        }
      }
    }

    var stream = form.getStream();
    var bufs = [];
    stream.on('data', function (buf) {
      return bufs.push(buf);
    });
    stream.on('end', function () {
      if (called) return;
      bufs.push(Buffer.from('\r\n'));
      var body = Buffer.concat(bufs);
      var boundary = form.getBoundary();
      var headers = {
        'content-type': 'multipart/form-data; boundary=' + boundary,
        'content-length': String(body.length)
      };
      called = true;
      callback(null, { body: body, headers: headers });
    });
    stream.on('error', function (e) {
      if (called) return;
      called = true;
      callback(e);
    });
  } catch (e) {
    if (called) return;
    called = true;
    callback(e);
  }
}