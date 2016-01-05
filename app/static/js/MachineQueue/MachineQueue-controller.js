'use strict';

angular.module('prodmgmt')
  .controller('MachineQueueController', ['$scope', '$modal', 'resolvedMachineQueue', 'MachineQueue',
    function ($scope, $modal, resolvedMachineQueue, MachineQueue) {

      $scope.Machinequeues = resolvedMachineQueue;

      $scope.create = function () {
        $scope.clear();
        $scope.open();
      };

      $scope.update = function (id) {
        $scope.MachineQueue = MachineQueue.get({id: id});
        $scope.open(id);
      };

      $scope.delete = function (id) {
        MachineQueue.delete({id: id},
          function () {
            $scope.Machinequeues = MachineQueue.query();
          });
      };

      $scope.save = function (id) {
        if (id) {
          MachineQueue.update({id: id}, $scope.MachineQueue,
            function () {
              $scope.Machinequeues = MachineQueue.query();
              $scope.clear();
            });
        } else {
          MachineQueue.save($scope.MachineQueue,
            function () {
              $scope.Machinequeues = MachineQueue.query();
              $scope.clear();
            });
        }
      };

      $scope.clear = function () {
        $scope.MachineQueue = {
          
          "machine_id": "",
          
          "work_in_progress": "",
          
          "slot_1": "",
          
          "slot_2": "",
          
          "slot_3": "",
          
          "slot_4": "",
          
          "slot_5": "",
          
          "id": ""
        };
      };

      $scope.open = function (id) {
        var MachineQueueSave = $modal.open({
          templateUrl: 'MachineQueue-save.html',
          controller: 'MachineQueueSaveController',
          resolve: {
            MachineQueue: function () {
              return $scope.MachineQueue;
            }
          }
        });

        MachineQueueSave.result.then(function (entity) {
          $scope.MachineQueue = entity;
          $scope.save(id);
        });
      };
    }])
  .controller('MachineQueueSaveController', ['$scope', '$modalInstance', 'MachineQueue',
    function ($scope, $modalInstance, MachineQueue) {
      $scope.MachineQueue = MachineQueue;

      

      $scope.ok = function () {
        $modalInstance.close($scope.MachineQueue);
      };

      $scope.cancel = function () {
        $modalInstance.dismiss('cancel');
      };
    }]);
