'use strict';

angular.module('prodmgmt')
  .config(['$routeProvider', function ($routeProvider) {
    $routeProvider
      .when('/Shifts', {
        templateUrl: 'views/Shift/Shifts.html',
        controller: 'ShiftController',
        resolve:{
          resolvedShift: ['Shift', function (Shift) {
            return Shift.query();
          }]
        }
      })
    }]);
