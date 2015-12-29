'use strict';

angular.module('prodmgmt')
  .config(['$routeProvider', function ($routeProvider) {
    $routeProvider
      .when('/Productionentries', {
        templateUrl: 'views/ProductionEntry/Productionentries.html',
        controller: 'ProductionEntryController',
        resolve:{
          resolvedProductionEntry: ['ProductionEntry', function (ProductionEntry) {
            return ProductionEntry.query();
          }]
        }
      })
    }]);
