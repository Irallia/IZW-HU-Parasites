'use strict';

Object.defineProperty(exports, "__esModule", {
  value: true
});

var _typeof = typeof Symbol === "function" && typeof Symbol.iterator === "symbol" ? function (obj) { return typeof obj; } : function (obj) { return obj && typeof Symbol === "function" && obj.constructor === Symbol && obj !== Symbol.prototype ? "symbol" : typeof obj; };

exports.default = toForm;
function toForm(fields, callback) {
  var form = void 0;
  try {
    form = new global.FormData();
    var _iteratorNormalCompletion = true;
    var _didIteratorError = false;
    var _iteratorError = undefined;

    try {
      for (var _iterator = Object.keys(fields)[Symbol.iterator](), _step; !(_iteratorNormalCompletion = (_step = _iterator.next()).done); _iteratorNormalCompletion = true) {
        var key = _step.value;

        var value = fields[key];
        if (value === undefined) continue;
        if (!(value instanceof global.File) && ((typeof value === 'undefined' ? 'undefined' : _typeof(value)) === 'object' || typeof value === 'function')) {
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
  } catch (e) {
    callback(e);
    return;
  }
  callback(null, { body: form });
}