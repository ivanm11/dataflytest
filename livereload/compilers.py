def compile_less(files, output):
    from functools import partial
    def task(files, output):
        from livereload.compiler import BaseCompiler, lessc
        less_concat = 'static/production/%s.less' % output
        less_output = 'static/production/%s.css' % output
        for i, less_file in enumerate(files):
            base = BaseCompiler(less_file)
            if i == 0:
                base.write(less_concat)
            else:
                base.append(less_concat)
        lessc(less_concat, less_output)()
    return partial(task, files, output)

def compile_js(files, output):
    from functools import partial
    def task(files, output):
        from livereload.compiler import BaseCompiler
        output = 'static/production/%s.js' % output
        for i, js_file in enumerate(files):
            base = BaseCompiler(js_file)
            if i == 0:
                base.write(output)
            else:
                base.append(output)
    return partial(task, files, output)