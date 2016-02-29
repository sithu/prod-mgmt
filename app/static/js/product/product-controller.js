'use strict';

angular.module('prodmgmt')
  .controller('ProductController', ['$scope', '$modal', 'resolvedProduct', 'Product', 'Raw_material',
    function ($scope, $modal, resolvedProduct, Product, Raw_material) {

      $scope.products = resolvedProduct;
      $scope.raw_materials = [];
      $scope.selected_raw_material = null;

      $scope.create = function () {
        // load all raw materials to select
        $scope.clear();
//        Raw_material.query().$promise.then(function (data){
//            $scope.raw_materials = data;
//            console.log($scope.raw_materials);
//        });
        $scope.raw_materials = Raw_material.query() || 'abc'
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
