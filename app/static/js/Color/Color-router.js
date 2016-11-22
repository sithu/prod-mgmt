'use strict';

angular.module('prodmgmt')
  .config(['$routeProvider', function ($routeProvider) {
    $routeProvider
      .when('/Colors', {
        templateUrl: 'views/Color/Colors.html',
        controller: 'ColorController',
        resolve:{
          resolvedColor: ['Color', function (Color) {
            return Color.query();
          }]
        }
      })
    }]);
