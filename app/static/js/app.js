// Declare app level module which depends on filters, and services
var prodmgmt = angular.module('prodmgmt', ['ngResource','ngCookies','ngRoute', 'ui.bootstrap', 'ui.date'])
  .config(['$routeProvider', function ($routeProvider) {
    $routeProvider
      .when('/', {
        templateUrl: 'views/home/home.html',
        needLogin: true
      })
      .when('/login', {
      	templateUrl: 'views/auth/login.html',
      	controller: 'loginController',
      	needLogin: false
      })
      .when('/logout', {
      	controller: 'logoutController',
      	needLogin: true
      })
      .otherwise({redirectTo: '/', needLogin: true});
  }]);

prodmgmt.run(function ($rootScope, $location, $route, AuthService) {
  $rootScope.$on('$routeChangeStart', function (event, toState, toParams, fromState, fromParams) {

    if (toState.needLogin && AuthService.isLoggedIn() === false) {
      console.log("Ypou must connect before you access to this url!!");
      event.preventDefault();
      $location.path('/login');
      // $route.reload();
    } 

  });
});
