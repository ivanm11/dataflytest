# STATIC ASSETS
# TYPE = { result: [files] }
# files - list of files to compile, concat, minify (relative to /www directory)

LESS = {
    'public': [
        'less/layout',    
        'less/pages',
        'less/responsive'      
    ],
    'admin': [
        'datafly/admin/layout',
        'less/pages',
        'less/admin'
    ]
}
JS = {
    'public': [
        'js/layout',        
        'js/pages',
    ],
    'admin': [
        'static/can-1.1.16/can.control',
        'datafly/widgets/ajax',
        'datafly/pages/redactor',
        'datafly/users/login',
        'js/admin',
    ]
}