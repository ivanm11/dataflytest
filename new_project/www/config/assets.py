# STATIC ASSETS
# TYPE = { result: [files] }
# files - list of files to compile, concat, minify (relative to /www directory)

CSS = {
    'public': [
        'less/bootstrap-public',    
        'less/public',
        'less/shared'
    ],
    'admin': [
        'less/bootstrap-admin',    
        'datafly/less/default-admin',
        'less/shared',
        'less/admin'
    ]
}
JS = {
    'public': [
        'js/public',        
        'js/shared'
    ],
    'admin': [
        'datafly/coffee/datafly',
        'datafly/coffee/editor',
        'js/shared',
        'js/admin'
    ]
}