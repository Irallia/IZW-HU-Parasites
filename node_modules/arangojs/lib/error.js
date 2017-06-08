'use strict';

Object.defineProperty(exports, "__esModule", {
  value: true
});

var _es6Error = require('es6-error');

var _es6Error2 = _interopRequireDefault(_es6Error);

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _possibleConstructorReturn(self, call) { if (!self) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return call && (typeof call === "object" || typeof call === "function") ? call : self; }

function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function, not " + typeof superClass); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, enumerable: false, writable: true, configurable: true } }); if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass; }

var ArangoError = function (_ExtendableError) {
  _inherits(ArangoError, _ExtendableError);

  function ArangoError(obj) {
    _classCallCheck(this, ArangoError);

    var _this = _possibleConstructorReturn(this, (ArangoError.__proto__ || Object.getPrototypeOf(ArangoError)).call(this));

    _this.message = obj.errorMessage;
    _this.errorNum = obj.errorNum;
    _this.code = obj.code;
    var err = new Error(_this.message);
    err.name = _this.name;
    if (err.fileName) _this.fileName = err.fileName;
    if (err.lineNumber) _this.lineNumber = err.lineNumber;
    if (err.columnNumber) _this.columnNumber = err.columnNumber;
    if (err.stack) _this.stack = err.stack;
    if (err.description) _this.description = err.description;
    if (err.number) _this.number = err.number;
    return _this;
  }

  return ArangoError;
}(_es6Error2.default);

exports.default = ArangoError;


ArangoError.prototype.name = 'ArangoError';
ArangoError.prototype.isArangoError = true;