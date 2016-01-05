'use strict';

angular.module('prodmgmt')
  .factory('MachineQueue', ['$resource', function ($resource) {
    return $resource('prodmgmt/Machinequeues/:id', {}, {
      'query': { method: 'GET', isArray: true},
      'get': { method: 'GET'},
      'update': { method: 'PUT'}
    });
  }]);
