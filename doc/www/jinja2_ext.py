import markdown2

def markdown_html(value):
    markdowner = markdown2.Markdown(
        extras = ['code-friendly', 'fenced_code', 'fenced-code-blocks']
    )
    return markdowner.convert(value)

extended_filters = dict(
    markdown = markdown_html
)

extended_globals = dict()