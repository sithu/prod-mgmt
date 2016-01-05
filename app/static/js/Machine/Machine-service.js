'use strict';

angular.module('prodmgmt')
  .factory('Machine', ['$resource', function ($resource) {
    return $resource('prodmgmt/Machines/:id', {}, {
      'query': { method: 'GET', isArray: true},
      'get': { method: 'GET'},
      'update': { method: 'PUT'}
    });
  }]);
