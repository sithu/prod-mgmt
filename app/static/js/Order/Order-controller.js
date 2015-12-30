'use strict';

angular.module('prodmgmt')
  .controller('OrderController', ['$scope', '$modal', 'resolvedOrder', 'Order',
    function ($scope, $modal, resolvedOrder, Order) {

      $scope.Orders = resolvedOrder;

      $scope.create = function () {
        $scope.clear();
        $scope.open();
      };

      $scope.update = function (id) {
        $scope.Order = Order.get({id: id});
        $scope.open(id);
      };

      $scope.delete = function (id) {
        Order.delete({id: id},
          function () {
            $scope.Orders = Order.query();
          });
      };

      $scope.save = function (id) {
        if (id) {
          Order.update({id: id}, $scope.Order,
            function () {
              $scope.Orders = Order.query();
              $scope.clear();
            });
        } else {
          Order.save($scope.Order,
            function () {
              $scope.Orders = Order.query();
              $scope.clear();
            });
        }
      };

      $scope.clear = function () {
        $scope.Order = {

          "id": "",

          "status": "",

          "product_id": "",

          "quantity": "",

          "raw_material_quantity": "",

          "created_at": "",

          "estimated_time_to_finish": "",

          "production_start_at": "",

          "production_end_at": "",

          "note": "",

        };
      };

      $scope.open = function (id) {
        var OrderSave = $modal.open({
          templateUrl: 'Order-save.html',
          controller: 'OrderSaveController',
          resolve: {
            Order: function () {
              return $scope.Order;
            }
          }
        });

        OrderSave.result.then(function (entity) {
          $scope.Order = entity;
          $scope.save(id);
        });
      };
    }])
  .controller('OrderSaveController', ['$scope', '$modalInstance', 'Order',
    function ($scope, $modalInstance, Order) {
      $scope.Order = Order;


      $scope.created_atDateOptions = {
        dateFormat: 'yy-mm-dd',
        maxDate: -1

      };
      $scope.production_start_atDateOptions = {
        dateFormat: 'yy-mm-dd',


      };
      $scope.production_end_atDateOptions = {
        dateFormat: 'yy-mm-dd',


      };

      $scope.ok = function () {
        $modalInstance.close($scope.Order);
      };

      $scope.cancel = function () {
        $modalInstance.dismiss('cancel');
      };
    }]);
