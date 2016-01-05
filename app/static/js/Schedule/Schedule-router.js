'use strict';

angular.module('prodmgmt')
  .config(['$routeProvider', function ($routeProvider) {
    $routeProvider
      .when('/Schedules', {
        templateUrl: 'views/Schedule/Schedules.html',
        controller: 'ScheduleController',
        resolve:{
          resolvedSchedule: ['Schedule', function (Schedule) {
            return Schedule.query();
          }]
        }
      })
    }]);
