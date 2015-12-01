'use strict';

angular.module('prodmgmt')
  .config(['$routeProvider', function ($routeProvider) {
    $routeProvider
      .when('/products', {
        templateUrl: 'views/product/products.html',
        controller: 'ProductController',
        resolve:{
          resolvedProduct: ['Product', function (Product) {
            return Product.query();
          }]
        }
      })
    }]);
