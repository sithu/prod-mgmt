'use strict';

angular.module('prodmgmt')
  .controller('Raw_materialController', ['$scope', '$modal', 'resolvedRaw_material', 'Raw_material',
    function ($scope, $modal, resolvedRaw_material, Raw_material) {

      $scope.raw_materials = resolvedRaw_material;

      $scope.create = function () {
        $scope.clear();
        $scope.open();
      };

      $scope.update = function (id) {
        $scope.raw_material = Raw_material.get({id: id});
        $scope.open(id);
      };

      $scope.delete = function (id) {
        Raw_material.delete({id: id},
          function () {
            $scope.raw_materials = Raw_material.query();
          });
      };

      $scope.save = function (id) {
        if (id) {
          Raw_material.update({id: id}, $scope.raw_material,
            function () {
              $scope.raw_materials = Raw_material.query();
              $scope.clear();
            });
        } else {
          Raw_material.save($scope.raw_material,
            function () {
              $scope.raw_materials = Raw_material.query();
              $scope.clear();
            });
        }
      };

      $scope.clear = function () {
        $scope.raw_material = {
          
          "name": "",
          
          "weight": "",
          
          "count": "",
          
          "purchase_price": "",
          
          "color": "",
          
          "created_at": "",
          
          "updated_at": "",
          
          "id": ""
        };
      };

      $scope.open = function (id) {
        var raw_materialSave = $modal.open({
          templateUrl: 'raw_material-save.html',
          controller: 'Raw_materialSaveController',
          resolve: {
            raw_material: function () {
              return $scope.raw_material;
            }
          }
        });

        raw_materialSave.result.then(function (entity) {
          $scope.raw_material = entity;
          $scope.save(id);
        });
      };
    }])
  .controller('Raw_materialSaveController', ['$scope', '$modalInstance', 'raw_material',
    function ($scope, $modalInstance, raw_material) {
      $scope.raw_material = raw_material;

      
      $scope.created_atDateOptions = {
        dateFormat: 'yy-mm-dd',
        
        
      };
      $scope.updated_atDateOptions = {
        dateFormat: 'yy-mm-dd',
        
        
      };

      $scope.ok = function () {
        $modalInstance.close($scope.raw_material);
      };

      $scope.cancel = function () {
        $modalInstance.dismiss('cancel');
      };
    }]);
