'use strict';

angular.module('prodmgmt')
  .config(['$routeProvider', function ($routeProvider) {
    $routeProvider
      .when('/Machines', {
        templateUrl: 'views/Machine/Machines.html',
        controller: 'MachineController',
        resolve:{
          resolvedMachine: ['Machine', function (Machine) {
            return Machine.query();
          }]
        }
      })
    }]);
