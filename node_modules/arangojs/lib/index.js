'use strict';

var _database = require('./database');

var _database2 = _interopRequireDefault(_database);

var _aqlQuery = require('./aql-query');

var _aqlQuery2 = _interopRequireDefault(_aqlQuery);

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

module.exports = function () {
  for (var _len = arguments.length, args = Array(_len), _key = 0; _key < _len; _key++) {
    args[_key] = arguments[_key];
  }

  return new (Function.prototype.bind.apply(_database2.default, [null].concat(args)))();
};
module.exports.Database = _database2.default;
module.exports.aqlQuery = module.exports.aql = _aqlQuery2.default;