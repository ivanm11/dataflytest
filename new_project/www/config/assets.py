# STATIC ASSETS
# TYPE = { result: [files] }
# files - list of files to compile, concat, minify (relative to /www directory)

CSS = {
    'public': [
        'css/bootstrap-public',    
        'css/public',
        'css/shared'
    ],
    'admin': [
        'css/bootstrap-admin',    
        'datafly/css/layout',
        'css/shared',
        'css/admin'
    ]
}
JS = {
    'public': [
        'js/public',        
        'js/shared'
    ],
    'admin': [
        'static/can-1.1.16/can.control',
        'datafly/js/ajax',
        'datafly/js/redactor',
        'datafly/js/login',
        'js/shared',
        'js/admin'
    ]
}