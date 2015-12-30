'use strict';

angular.module('prodmgmt')
  .controller('ProductionEntryController', ['$scope', '$modal', 'resolvedProductionEntry', 'ProductionEntry',
    function ($scope, $modal, resolvedProductionEntry, ProductionEntry) {

      $scope.Productionentries = resolvedProductionEntry;

      $scope.create = function () {
        $scope.clear();
        $scope.open();
      };

      $scope.update = function (id) {
        $scope.ProductionEntry = ProductionEntry.get({id: id});
        $scope.open(id);
      };

      $scope.delete = function (id) {
        ProductionEntry.delete({id: id},
          function () {
            $scope.Productionentries = ProductionEntry.query();
          });
      };

      $scope.save = function (id) {
        if (id) {
          ProductionEntry.update({id: id}, $scope.ProductionEntry,
            function () {
              $scope.Productionentries = ProductionEntry.query();
              $scope.clear();
            });
        } else {
          ProductionEntry.save($scope.ProductionEntry,
            function () {
              $scope.Productionentries = ProductionEntry.query();
              $scope.clear();
            });
        }
      };

      $scope.clear = function () {
        $scope.ProductionEntry = {
          
          "status": "",
          
          "shift_name": "",
          
          "machine_id": "",
          
          "raw_material_id": "",
          
          "order_id": "",
          
          "team_lead_id": "",
          
          "team_lead_name": "",
          
          "estimated_time_to_finish": "",
          
          "start": "",
          
          "end": "",
          
          "delay": "",
          
          "delay_reason": "",
          
          "planned_quantity": "",
          
          "finished_quantity": "",
          
          "defected_quantity": "",
          
          "id": ""
        };
      };

      $scope.open = function (id) {
        var ProductionEntrySave = $modal.open({
          templateUrl: 'ProductionEntry-save.html',
          controller: 'ProductionEntrySaveController',
          resolve: {
            ProductionEntry: function () {
              return $scope.ProductionEntry;
            }
          }
        });

        ProductionEntrySave.result.then(function (entity) {
          $scope.ProductionEntry = entity;
          $scope.save(id);
        });
      };
    }])
  .controller('ProductionEntrySaveController', ['$scope', '$modalInstance', 'ProductionEntry',
    function ($scope, $modalInstance, ProductionEntry) {
      $scope.ProductionEntry = ProductionEntry;

      
      $scope.startDateOptions = {
        dateFormat: 'yy-mm-dd',
        
        
      };
      $scope.endDateOptions = {
        dateFormat: 'yy-mm-dd',
        
        
      };

      $scope.ok = function () {
        $modalInstance.close($scope.ProductionEntry);
      };

      $scope.cancel = function () {
        $modalInstance.dismiss('cancel');
      };
    }]);
