Datafly.redactor_buttons = [
    'html',
    'formatting', '|',
    'bold', 'italic', 'link', '|',
    'unorderedlist', 'orderedlist', '|',
    'alignment', '|',
    'indent', 'outdent', '|',
    'image', 'file', 'video'
]

$ () ->

    $('.redactor').redactor(
        buttons: Datafly.redactor_buttons
        imageUpload: '/admin/upload/img'
        fileUpload: '/admin/upload/file'        
        toolbarExternal: '#redactor-toolbar'        
    )

    $('#save').click ->
        data = {}
        $('.redactor').each ->            
            clip = $(this).data('clip')
            html = $(this).redactor('get')
            data[clip] = html
        id = $(this).data('page-id')
        url = "/api/pages/#{ id }"
        $.ajax(
            url: url
            type: 'POST'
            data: data
        )

    $('#cancel').click -> location.reload()