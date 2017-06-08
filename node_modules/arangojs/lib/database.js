'use strict';

Object.defineProperty(exports, "__esModule", {
  value: true
});

var _extends = Object.assign || function (target) { for (var i = 1; i < arguments.length; i++) { var source = arguments[i]; for (var key in source) { if (Object.prototype.hasOwnProperty.call(source, key)) { target[key] = source[key]; } } } return target; };

var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

var _all = require('./util/all');

var _all2 = _interopRequireDefault(_all);

var _btoa = require('./util/btoa');

var _btoa2 = _interopRequireDefault(_btoa);

var _multipart = require('./util/multipart');

var _multipart2 = _interopRequireDefault(_multipart);

var _connection = require('./connection');

var _connection2 = _interopRequireDefault(_connection);

var _cursor = require('./cursor');

var _cursor2 = _interopRequireDefault(_cursor);

var _graph = require('./graph');

var _graph2 = _interopRequireDefault(_graph);

var _collection = require('./collection');

var _collection2 = _interopRequireDefault(_collection);

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

function _objectWithoutProperties(obj, keys) { var target = {}; for (var i in obj) { if (keys.indexOf(i) >= 0) continue; if (!Object.prototype.hasOwnProperty.call(obj, i)) continue; target[i] = obj[i]; } return target; }

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

var Database = function () {
  function Database(config) {
    _classCallCheck(this, Database);

    this._connection = new _connection2.default(config);
    this._api = this._connection.route('/_api');
    this.name = this._connection.config.databaseName;
  }

  _createClass(Database, [{
    key: 'route',
    value: function route(path, headers) {
      return this._connection.route(path, headers);
    }

    // Database manipulation

  }, {
    key: 'useDatabase',
    value: function useDatabase(databaseName) {
      if (this._connection.config.databaseName === false) {
        throw new Error('Can not change database from absolute URL');
      }
      this._connection.config.databaseName = databaseName;
      this._connection._databasePath = '/_db/' + databaseName;
      this.name = databaseName;
      return this;
    }
  }, {
    key: 'useBearerAuth',
    value: function useBearerAuth(token) {
      this._connection.config.headers['authorization'] = 'Bearer ' + token;
      return this;
    }
  }, {
    key: 'useBasicAuth',
    value: function useBasicAuth(username, password) {
      this._connection.config.headers['authorization'] = 'Basic ' + (0, _btoa2.default)((username || 'root') + ':' + (password || ''));
      return this;
    }
  }, {
    key: 'get',
    value: function get(cb) {
      var _connection$promisify = this._connection.promisify(cb),
          promise = _connection$promisify.promise,
          callback = _connection$promisify.callback;

      this._api.get('/database/current', function (err, res) {
        return err ? callback(err) : callback(null, res.body.result);
      });
      return promise;
    }
  }, {
    key: 'createDatabase',
    value: function createDatabase(databaseName, users, cb) {
      if (typeof users === 'function') {
        cb = users;
        users = undefined;
      }

      var _connection$promisify2 = this._connection.promisify(cb),
          promise = _connection$promisify2.promise,
          callback = _connection$promisify2.callback;

      this._api.post('/database', { users: users, name: databaseName }, function (err, res) {
        return err ? callback(err) : callback(null, res.body);
      });
      return promise;
    }
  }, {
    key: 'listDatabases',
    value: function listDatabases(cb) {
      var _connection$promisify3 = this._connection.promisify(cb),
          promise = _connection$promisify3.promise,
          callback = _connection$promisify3.callback;

      this._api.get('/database', function (err, res) {
        return err ? callback(err) : callback(null, res.body.result);
      });
      return promise;
    }
  }, {
    key: 'listUserDatabases',
    value: function listUserDatabases(cb) {
      var _connection$promisify4 = this._connection.promisify(cb),
          promise = _connection$promisify4.promise,
          callback = _connection$promisify4.callback;

      this._api.get('/database/user', function (err, res) {
        return err ? callback(err) : callback(null, res.body.result);
      });
      return promise;
    }
  }, {
    key: 'dropDatabase',
    value: function dropDatabase(databaseName, cb) {
      var _connection$promisify5 = this._connection.promisify(cb),
          promise = _connection$promisify5.promise,
          callback = _connection$promisify5.callback;

      this._api.delete('/database/' + databaseName, function (err, res) {
        return err ? callback(err) : callback(null, res.body);
      });
      return promise;
    }

    // Collection manipulation

  }, {
    key: 'collection',
    value: function collection(collectionName) {
      return new _collection.DocumentCollection(this._connection, collectionName);
    }
  }, {
    key: 'edgeCollection',
    value: function edgeCollection(collectionName) {
      return new _collection.EdgeCollection(this._connection, collectionName);
    }
  }, {
    key: 'listCollections',
    value: function listCollections(excludeSystem, cb) {
      if (typeof excludeSystem === 'function') {
        cb = excludeSystem;
        excludeSystem = undefined;
      }

      var _connection$promisify6 = this._connection.promisify(cb),
          promise = _connection$promisify6.promise,
          callback = _connection$promisify6.callback;

      if (typeof excludeSystem !== 'boolean') excludeSystem = true;
      var resultField = this._connection.arangoMajor < 3 ? 'collections' : 'result';
      this._api.get('/collection', { excludeSystem: excludeSystem }, function (err, res) {
        return err ? callback(err) : callback(null, res.body[resultField]);
      });
      return promise;
    }
  }, {
    key: 'collections',
    value: function collections(excludeSystem, cb) {
      var _this = this;

      if (typeof excludeSystem === 'function') {
        cb = excludeSystem;
        excludeSystem = undefined;
      }

      var _connection$promisify7 = this._connection.promisify(cb),
          promise = _connection$promisify7.promise,
          callback = _connection$promisify7.callback;

      this.listCollections(excludeSystem, function (err, collections) {
        return err ? callback(err) : callback(null, collections.map(function (info) {
          return (0, _collection2.default)(_this._connection, info);
        }));
      });
      return promise;
    }
  }, {
    key: 'truncate',
    value: function truncate(excludeSystem, cb) {
      var _this2 = this;

      if (typeof excludeSystem === 'function') {
        cb = excludeSystem;
        excludeSystem = undefined;
      }

      var _connection$promisify8 = this._connection.promisify(cb),
          promise = _connection$promisify8.promise,
          callback = _connection$promisify8.callback;

      this.listCollections(excludeSystem, function (err, collections) {
        return err ? callback(err) : (0, _all2.default)(collections.map(function (data) {
          return function (cb) {
            return _this2._api.put('/collection/' + data.name + '/truncate', function (err, res) {
              return err ? cb(err) : cb(null, res.body);
            });
          };
        }), callback);
      });
      return promise;
    }

    // Graph manipulation

  }, {
    key: 'graph',
    value: function graph(graphName) {
      return new _graph2.default(this._connection, graphName);
    }
  }, {
    key: 'listGraphs',
    value: function listGraphs(cb) {
      var _connection$promisify9 = this._connection.promisify(cb),
          promise = _connection$promisify9.promise,
          callback = _connection$promisify9.callback;

      this._api.get('/gharial', function (err, res) {
        return err ? callback(err) : callback(null, res.body.graphs);
      });
      return promise;
    }
  }, {
    key: 'graphs',
    value: function graphs(cb) {
      var _this3 = this;

      var _connection$promisify10 = this._connection.promisify(cb),
          promise = _connection$promisify10.promise,
          callback = _connection$promisify10.callback;

      this.listGraphs(function (err, graphs) {
        return err ? callback(err) : callback(null, graphs.map(function (info) {
          return _this3.graph(info._key);
        }));
      });
      return promise;
    }

    // Queries

  }, {
    key: 'transaction',
    value: function transaction(collections, action, params, lockTimeout, cb) {
      if (typeof lockTimeout === 'function') {
        cb = lockTimeout;
        lockTimeout = undefined;
      }
      if (typeof params === 'function') {
        cb = params;
        params = undefined;
      }
      if (typeof params === 'number') {
        lockTimeout = params;
        params = undefined;
      }
      if (typeof collections === 'string' || Array.isArray(collections)) {
        collections = { write: collections };
      }

      var _connection$promisify11 = this._connection.promisify(cb),
          promise = _connection$promisify11.promise,
          callback = _connection$promisify11.callback;

      this._api.post('/transaction', { collections: collections, action: action, params: params, lockTimeout: lockTimeout }, function (err, res) {
        return err ? callback(err) : callback(null, res.body.result);
      });
      return promise;
    }
  }, {
    key: 'query',
    value: function query(_query, bindVars, opts, cb) {
      var _this4 = this;

      if (typeof opts === 'function') {
        cb = opts;
        opts = undefined;
      }
      if (typeof bindVars === 'function') {
        cb = bindVars;
        bindVars = undefined;
      }

      var _connection$promisify12 = this._connection.promisify(cb),
          promise = _connection$promisify12.promise,
          callback = _connection$promisify12.callback;

      if (_query && _query.query) {
        if (!opts) opts = bindVars;
        bindVars = _query.bindVars;
        _query = _query.query;
      }
      if (_query && typeof _query.toAQL === 'function') {
        _query = _query.toAQL();
      }
      this._api.post('/cursor', _extends({}, opts, { query: _query, bindVars: bindVars }), function (err, res) {
        return err ? callback(err) : callback(null, new _cursor2.default(_this4._connection, res.body));
      });
      return promise;
    }

    // Function management

  }, {
    key: 'listFunctions',
    value: function listFunctions(cb) {
      var _connection$promisify13 = this._connection.promisify(cb),
          promise = _connection$promisify13.promise,
          callback = _connection$promisify13.callback;

      this._api.get('/aqlfunction', function (err, res) {
        return err ? callback(err) : callback(null, res.body);
      });
      return promise;
    }
  }, {
    key: 'createFunction',
    value: function createFunction(name, code, cb) {
      var _connection$promisify14 = this._connection.promisify(cb),
          promise = _connection$promisify14.promise,
          callback = _connection$promisify14.callback;

      this._api.post('/aqlfunction', { name: name, code: code }, function (err, res) {
        return err ? callback(err) : callback(null, res.body);
      });
      return promise;
    }
  }, {
    key: 'dropFunction',
    value: function dropFunction(name, group, cb) {
      if (typeof group === 'function') {
        cb = group;
        group = undefined;
      }

      var _connection$promisify15 = this._connection.promisify(cb),
          promise = _connection$promisify15.promise,
          callback = _connection$promisify15.callback;

      this._api.delete('/aqlfunction/' + name, { group: Boolean(group) }, function (err, res) {
        return err ? callback(err) : callback(null, res.body);
      });
      return promise;
    }

    // Service management

  }, {
    key: 'listServices',
    value: function listServices(cb) {
      var _connection$promisify16 = this._connection.promisify(cb),
          promise = _connection$promisify16.promise,
          callback = _connection$promisify16.callback;

      this._api.get('/foxx', function (err, res) {
        return err ? callback(err) : callback(null, res.body);
      });
      return promise;
    }
  }, {
    key: 'installService',
    value: function installService(mount, source, opts, cb) {
      var _this5 = this;

      if (typeof opts === 'function') {
        cb = opts;
        opts = undefined;
      }

      var _ref = opts || {},
          configuration = _ref.configuration,
          dependencies = _ref.dependencies,
          qs = _objectWithoutProperties(_ref, ['configuration', 'dependencies']);

      var _connection$promisify17 = this._connection.promisify(cb),
          promise = _connection$promisify17.promise,
          callback = _connection$promisify17.callback;

      (0, _multipart2.default)({
        configuration: configuration,
        dependencies: dependencies,
        source: source
      }, function (err, req) {
        return err ? callback(err) : _this5._api.request({
          method: 'POST',
          path: '/foxx',
          rawBody: req.body,
          qs: _extends({}, qs, { mount: mount }),
          headers: req.headers
        }, function (err, res) {
          return err ? callback(err) : callback(null, res.body);
        });
      });
      return promise;
    }
  }, {
    key: 'upgradeService',
    value: function upgradeService(mount, source, opts, cb) {
      var _this6 = this;

      if (typeof opts === 'function') {
        cb = opts;
        opts = undefined;
      }

      var _ref2 = opts || {},
          configuration = _ref2.configuration,
          dependencies = _ref2.dependencies,
          qs = _objectWithoutProperties(_ref2, ['configuration', 'dependencies']);

      var _connection$promisify18 = this._connection.promisify(cb),
          promise = _connection$promisify18.promise,
          callback = _connection$promisify18.callback;

      (0, _multipart2.default)({
        configuration: configuration,
        dependencies: dependencies,
        source: source
      }, function (err, req) {
        return err ? callback(err) : _this6._api.request({
          method: 'PATCH',
          path: '/foxx/service',
          rawBody: req.body,
          qs: _extends({}, qs, { mount: mount }),
          headers: req.headers
        }, function (err, res) {
          return err ? callback(err) : callback(null, res.body);
        });
      });
      return promise;
    }
  }, {
    key: 'replaceService',
    value: function replaceService(mount, source, opts, cb) {
      var _this7 = this;

      if (typeof opts === 'function') {
        cb = opts;
        opts = undefined;
      }

      var _ref3 = opts || {},
          configuration = _ref3.configuration,
          dependencies = _ref3.dependencies,
          qs = _objectWithoutProperties(_ref3, ['configuration', 'dependencies']);

      var _connection$promisify19 = this._connection.promisify(cb),
          promise = _connection$promisify19.promise,
          callback = _connection$promisify19.callback;

      (0, _multipart2.default)({
        configuration: configuration,
        dependencies: dependencies,
        source: source
      }, function (err, req) {
        return err ? callback(err) : _this7._api.request({
          method: 'PUT',
          path: '/foxx/service',
          rawBody: req.body,
          qs: _extends({}, qs, { mount: mount }),
          headers: req.headers
        }, function (err, res) {
          return err ? callback(err) : callback(null, res.body);
        });
      });
      return promise;
    }
  }, {
    key: 'uninstallService',
    value: function uninstallService(mount, opts, cb) {
      if (typeof opts === 'function') {
        cb = opts;
        opts = undefined;
      }

      var _connection$promisify20 = this._connection.promisify(cb),
          promise = _connection$promisify20.promise,
          callback = _connection$promisify20.callback;

      this._api.delete('/foxx/service', _extends({}, opts, { mount: mount }), function (err) {
        return err ? callback(err) : callback(null);
      });
      return promise;
    }
  }, {
    key: 'getService',
    value: function getService(mount, cb) {
      var _connection$promisify21 = this._connection.promisify(cb),
          promise = _connection$promisify21.promise,
          callback = _connection$promisify21.callback;

      this._api.get('/foxx/service', { mount: mount }, function (err, res) {
        return err ? callback(err) : callback(null, res.body);
      });
      return promise;
    }
  }, {
    key: 'getServiceConfiguration',
    value: function getServiceConfiguration(mount, cb) {
      var _connection$promisify22 = this._connection.promisify(cb),
          promise = _connection$promisify22.promise,
          callback = _connection$promisify22.callback;

      this._api.get('/foxx/configuration', { mount: mount }, function (err, res) {
        return err ? callback(err) : callback(null, res.body);
      });
      return promise;
    }
  }, {
    key: 'updateServiceConfiguration',
    value: function updateServiceConfiguration(mount, cfg, cb) {
      var _connection$promisify23 = this._connection.promisify(cb),
          promise = _connection$promisify23.promise,
          callback = _connection$promisify23.callback;

      this._api.patch('/foxx/configuration', cfg, { mount: mount }, function (err, res) {
        return err ? callback(err) : callback(null, res.body);
      });
      return promise;
    }
  }, {
    key: 'replaceServiceConfiguration',
    value: function replaceServiceConfiguration(mount, cfg, cb) {
      var _connection$promisify24 = this._connection.promisify(cb),
          promise = _connection$promisify24.promise,
          callback = _connection$promisify24.callback;

      this._api.put('/foxx/configuration', cfg, { mount: mount }, function (err, res) {
        return err ? callback(err) : callback(null, res.body);
      });
      return promise;
    }
  }, {
    key: 'getServiceDependencies',
    value: function getServiceDependencies(mount, cb) {
      var _connection$promisify25 = this._connection.promisify(cb),
          promise = _connection$promisify25.promise,
          callback = _connection$promisify25.callback;

      this._api.get('/foxx/dependencies', { mount: mount }, function (err, res) {
        return err ? callback(err) : callback(null, res.body);
      });
      return promise;
    }
  }, {
    key: 'updateServiceDependencies',
    value: function updateServiceDependencies(mount, cfg, cb) {
      var _connection$promisify26 = this._connection.promisify(cb),
          promise = _connection$promisify26.promise,
          callback = _connection$promisify26.callback;

      this._api.patch('/foxx/dependencies', cfg, { mount: mount }, function (err, res) {
        return err ? callback(err) : callback(null, res.body);
      });
      return promise;
    }
  }, {
    key: 'replaceServiceDependencies',
    value: function replaceServiceDependencies(mount, cfg, cb) {
      var _connection$promisify27 = this._connection.promisify(cb),
          promise = _connection$promisify27.promise,
          callback = _connection$promisify27.callback;

      this._api.put('/foxx/dependencies', cfg, { mount: mount }, function (err, res) {
        return err ? callback(err) : callback(null, res.body);
      });
      return promise;
    }
  }, {
    key: 'enableServiceDevelopmentMode',
    value: function enableServiceDevelopmentMode(mount, cb) {
      var _connection$promisify28 = this._connection.promisify(cb),
          promise = _connection$promisify28.promise,
          callback = _connection$promisify28.callback;

      this._api.post('/foxx/development', undefined, { mount: mount }, function (err, res) {
        return err ? callback(err) : callback(null, res.body);
      });
      return promise;
    }
  }, {
    key: 'disableServiceDevelopmentMode',
    value: function disableServiceDevelopmentMode(mount, cb) {
      var _connection$promisify29 = this._connection.promisify(cb),
          promise = _connection$promisify29.promise,
          callback = _connection$promisify29.callback;

      this._api.delete('/foxx/development', { mount: mount }, function (err, res) {
        return err ? callback(err) : callback(null, res.body);
      });
      return promise;
    }
  }, {
    key: 'listServiceScripts',
    value: function listServiceScripts(mount, cb) {
      var _connection$promisify30 = this._connection.promisify(cb),
          promise = _connection$promisify30.promise,
          callback = _connection$promisify30.callback;

      this._api.get('/foxx/scripts', { mount: mount }, function (err, res) {
        return err ? callback(err) : callback(null, res.body);
      });
      return promise;
    }
  }, {
    key: 'runServiceScript',
    value: function runServiceScript(mount, name, args, cb) {
      if (typeof args === 'function') {
        cb = args;
        args = undefined;
      }

      var _connection$promisify31 = this._connection.promisify(cb),
          promise = _connection$promisify31.promise,
          callback = _connection$promisify31.callback;

      this._api.post('/foxx/scripts/' + name, args, { mount: mount }, function (err, res) {
        return err ? callback(err) : callback(null, res.body);
      });
      return promise;
    }
  }, {
    key: 'runServiceTests',
    value: function runServiceTests(mount, opts, cb) {
      if (typeof opts === 'function') {
        cb = opts;
        opts = undefined;
      }

      var _connection$promisify32 = this._connection.promisify(cb),
          promise = _connection$promisify32.promise,
          callback = _connection$promisify32.callback;

      this._api.post('/foxx/tests', undefined, _extends({}, opts, { mount: mount }), function (err, res) {
        return err ? callback(err) : callback(null, res.body);
      });
      return promise;
    }
  }, {
    key: 'getServiceReadme',
    value: function getServiceReadme(mount, cb) {
      var _connection$promisify33 = this._connection.promisify(cb),
          promise = _connection$promisify33.promise,
          callback = _connection$promisify33.callback;

      this._api.get('/foxx/readme', { mount: mount }, function (err, res) {
        return err ? callback(err) : callback(null, res.body);
      });
      return promise;
    }
  }, {
    key: 'downloadService',
    value: function downloadService(mount, cb) {
      var _connection$promisify34 = this._connection.promisify(cb),
          promise = _connection$promisify34.promise,
          callback = _connection$promisify34.callback;

      this._api.request({ method: 'POST', path: '/foxx/download', qs: { mount: mount }, expectBinary: true }, function (err, res) {
        return err ? callback(err) : callback(null, res.body);
      });
      return promise;
    }
  }]);

  return Database;
}();

exports.default = Database;