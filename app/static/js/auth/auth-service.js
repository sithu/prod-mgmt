angular.module('prodmgmt').factory('AuthService',
  ['$q', '$timeout', '$http', '$window',
  function ($q, $timeout, $http, $window) {

    // create user variable
    var user = null;

    // return available functions for use in controllers
    return ({
      isLoggedIn: isLoggedIn,
      login: login,
      logout: logout,
      register: register
    });

  function isLoggedIn() {
    if(user) {
      return true;
    } else {
      return false;
    }
  }

  function login(email, password) {

    // create a new instance of deferred
    var deferred = $q.defer();

    // send a post request to the server
    $http.post('/api/login', {email: email, password: password})
      // handle success
      .success(function (data, status) {
        if(status === 200 && data.result){
          user = true;
          $window.sessionStorage["userInfo"] = JSON.stringify(data);
          deferred.resolve();
        } else {
          user = false;
          deferred.reject();
        }
      })
      // handle error
      .error(function (data) {
        user = false;
        deferred.reject();
      });

    // return promise object
    return deferred.promise;

  }

  function logout() {

    // create a new instance of deferred
    var deferred = $q.defer();

    // send a get request to the server
    $http.get('/api/logout')
      // handle success
      .success(function (data) {
        $window.sessionStorage["userInfo"] = null;
        user = false;
        deferred.resolve();
      })
      // handle error
      .error(function (data) {
        $window.sessionStorage["userInfo"] = null;
        user = false;
        deferred.reject();
      });

    // return promise object
    return deferred.promise;

  }

  function register(email, password) {

    // create a new instance of deferred
    var deferred = $q.defer();

    // send a post request to the server
    $http.post('/api/register', {email: email, password: password})
      // handle success
      .success(function (data, status) {
        if(status === 200 && data.result){
          deferred.resolve();
        } else {
          deferred.reject();
        }
      })
      // handle error
      .error(function (data) {
        deferred.reject();
      });

    // return promise object
    return deferred.promise;

  }

  // FIXME: this is NOT working yet!
  function init() {
    if ($window.sessionStorage["userInfo"]) {
      var userInfo = JSON.parse($window.sessionStorage["userInfo"]);
      if (userInfo) {
        user = userInfo.result;
      }
    } 
  }
  
  init();


}]);