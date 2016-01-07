'use strict';

angular.module('prodmgmt')
  .factory('Shift', ['$resource', function ($resource) {
    return $resource('prodmgmt/Shifts/:id', {}, {
      'query': { method: 'GET', isArray: true},
      'get': { method: 'GET'},
      'update': { method: 'PUT'}
    });
  }]);
