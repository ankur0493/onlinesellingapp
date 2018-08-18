(function(window, angular, _) {
    'user strict';

    var app = angular.module('sellerapp', [
            'ngResource',
            'ngRoute',
            'ngCookies',
            'ngSanitize',
            'ui.bootstrap',
            'ui.router',
            'sellerapp.amazon',
            // 'sellerapp.authentication',
        ]);

    app.config(function($stateProvider, $urlRouterProvider) {
        $stateProvider
            // .state('index', {
            //     url: '',
            //     templateUrl: 'static/app/templates/login.html',
            //     controller: 'loginController'
            // })
            .state('profit-loss-calculator', {
                url: '',
                templateUrl: 'static/app/amazon/profit-loss.html',
                controller: 'amazonProfitLossController'
            })
    });

})(window, angular, _);
