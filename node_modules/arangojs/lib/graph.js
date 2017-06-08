'use strict';

Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.EdgeCollection = exports.VertexCollection = undefined;

var _extends = Object.assign || function (target) { for (var i = 1; i < arguments.length; i++) { var source = arguments[i]; for (var key in source) { if (Object.prototype.hasOwnProperty.call(source, key)) { target[key] = source[key]; } } } return target; };

var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

var _collection = require('./collection');

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _possibleConstructorReturn(self, call) { if (!self) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return call && (typeof call === "object" || typeof call === "function") ? call : self; }

function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function, not " + typeof superClass); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, enumerable: false, writable: true, configurable: true } }); if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass; }

var GraphVertexCollection = function (_BaseCollection) {
  _inherits(GraphVertexCollection, _BaseCollection);

  function GraphVertexCollection(connection, name, graph) {
    _classCallCheck(this, GraphVertexCollection);

    var _this = _possibleConstructorReturn(this, (GraphVertexCollection.__proto__ || Object.getPrototypeOf(GraphVertexCollection)).call(this, connection, name));

    _this.type = _collection._types.DOCUMENT_COLLECTION;
    _this.graph = graph;
    _this._gharial = _this._api.route('/gharial/' + _this.graph.name + '/vertex');
    return _this;
  }

  _createClass(GraphVertexCollection, [{
    key: '_documentPath',
    value: function _documentPath(documentHandle) {
      return '/document/' + this._documentHandle(documentHandle);
    }
  }, {
    key: 'remove',
    value: function remove(documentHandle, cb) {
      var _connection$promisify = this._connection.promisify(cb),
          promise = _connection$promisify.promise,
          callback = _connection$promisify.callback;

      this._gharial.delete('/' + this._documentHandle(documentHandle), function (err, res) {
        return err ? callback(err) : callback(null, res.body);
      });
      return promise;
    }
  }, {
    key: 'vertex',
    value: function vertex(documentHandle, cb) {
      var _connection$promisify2 = this._connection.promisify(cb),
          promise = _connection$promisify2.promise,
          callback = _connection$promisify2.callback;

      this._gharial.get('/' + this._documentHandle(documentHandle), function (err, res) {
        return err ? callback(err) : callback(null, res.body);
      });
      return promise;
    }
  }, {
    key: 'save',
    value: function save(data, cb) {
      var _connection$promisify3 = this._connection.promisify(cb),
          promise = _connection$promisify3.promise,
          callback = _connection$promisify3.callback;

      this._gharial.post(this.name, data, function (err, res) {
        return err ? callback(err) : callback(null, res.body);
      });
      return promise;
    }
  }]);

  return GraphVertexCollection;
}(_collection._BaseCollection);

var GraphEdgeCollection = function (_EdgeCollection) {
  _inherits(GraphEdgeCollection, _EdgeCollection);

  function GraphEdgeCollection(connection, name, graph) {
    _classCallCheck(this, GraphEdgeCollection);

    var _this2 = _possibleConstructorReturn(this, (GraphEdgeCollection.__proto__ || Object.getPrototypeOf(GraphEdgeCollection)).call(this, connection, name));

    _this2.type = _collection._types.EDGE_COLLECTION;
    _this2.graph = graph;
    _this2._gharial = _this2._api.route('/gharial/' + _this2.graph.name + '/edge');
    return _this2;
  }

  _createClass(GraphEdgeCollection, [{
    key: 'remove',
    value: function remove(documentHandle, cb) {
      var _connection$promisify4 = this._connection.promisify(cb),
          promise = _connection$promisify4.promise,
          callback = _connection$promisify4.callback;

      this._gharial.delete('/' + this._documentHandle(documentHandle), function (err, res) {
        return err ? callback(err) : callback(null, res.body);
      });
      return promise;
    }
  }, {
    key: 'edge',
    value: function edge(documentHandle, cb) {
      var _connection$promisify5 = this._connection.promisify(cb),
          promise = _connection$promisify5.promise,
          callback = _connection$promisify5.callback;

      this._gharial.get('/' + this._documentHandle(documentHandle), function (err, res) {
        return err ? callback(err) : callback(null, res.body);
      });
      return promise;
    }
  }, {
    key: 'save',
    value: function save(data, fromId, toId, cb) {
      if (typeof fromId === 'function') {
        cb = fromId;
        fromId = undefined;
      } else if (fromId) {
        data._from = this._documentHandle(fromId);
        data._to = this._documentHandle(toId);
      }

      var _connection$promisify6 = this._connection.promisify(cb),
          promise = _connection$promisify6.promise,
          callback = _connection$promisify6.callback;

      this._gharial.post(this.name, data, function (err, res) {
        return err ? callback(err) : callback(null, res.body);
      });
      return promise;
    }
  }]);

  return GraphEdgeCollection;
}(_collection.EdgeCollection);

var Graph = function () {
  function Graph(connection, name) {
    _classCallCheck(this, Graph);

    this.name = name;
    this._connection = connection;
    this._api = this._connection.route('/_api');
    this._gharial = this._api.route('/gharial/' + this.name);
  }

  _createClass(Graph, [{
    key: 'get',
    value: function get(cb) {
      var _connection$promisify7 = this._connection.promisify(cb),
          promise = _connection$promisify7.promise,
          callback = _connection$promisify7.callback;

      this._gharial.get(function (err, res) {
        return err ? callback(err) : callback(null, res.body.graph);
      });
      return promise;
    }
  }, {
    key: 'create',
    value: function create(properties, cb) {
      if (typeof properties === 'function') {
        cb = properties;
        properties = undefined;
      }

      var _connection$promisify8 = this._connection.promisify(cb),
          promise = _connection$promisify8.promise,
          callback = _connection$promisify8.callback;

      this._api.post('/gharial', _extends({}, properties, { name: this.name }), function (err, res) {
        return err ? callback(err) : callback(null, res.body.graph);
      });
      return promise;
    }
  }, {
    key: 'drop',
    value: function drop(dropCollections, cb) {
      if (typeof dropCollections === 'function') {
        cb = dropCollections;
        dropCollections = undefined;
      }
      if (typeof dropCollections !== 'boolean') dropCollections = false;

      var _connection$promisify9 = this._connection.promisify(cb),
          promise = _connection$promisify9.promise,
          callback = _connection$promisify9.callback;

      this._gharial.delete({ dropCollections: dropCollections }, function (err, res) {
        return err ? callback(err) : callback(null, res.body);
      });
      return promise;
    }
  }, {
    key: 'vertexCollection',
    value: function vertexCollection(collectionName) {
      return new GraphVertexCollection(this._connection, collectionName, this);
    }
  }, {
    key: 'addVertexCollection',
    value: function addVertexCollection(collectionName, cb) {
      var _connection$promisify10 = this._connection.promisify(cb),
          promise = _connection$promisify10.promise,
          callback = _connection$promisify10.callback;

      this._gharial.post('/vertex', { collection: collectionName }, function (err, res) {
        return err ? callback(err) : callback(null, res.body.graph);
      });
      return promise;
    }
  }, {
    key: 'removeVertexCollection',
    value: function removeVertexCollection(collectionName, dropCollection, cb) {
      if (typeof dropCollection === 'function') {
        cb = dropCollection;
        dropCollection = undefined;
      }

      var _connection$promisify11 = this._connection.promisify(cb),
          promise = _connection$promisify11.promise,
          callback = _connection$promisify11.callback;

      if (typeof dropCollection !== 'boolean') dropCollection = false;
      this._gharial.delete('/vertex/' + collectionName, { dropCollection: dropCollection }, function (err, res) {
        return err ? callback(err) : callback(null, res.body.graph);
      });
      return promise;
    }
  }, {
    key: 'edgeCollection',
    value: function edgeCollection(collectionName) {
      return new GraphEdgeCollection(this._connection, collectionName, this);
    }
  }, {
    key: 'addEdgeDefinition',
    value: function addEdgeDefinition(definition, cb) {
      var _connection$promisify12 = this._connection.promisify(cb),
          promise = _connection$promisify12.promise,
          callback = _connection$promisify12.callback;

      this._gharial.post('/edge', definition, function (err, res) {
        return err ? callback(err) : callback(null, res.body.graph);
      });
      return promise;
    }
  }, {
    key: 'replaceEdgeDefinition',
    value: function replaceEdgeDefinition(definitionName, definition, cb) {
      var _connection$promisify13 = this._connection.promisify(cb),
          promise = _connection$promisify13.promise,
          callback = _connection$promisify13.callback;

      this._gharial.put('/edge/' + definitionName, definition, function (err, res) {
        return err ? callback(err) : callback(null, res.body.graph);
      });
      return promise;
    }
  }, {
    key: 'removeEdgeDefinition',
    value: function removeEdgeDefinition(definitionName, dropCollection, cb) {
      if (typeof dropCollection === 'function') {
        cb = dropCollection;
        dropCollection = undefined;
      }

      var _connection$promisify14 = this._connection.promisify(cb),
          promise = _connection$promisify14.promise,
          callback = _connection$promisify14.callback;

      if (typeof dropCollection !== 'boolean') dropCollection = false;
      this._gharial.delete('edge/' + definitionName, { dropCollection: dropCollection }, function (err, res) {
        return err ? callback(err) : callback(null, res.body.graph);
      });
      return promise;
    }
  }, {
    key: 'traversal',
    value: function traversal(startVertex, opts, cb) {
      if (typeof opts === 'function') {
        cb = opts;
        opts = undefined;
      }

      var _connection$promisify15 = this._connection.promisify(cb),
          promise = _connection$promisify15.promise,
          callback = _connection$promisify15.callback;

      this._api.post('/traversal', _extends({}, opts, { startVertex: startVertex, graphName: this.name }), function (err, res) {
        return err ? callback(err) : callback(null, res.body.result);
      });
      return promise;
    }
  }]);

  return Graph;
}();

exports.default = Graph;
exports.VertexCollection = GraphVertexCollection;
exports.EdgeCollection = GraphEdgeCollection;