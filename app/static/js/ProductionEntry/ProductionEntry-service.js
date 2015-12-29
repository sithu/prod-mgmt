'use strict';

angular.module('prodmgmt')
  .factory('ProductionEntry', ['$resource', function ($resource) {
    return $resource('prodmgmt/Productionentries/:id', {}, {
      'query': { method: 'GET', isArray: true},
      'get': { method: 'GET'},
      'update': { method: 'PUT'}
    });
  }]);
