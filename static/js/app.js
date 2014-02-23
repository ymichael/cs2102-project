var app = angular.module('app', []);

app.config(function($interpolateProvider) {
    $interpolateProvider.startSymbol('{[{');
    $interpolateProvider.endSymbol('}]}');

});

app.controller(
    'ListingsController',
    ['$scope', '$http',
        function($scope, $http) {
            $http.get('/listings').success(function(data) {
                $scope.listings = data
            });
        }
    ]
);
