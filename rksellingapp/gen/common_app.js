(function(window, angular, _) {
    'user strict';

    var app = angular.module('sellerapp', [
            'ngResource',
            'ngRoute',
            'ngCookies',
            'ngSanitize',
            'ui.bootstrap',
            'ui.router',
            'sellerapp.amazon'
        ]);

    app.config(function($stateProvider, $urlRouterProvider) {
        $stateProvider
            .state('index', {
                url: '',
                templateUrl: 'static/app/amazon/profit-loss.html',
                controller: 'amazonProfitLossController'
            })
    });

})(window, angular, _);

(function(){
    'use strict';

    // fsr Module
    angular.module('sellerapp.amazon', [
        'sellerapp.amazon.controllers'
    ]);
})();

(function(){
    'use strict';

    // operations Controllers Module
    angular.module('sellerapp.amazon.controllers', []);
})();
(function(){
    'use strict';

    angular.module('sellerapp.amazon.controllers')
        .controller('amazonProfitLossController', [
            '$scope',
            '$http',
            function($scope, $http) {
                $scope.amazonFormData = {};

                $scope.submitAmazonForm = function() {
                    $http.post('amazon/profit-loss/', $scope.amazonFormData)
                    .then(function(response) {
                        $scope.amazonFormData = response.data;
                        },function(error) {
                    });
                };

                $scope.resetAmazonForm = function() {
                    $scope.amazonFormData = {};
                }
            }
        ]);
})();