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
