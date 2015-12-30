'use strict';

angular.module('prodmgmt')
  .config(['$routeProvider', function ($routeProvider) {
    $routeProvider
      .when('/Orders', {
        templateUrl: 'views/Order/Orders.html',
        controller: 'OrderController',
        resolve:{
          resolvedOrder: ['Order', function (Order) {
            return Order.query();
          }]
        }
      })
    }]);
