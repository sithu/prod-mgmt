'use strict';

angular.module('prodmgmt')
  .factory('User', ['$resource', function ($resource) {
    return $resource('prodmgmt/Users/:id', {}, {
      'query': { method: 'GET', isArray: true},
      'get': { method: 'GET'},
      'update': { method: 'PUT'}
    });
  }]);
