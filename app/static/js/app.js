// Declare app level module which depends on filters, and services
var prodmgmt = angular.module('prodmgmt', ['ngResource', 'ngRoute', 'ui.bootstrap', 'ui.date'])
  .config(['$routeProvider', function ($routeProvider) {
    $routeProvider
      .when('/', {
        templateUrl: 'views/home/home.html',
        access: {restricted: true}
      })
      .when('/login', {
      	templateUrl: 'views/auth/login.html',
      	controller: 'loginController',
      	access: {restricted: false}
      })
      .when('/logout', {
      	controller: 'logoutController',
      	access: {restricted: true}
      })
      .otherwise({redirectTo: '/', restricted: false});
  }]);

prodmgmt.run(function ($rootScope, $location, $route, AuthService) {
  $rootScope.$on('$routeChangeStart', function (event, next, current) {
    if (next.access === undefined) {
        console.log("Restricted attribute not present");
    } else if (next.access.restricted && AuthService.isLoggedIn() === false) {
      $location.path('/login');
      $route.reload();
    }
  });
});
