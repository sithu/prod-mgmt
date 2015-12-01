'use strict';

angular.module('prodmgmt')
  .factory('Raw_material', ['$resource', function ($resource) {
    return $resource('prodmgmt/raw_materials/:id', {}, {
      'query': { method: 'GET', isArray: true},
      'get': { method: 'GET'},
      'update': { method: 'PUT'}
    });
  }]);
