Datafly.redactor_buttons = [
    'formatting', '|',
    'bold', 'italic', 'link', '|',
    'unorderedlist', 'orderedlist', '|',
    'alignment', '|',
    'indent', 'outdent', 'table', '|',
    'image', 'file', 'video',
    'html'
]

$ () ->

    $('.dropdown-toggle').dropdown()

    $('#versions a').click ->
        v = $(this).text()
        id = $(this).data('id')
        $.ajax(
            url: """/admin/api/pages/#{id}/version"""
            type: 'GET'
        ).done((data) ->
            $('[data-clip]').each ->               
                clip = $(this).data('clip')
                html = data[clip]
                $(this).redactor('set', html)
        )        
        Datafly.notify """Loaded from #{v}"""

    $('[data-clip]').each ->
        clip = $(this).data('clip')
        $('.toolbar-redactor').append(
            """<div id="toolbar-#{clip}"></div>"""
        )
        $(this).redactor(
            buttons: Datafly.redactor_buttons
            imageUpload: '/admin/upload/img'
            fileUpload: '/admin/upload/file'
            imageUploadCallback: (image, json) ->
                console.log(image)
                console.log(json)        
            toolbarExternal: "#toolbar-#{clip}"
            plugins: ['externalswitcher']
        )

    # focus top redactor
    $('[data-clip]').first().redactor 'focus'

    $('#save').click ->
        page =
            meta: $('form#meta').serializeObject()                
        $('[data-clip]').each ->            
            clip = $(this).data('clip')
            html = $(this).redactor('get')
            page[clip] = html
        page['id'] = id = $(this).data('page-id')
        url = "/admin/api/pages/id/#{ id }"
        $.ajax(
            url: url
            type: 'POST'
            data: JSON.stringify(
                page: page
            ),
            dataType: 'json',
            contentType: 'application/json'
        )
        Datafly.notify 'New version published!'

    $('#cancel').click -> location.reload()