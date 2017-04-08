( function () {
    var app = angular.module("mainPageApp", ["xeditable"])  // "ngResource", "ngCookie",
        .config(function ($interpolateProvider) {
            $interpolateProvider.startSymbol('{$');
            $interpolateProvider.endSymbol('$}');
    });

    app.run(function (editableOptions) {
        editableOptions.theme = 'bs3'; // bootstrap3 theme. Can be also 'bs2', 'default'
        console.log("--inside album_id get--");
    });

    app.controller("ConfGenCtrl", function ($scope, $http) { 
    	console.log("--inside album_id get--");
    }); 	
})();
