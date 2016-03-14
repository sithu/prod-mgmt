'use strict';

angular.module('prodmgmt')
  .controller('ProductController', ['$scope', '$modal', 'resolvedProduct', 'Product', 'Raw_material',
    function ($scope, $modal, resolvedProduct, Product, Raw_material) {
      $scope.products = resolvedProduct;
      $scope.raw_materials = [];
      
      Raw_material.query().$promise.then(function (data){
        $scope.raw_materials = data;
      });

      $scope.create = function () {
        $scope.clear();
        $scope.open();
      };

      $scope.update = function (id) {
        $scope.raw_materials = Raw_material.query();
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

          "type": "",

          "weight": "",

          "time_to_build": "",

          "selling_price": "",

          "color": "",

          "raw_material_id": 0,

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
            },
            raw_materials: function() {
              return $scope.raw_materials;
            }
          }
        });

        productSave.result.then(function (entity) {
          $scope.product = entity;
          $scope.save(id);
        });
      };
    }])
  .controller('ProductSaveController', ['$scope', '$modalInstance', 'product', 'raw_materials',
    function ($scope, $modalInstance, product, raw_materials) {
      $scope.product = product;
      $scope.raw_materials = raw_materials;
      $scope.product.raw_material_id = raw_materials.length ? raw_materials[0].id : -1;
      
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
