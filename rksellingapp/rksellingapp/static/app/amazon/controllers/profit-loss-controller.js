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