'use strict';

angular.module('prodmgmt')
  .factory('Product', ['$resource', function ($resource) {
    return $resource('prodmgmt/products/:id', {}, {
      'query': { method: 'GET', isArray: true},
      'get': { method: 'GET'},
      'update': { method: 'PUT'}
    });
  }]);
