'use strict';

angular.module('prodmgmt')
  .controller('MachineMoldController', ['$scope', '$modal', 'resolvedMachineMold', 'MachineMold',
    function ($scope, $modal, resolvedMachineMold, MachineMold) {

      $scope.Machinemolds = resolvedMachineMold;

      $scope.create = function () {
        $scope.clear();
        $scope.open();
      };

      $scope.update = function (id) {
        $scope.MachineMold = MachineMold.get({id: id});
        $scope.open(id);
      };

      $scope.delete = function (id) {
        MachineMold.delete({id: id},
          function () {
            $scope.Machinemolds = MachineMold.query();
          });
      };

      $scope.save = function (id) {
        if (id) {
          MachineMold.update({id: id}, $scope.MachineMold,
            function () {
              $scope.Machinemolds = MachineMold.query();
              $scope.clear();
            });
        } else {
          MachineMold.save($scope.MachineMold,
            function () {
              $scope.Machinemolds = MachineMold.query();
              $scope.clear();
            });
        }
      };

      $scope.clear = function () {
        $scope.MachineMold = {
          
          "mold_type": "",
          
          "time_to_install": "",
          
          "created_at": "",
          
          "modified_at": "",
          
          "id": ""
        };
      };

      $scope.open = function (id) {
        var MachineMoldSave = $modal.open({
          templateUrl: 'MachineMold-save.html',
          controller: 'MachineMoldSaveController',
          resolve: {
            MachineMold: function () {
              return $scope.MachineMold;
            }
          }
        });

        MachineMoldSave.result.then(function (entity) {
          $scope.MachineMold = entity;
          $scope.save(id);
        });
      };
    }])
  .controller('MachineMoldSaveController', ['$scope', '$modalInstance', 'MachineMold',
    function ($scope, $modalInstance, MachineMold) {
      $scope.MachineMold = MachineMold;

      
      $scope.created_atDateOptions = {
        dateFormat: 'yy-mm-dd',
        
        
      };
      $scope.modified_atDateOptions = {
        dateFormat: 'yy-mm-dd',
        
        
      };

      $scope.ok = function () {
        $modalInstance.close($scope.MachineMold);
      };

      $scope.cancel = function () {
        $modalInstance.dismiss('cancel');
      };
    }]);
