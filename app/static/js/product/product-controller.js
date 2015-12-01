'use strict';

angular.module('prodmgmt')
  .controller('ProductController', ['$scope', '$modal', 'resolvedProduct', 'Product',
    function ($scope, $modal, resolvedProduct, Product) {

      $scope.products = resolvedProduct;

      $scope.create = function () {
        $scope.clear();
        $scope.open();
      };

      $scope.update = function (id) {
        $scope.product = Product.get({id: id});
        $scope.open(id);
      };

      $scope.delete = function (id) {
        Product.delete({id: id},
          function () {
            $scope.products = Product.query();
          });
      };

      $scope.save = function (id) {
        if (id) {
          Product.update({id: id}, $scope.product,
            function () {
              $scope.products = Product.query();
              $scope.clear();
            });
        } else {
          Product.save($scope.product,
            function () {
              $scope.products = Product.query();
              $scope.clear();
            });
        }
      };

      $scope.clear = function () {
        $scope.product = {
          
          "name": "",
          
          "type": "",
          
          "weight": "",
          
          "time_to_build": "",
          
          "selling_price": "",
          
          "color": "",
          
          "created_at": "",
          
          "updated_at": "",
          
          "id": ""
        };
      };

      $scope.open = function (id) {
        var productSave = $modal.open({
          templateUrl: 'product-save.html',
          controller: 'ProductSaveController',
          resolve: {
            product: function () {
              return $scope.product;
            }
          }
        });

        productSave.result.then(function (entity) {
          $scope.product = entity;
          $scope.save(id);
        });
      };
    }])
  .controller('ProductSaveController', ['$scope', '$modalInstance', 'product',
    function ($scope, $modalInstance, product) {
      $scope.product = product;

      
      $scope.created_atDateOptions = {
        dateFormat: 'yy-mm-dd',
        
        
      };
      $scope.updated_atDateOptions = {
        dateFormat: 'yy-mm-dd',
        
        
      };

      $scope.ok = function () {
        $modalInstance.close($scope.product);
      };

      $scope.cancel = function () {
        $modalInstance.dismiss('cancel');
      };
    }]);
