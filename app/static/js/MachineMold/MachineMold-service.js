'use strict';

angular.module('prodmgmt')
  .factory('MachineMold', ['$resource', function ($resource) {
    return $resource('prodmgmt/Machinemolds/:id', {}, {
      'query': { method: 'GET', isArray: true},
      'get': { method: 'GET'},
      'update': { method: 'PUT'}
    });
  }]);
