'use strict';

angular.module('prodmgmt')
  .config(['$routeProvider', function ($routeProvider) {
    $routeProvider
      .when('/raw_materials', {
        templateUrl: 'views/raw_material/raw_materials.html',
        controller: 'Raw_materialController',
        resolve:{
          resolvedRaw_material: ['Raw_material', function (Raw_material) {
            return Raw_material.query();
          }]
        }
      })
    }]);
