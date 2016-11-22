'use strict';

angular.module('prodmgmt')
  .factory('Color', ['$resource', function ($resource) {
    return $resource('prodmgmt/Colors/:id', {}, {
      'query': { method: 'GET', isArray: true},
      'get': { method: 'GET'},
      'update': { method: 'PUT'}
    });
  }]);
