'use strict';

Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.default = aql;
function aql(strings) {
  var bindVars = {};
  var bindVals = [];
  var query = strings[0];

  for (var _len = arguments.length, args = Array(_len > 1 ? _len - 1 : 0), _key = 1; _key < _len; _key++) {
    args[_key - 1] = arguments[_key];
  }

  for (var i = 0; i < args.length; i++) {
    var rawValue = args[i];
    var value = rawValue;
    if (rawValue && typeof rawValue.toAQL === 'function') {
      query += '' + rawValue.toAQL() + strings[i + 1];
      continue;
    }
    var index = bindVals.indexOf(rawValue);
    var isKnown = index !== -1;
    var name = 'value' + (isKnown ? index : bindVals.length);
    if (rawValue && rawValue.isArangoCollection) {
      name = '@' + name;
      value = rawValue.name;
    }
    if (!isKnown) {
      bindVals.push(rawValue);
      bindVars[name] = value;
    }
    query += '@' + name + strings[i + 1];
  }
  return { query: query, bindVars: bindVars };
}