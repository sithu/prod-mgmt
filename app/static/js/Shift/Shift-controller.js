'use strict';

angular.module('prodmgmt')
  .controller('ShiftController', ['$scope', '$modal', 'resolvedShift', 'Shift',
    function ($scope, $modal, resolvedShift, Shift) {

      $scope.Shifts = resolvedShift;

      $scope.create = function () {
        $scope.clear();
        $scope.open();
      };

      $scope.update = function (id) {
        $scope.Shift = Shift.get({id: id});
        $scope.open(id);
      };

      $scope.delete = function (id) {
        Shift.delete({id: id},
          function () {
            $scope.Shifts = Shift.query();
          });
      };

      $scope.save = function (id) {
        if (id) {
          Shift.update({id: id}, $scope.Shift,
            function () {
              $scope.Shifts = Shift.query();
              $scope.clear();
            });
        } else {
          Shift.save($scope.Shift,
            function () {
              $scope.Shifts = Shift.query();
              $scope.clear();
            });
        }
      };

      $scope.clear = function () {
        $scope.Shift = {
          
          "shift_name": "",
          
          "start_time": "",
          
          "end_time": "",
          
          "id": ""
        };
      };

      $scope.open = function (id) {
        var ShiftSave = $modal.open({
          templateUrl: 'Shift-save.html',
          controller: 'ShiftSaveController',
          resolve: {
            Shift: function () {
              return $scope.Shift;
            }
          }
        });

        ShiftSave.result.then(function (entity) {
          $scope.Shift = entity;
          $scope.save(id);
        });
      };
    }])
  .controller('ShiftSaveController', ['$scope', '$modalInstance', 'Shift',
    function ($scope, $modalInstance, Shift) {
      $scope.Shift = Shift;

      

      $scope.ok = function () {
        $modalInstance.close($scope.Shift);
      };

      $scope.cancel = function () {
        $modalInstance.dismiss('cancel');
      };
    }]);
