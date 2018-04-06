(function(){
    'use strict';

    angular.module('sellerapp.amazon.controllers')
        .controller('amazonProfitLossController', [
            '$scope',
            '$http',
            function($scope, $http) {
                $scope.amazonFormData = {};
                $scope.amazonFormData.region = 'National';

                $scope.submitAmazonForm = function() {
                    var formData = $scope.amazonFormData;
                    if(!(formData.product_name && formData.purchase_price_with_gst && formData.weight && formData.region && formData.list_price)) {
                        alert("Please fill all fields marked with *")
                    }
                    $http.post('amazon/profit-loss/', $scope.amazonFormData)
                    .then(function(response) {
                        $scope.amazonFormData = response.data;
                        },function(error) {
                            // console.log(error);
                    });
                };

                $scope.resetAmazonForm = function() {
                    $scope.amazonFormData = {};
                }
            }
        ]);
})();