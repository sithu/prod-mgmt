'use strict';

angular.module('prodmgmt')
  .config(['$routeProvider', function ($routeProvider) {
    $routeProvider
      .when('/Machinemolds', {
        templateUrl: 'views/MachineMold/Machinemolds.html',
        controller: 'MachineMoldController',
        resolve:{
          resolvedMachineMold: ['MachineMold', function (MachineMold) {
            return MachineMold.query();
          }]
        }
      })
    }]);
