$(document).ready ->   

    $('ul.photos').on 'click', 'button.delete-img', (e) ->
        $(e.currentTarget).parents('li').remove()

    $('#new-photo').click (event) ->
        html = _.template(
            $('#photo-template').html(),
            {
                index: $('ul.photos li').length + 1
            }
        );
        $('ul.photos').append(html).sortable()

    $('#save-gallery').click (event) ->
        title = $('[name=title]').val()
        pics = []
        $('.get-photo').each () ->
            src = $(this).attr('src')
            if ( src.indexOf('static/upload') > 0 )
                pics.push(src)
        if ( title == '' or pics.length == 0 )
            return Datafly.error 'You need to specify title and upload at least one image';
        $.ajax(
            url: '/admin/api/gallery'
            type: 'POST'
            data: JSON.stringify(
                'data':
                    'title': title
                    'desc': $('[name=desc]').val()
                    'pics': pics
                    'id': $('[name=id]').val()
                    'sort': Number($('[name=sort]').val())
                    'category': $('#get-project-category').text()
            )
            dataType: 'json'
            contentType: 'application/json'
        ).done(
            (data) -> $('[name=id]').attr('value', data.id)
        )
        Datafly.notify 'Saved!'