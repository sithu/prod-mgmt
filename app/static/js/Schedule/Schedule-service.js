'use strict';

angular.module('prodmgmt')
  .factory('Schedule', ['$resource', function ($resource) {
    return $resource('prodmgmt/Schedules/:id', {}, {
      'query': { method: 'GET', isArray: true},
      'get': { method: 'GET'},
      'update': { method: 'PUT'}
    });
  }]);
