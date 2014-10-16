app.controller("chatController", ['$scope', '$http', '$q', '$timeout', function($scope, $http, $q, $timeout) {

    $scope.username = "";
    $scope.isLoggedIn = false;
    $scope.messages = [];
    $scope.messageToSend = "";
    $scope.error = "";

    var timer = null;

    function getDeferedForUrl(url, data) {
        var deferred = $q.defer();
        $http.post(url, data)
            .success(function(response) {
                deferred.resolve(response);
            })
            .error(function(response) {
                deferred.reject(response);
            });
        return deferred.promise;
    }

    function onAjaxError() {
        $scope.error = "Error!";
    }

    function handleError(data) {
        $scope.error = "Error: " + data.error;
    }

    function getMessages() {
        var ajax = getDeferedForUrl('/receive', {'username': $scope.username});
        ajax.then(function(data) {
            if (data.error) {
                handleError(data);
                return;
            }

            for (var i=0; i<data.length; i++)
                $scope.messages.push(data[i]);

            timer = $timeout(getMessages, 1000);
        }, onAjaxError);
    }

    $scope.sendMessage = function(message) {
        if (message == '/logout')
            var ajax = getDeferedForUrl('/logout', {'username': $scope.username});
        else
            var ajax = getDeferedForUrl('/send', {'username': $scope.username, 'message': message});
        ajax.then(function(data) {
            if (data.error) {
                handleError(data);
                return;
            }
            $scope.messageToSend = "";
            if (message == '/logout') {
                $scope.isLoggedIn = false;
                timer.cancel();
            }
        }, onAjaxError);
    };

    $scope.login = function (username) {
        var ajax = getDeferedForUrl('/login', {'username': username});
        ajax.then(function(data) {
            if (data.error) {
                handleError(data);
                $scope.username = '';
                return;
            }
            if(data.status == 'ok') {
                $scope.username = username;
                $scope.isLoggedIn = true;
                getMessages();
            }
        }, onAjaxError);
    }
}]);
