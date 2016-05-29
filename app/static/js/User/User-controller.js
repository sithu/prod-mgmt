'use strict';

angular.module('prodmgmt')
  .controller('UserController', ['$scope', '$modal', 'resolvedUser', 'User',
    function ($scope, $modal, resolvedUser, User) {

      $scope.Users = resolvedUser;

      $scope.create = function () {
        $scope.clear();
        $scope.open();
      };

      $scope.update = function (id) {
        $scope.User = User.get({id: id});
        $scope.open(id);
      };

      $scope.delete = function (id) {
        User.delete({id: id},
          function () {
            $scope.Users = User.query();
          });
      };

      $scope.save = function (id) {
        if (id) {
          User.update({id: id}, $scope.User,
            function () {
              $scope.Users = User.query();
              $scope.clear();
            });
        } else {
          User.save($scope.User,
            function () {
              $scope.Users = User.query();
              $scope.clear();
            });
        }
      };

      $scope.clear = function () {
        $scope.User = {
          
          "name": "",
          
          "email": "",
          
          "phone": "",
          
          "password_hash": "",
          
          "level": "",

          "gender": "",

          "shift_name": "",
          
          "salary": "",
          
          "department": "",
          
          "status": "",
          
          "start_date": "",
          
          "end_date": "",
          
          "profile_photo_url": "",
          
          "last_login_at": "",
          
          "modified_at": "",
          
          "id": ""
        };
      };

      $scope.open = function (id) {
        var UserSave = $modal.open({
          templateUrl: 'User-save.html',
          controller: 'UserSaveController',
          resolve: {
            User: function () {
              return $scope.User;
            }
          }
        });

        UserSave.result.then(function (entity) {
          if (entity && !entity.end_date) {
            entity.end_date = "";
          }
          $scope.User = entity;
          $scope.save(id);
        });
      };
    }])
  .controller('UserSaveController', ['$scope', '$modalInstance', 'User',
    function ($scope, $modalInstance, User) {
      $scope.User = User;

      
      $scope.start_dateDateOptions = {
        dateFormat: 'yy-mm-dd',
        
        
      };
      $scope.end_dateDateOptions = {
        dateFormat: 'yy-mm-dd',
        
        
      };
      $scope.last_login_atDateOptions = {
        dateFormat: 'yy-mm-dd',
        
        
      };
      $scope.modified_atDateOptions = {
        dateFormat: 'yy-mm-dd',
        
        
      };

      $scope.ok = function () {
        $modalInstance.close($scope.User);
      };

      $scope.cancel = function () {
        $modalInstance.dismiss('cancel');
      };
    }]);
