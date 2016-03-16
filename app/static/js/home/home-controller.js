angular.module('prodmgmt')
.controller('homeController', ['$rootScope', '$scope', '$window', '$location', 'AuthService', 
	function ($rootScope, $scope, $window, $location, AuthService) {
  
  	// FIXME
  	$scope.location = $location;
  	console.log($location.path());
  	
}]);
