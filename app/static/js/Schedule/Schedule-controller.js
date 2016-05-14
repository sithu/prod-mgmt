'use strict';

angular.module('prodmgmt')
  .controller('ScheduleController', ['$scope', '$modal', 'resolvedSchedule', 'Schedule',
    function ($scope, $modal, resolvedSchedule, Schedule) {

      $scope.Schedules = resolvedSchedule;

      $scope.create = function () {
        $scope.clear();
        $scope.createSchedule();
      };

      $scope.update = function (id) {
        $scope.Schedule = Schedule.get({id: id});
        $scope.open(id);
      };

      $scope.delete = function (id) {
        Schedule.delete({id: id},
          function () {
            $scope.Schedules = Schedule.query();
          });
      };

      $scope.save = function (id) {
        if (id) {
          Schedule.update({id: id}, $scope.Schedule,
            function () {
              $scope.Schedules = Schedule.query();
              $scope.clear();
            });
        } else {
          Schedule.save($scope.Schedule,
            function () {
              $scope.Schedules = Schedule.query();
              $scope.clear();
            });
        }
      };

      $scope.clear = function () {
        $scope.Schedule = {
          
          "date": "",
          
          "shift_name": "",
          
          "employee_id": "",
          
          "manager_id": "",
          
          "is_in_duty": "",
          
          "assigned_machine": "",
          
          "sign_in_at": "",
          
          "sign_out_at": "",
          
          "id": ""
        };
      };

      $scope.open = function (id) {
        var ScheduleSave = $modal.open({
          templateUrl: 'Schedule-save.html',
          controller: 'ScheduleSaveController',
          resolve: {
            Schedule: function () {
              return $scope.Schedule;
            }
          }
        });

        ScheduleSave.result.then(function (entity) {
          $scope.Schedule = entity;
          $scope.save(id);
        });
      };
      // new schedule
      $scope.createSchedule = function (id) {
        var ScheduleCreate = $modal.open({
          templateUrl: 'New-Schedule.html',
          controller: 'ScheduleSaveController',
          resolve: {
            Schedule: function () {
              return $scope.Schedule;
            }
          }
        });

        ScheduleCreate.result.then(function (entity) {
          $scope.Schedule = entity;
          $scope.save(id);
        });
      };

    }])
  .controller('ScheduleSaveController', ['$scope', '$modalInstance', 'Schedule',
    function ($scope, $modalInstance, Schedule) {
      $scope.Schedule = Schedule;

      
      $scope.dateDateOptions = {
        dateFormat: 'yy-mm-dd',
        
        
      };
      $scope.sign_in_atDateOptions = {
        dateFormat: 'yy-mm-dd',
        
        
      };
      $scope.sign_out_atDateOptions = {
        dateFormat: 'yy-mm-dd',
        
        
      };

      $scope.ok = function () {
        $modalInstance.close($scope.Schedule);
      };

      $scope.cancel = function () {
        $modalInstance.dismiss('cancel');
      };
    }]);
