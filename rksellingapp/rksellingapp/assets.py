from django_assets import Bundle, register

NM = 'lib/node_modules/'


css_common = Bundle(
    NM + 'angular-ui-bootstrap/dist/ui-bootstrap-csp.css',
    NM + 'bootstrap/dist/css/bootstrap.min.css',

    output='gen/common.css',
    )

register('css_common', css_common)

js_common_libraries = Bundle(
    NM + 'jquery/dist/jquery.min.js',
    NM + 'bootstrap/dist/js/bootstrap.min.js',
    NM + 'angular/angular.js',
    NM + 'angular-resource/angular-resource.min.js',
    NM + 'angular-route/angular-route.min.js',
    NM + 'angular-ui-router/build/angular-ui-router.min.js',
    NM + 'angular-ui-bootstrap/dist/ui-bootstrap-tpls.js',
    NM + 'angular-cookies/angular-cookies.min.js',
    NM + 'angular-sanitize/angular-sanitize.min.js',
    NM + 'angular-storage/dist/angular-storage.min.js',
    NM + 'angular-ui-bootstrap/dist/ui-bootstrap.js',
    NM + 'lodash/index.js',

    # filters='jsmin',
    output='gen/common_external.js'
    )

register('js_common_libraries', js_common_libraries)

js_common_app = Bundle(
    'app/app.js',
    'app/amazon/index.js',
    'app/amazon/controllers/index.js',
    'app/amazon/services/index.js',
    'app/amazon/controllers/profit-loss-controller.js',

    'app/authentication/index.js',
    'app/authentication/controllers/index.js',
    'app/authentication/services/index.js',
    'app/authentication/controllers/login-controller.js',

    output='gen/common_app.js')

register('js_common_app', js_common_app)
