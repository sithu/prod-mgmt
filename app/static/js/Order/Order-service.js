'use strict';

angular.module('prodmgmt')
  .factory('Order', ['$resource', function ($resource) {
    return $resource('prodmgmt/Orders/:id', {}, {
      'query': { method: 'GET', isArray: true},
      'get': { method: 'GET'},
      'update': { method: 'PUT'}
    });
  }]);
