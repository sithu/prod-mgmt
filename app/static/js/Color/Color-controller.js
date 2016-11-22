'use strict';

angular.module('prodmgmt')
  .controller('ColorController', ['$scope', '$modal', 'resolvedColor', 'Color',
    function ($scope, $modal, resolvedColor, Color) {

      $scope.Colors = resolvedColor;

      $scope.create = function () {
        $scope.clear();
        $scope.open();
      };

      $scope.update = function (id) {
        $scope.Color = Color.get({id: id});
        $scope.open(id);
      };

      $scope.delete = function (id) {
        Color.delete({id: id},
          function () {
            $scope.Colors = Color.query();
          });
      };

      $scope.save = function (id) {
        if (id) {
          Color.update({id: id}, $scope.Color,
            function () {
              $scope.Colors = Color.query();
              $scope.clear();
            });
        } else {
          Color.save($scope.Color,
            function () {
              $scope.Colors = Color.query();
              $scope.clear();
            });
        }
      };

      $scope.clear = function () {
        $scope.Color = {
          
          "id": "",
          
          "name": "",
          
          "created_at": "",
          
          "updated_at": ""
          
        };
      };

      $scope.open = function (id) {
        var ColorSave = $modal.open({
          templateUrl: (id) ? 'Color-save.html' : 'Color-new.html',
          controller: 'ColorSaveController',
          resolve: {
            Color: function () {
              return $scope.Color;
            }
          }
        });

        ColorSave.result.then(function (entity) {
          $scope.Color = entity;
          $scope.save(id);
        });
      };
    }])
  .controller('ColorSaveController', ['$scope', '$modalInstance', 'Color',
    function ($scope, $modalInstance, Color) {
      $scope.Color = Color;

      
      $scope.created_atDateOptions = {
        dateFormat: 'yy-mm-dd',
        
        
      };
      $scope.updated_atDateOptions = {
        dateFormat: 'yy-mm-dd',
        
        
      };

      $scope.ok = function () {
        $modalInstance.close($scope.Color);
      };

      $scope.cancel = function () {
        $modalInstance.dismiss('cancel');
      };
    }]);
