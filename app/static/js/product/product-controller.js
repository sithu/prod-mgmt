'use strict';

angular.module('prodmgmt')
  .controller('ProductController', ['$scope', '$modal', 'resolvedProduct', 'Product', 'Color',
    function ($scope, $modal, resolvedProduct, Product, Color) {
      $scope.products = resolvedProduct;
      $scope.colors = [];
      
      Color.query().$promise.then(function (data){
        $scope.colors = data;
      });

      $scope.create = function () {
        $scope.clear();
        $scope.open();
      };

      $scope.update = function (id) {
        $scope.colors = Color.query();
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
          console.log($scope.product);
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

          "weight": "",

          "time_to_build": "",

          "selling_price": "",

          "colors": "",

          "raw_material_id": "",

          "num_employee_required": "",

          "mold_id": "",

          "id": ""
        };
      };

      $scope.open = function (id) {
        var productSave = $modal.open({
          templateUrl: (id) ? 'product-edit.html' : 'product-new.html',
          controller: 'ProductSaveController',
          resolve: {
            product: function () {
              return $scope.product;
            },
            colors: function() {
              return $scope.colors;
            }
          }
        });

        productSave.result.then(function (entity) {
          $scope.product = entity;
          $scope.save(id);
        });
      };
    }])
  .controller('ProductSaveController', ['$scope', '$modalInstance', 'product', 'colors',
    function ($scope, $modalInstance, product, colors) {
      $scope.product = product;
      $scope.colors = colors;
      //$scope.product.raw_material_id = raw_materials.length ? raw_materials[0].id : -1;
      
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
