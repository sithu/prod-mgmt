'use strict';

angular.module('prodmgmt')
  .config(['$routeProvider', function ($routeProvider) {
    $routeProvider
      .when('/Machinequeues', {
        templateUrl: 'views/MachineQueue/Machinequeues.html',
        controller: 'MachineQueueController',
        resolve:{
          resolvedMachineQueue: ['MachineQueue', function (MachineQueue) {
            return MachineQueue.query();
          }]
        }
      })
    }]);
