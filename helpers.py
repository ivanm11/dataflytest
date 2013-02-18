from fabric.api import local

def replace_in_file(path, replacements):
    source = open(path).read()
    for key, value in replacements.iteritems():
        var = '{{ $%s }}' % key
        source = source.replace(var, str(value))
    output = open(path, 'w')
    output.write(source)
    output.close

def rename_and_replace_in_file(source, target, replacements):
    local('mv %s %s' % (source, target))
    replace_in_file(target, replacements)