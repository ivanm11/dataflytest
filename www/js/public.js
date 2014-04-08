
$(document).ready(function () {

    // JavaScript for public facing pages
    
    $('.carousel').carousel({
        interval: 5000
    })

    $('#contact-form button').click(function(event) {
        $('#contact-form').html('<p>Thank You!</p>')
    });

    $('#ajaxtest-form button').click(function(event) {
        var action = $('#ajaxtest-form').attr('action');
        var bodyval = $('.form-control').val();

        $.ajax({
            type:"POST",
            url:action,
            data: bodyval
        })
            .fail(function(){
                $('#ajaxtest-form').html("Adding blog record failed");
            })
            .success(function(){
                $('#ajaxtest-form').html("Successfully added");
            })
        //$('#ajaxtest-form').html('<p>No-no-no!</p>')
    });


/*    $.fn.serializeObject = function()
    {
        var o = {};
        var a = this.serializeArray();
        $.each(a, function() {
            if (o[this.name] !== undefined) {
                if (!o[this.name].push) {
                    o[this.name] = [o[this.name]];
                }
                o[this.name].push(this.value || '');
            } else {
                o[this.name] = this.value || '';
            }
        });
        return o;
    };
*/

$.fn.serializeObject = function() {
  var values;
  values = this.serializeArray();
  return _.chain(values).map(function(el) {
    return [el.name, el.value];
  }).object().value();
};


    $(document).on('click', '#comment-submit-button', function(event) {
        // Check what text on this button is.
        // If Send, then create new
        // If Edit, then edit existing
        console.log($(this).html())
        if ($('#comment-body').val() == '')
        {
            alert('null value')
            return false
        }
        if ($(this).html() == 'Send Comment')
        {
            var action = $('#comments-form').attr('action');
            var body = $('#comment-body').val();
            comment = $('form#comments-form')
            console.log($('form#comments-form').serializeObject())
            $.ajax({
                    url: action,
                    type: 'POST',
                    data: $('form#comments-form').serializeObject()
                }
            )
                .fail(function(){
                    $('#ajaxtest-form').html("Adding blog record failed");
                })
                .done(function(data){
                    $('section.comments').prepend(data);
                    $('#comment-body').val('');
                })
        }
        else if($(this).html() == 'Edit Comment')
        {

            var action = $('#comments-form').attr('action');
            var body = $('#comment-body').val();
            comment = $('form#comments-form')
            console.log($('form#comments-form').serializeObject())
            $.ajax({
                    url: action,
                    type: 'POST',
                    data: $('form#comments-form').serializeObject()
                }
            )
                .fail(function(){
                    $('#ajaxtest-form').html("Adding blog record failed");
                })
                .done(function(data){
                    $('#comments-form').attr('action', '/comments/page/create');
                    $('#comment-submit-button').html('Send Comment');
                    $('#comment-body').val('');
                    $('div.block-white[data-comment-id=\"' + $('#comments-form').attr('data-comment-id') + '\"]').children('.comment-text').html(data);
                    $('#comments-form').removeAttr('data-comment-id');
                    $('#comment-back-button').hide();
//                    $('section.comments').prepend(data); //Rewrite this, as this edits existing comment
                })
        }
        else
        {
            return false
        }
        //$('#ajaxtest-form').html('<p>No-no-no!</p>')
    });

    $(document).on('click', 'a.edit-button', function(event) {

        $('#comment-body').val($(this).parent('div').children('div.comment-text').html());
        $('#comment-submit-button').html('Edit Comment');
        $('#comments-form').attr('action', $(this).attr('href'));
        $('#comments-form').attr('data-comment-id', $(this).parent('.block-white').attr('data-comment-id'));
        $('#comment-back-button').show();
        return false
        //$('#ajaxtest-form').html('<p>No-no-no!</p>')
    });

    $(document).on('click', 'a.delete-button', function(event) {
        var link = $(this)
        $.ajax({
                    url: $(this).attr('href'),
                    type: 'GET'
                }
            )
                .done(function(data){
                    link.closest('article').remove();
//                    $('section.comments').prepend(data); //Rewrite this, as this edits existing comment
                })
        return false
        //$('#ajaxtest-form').html('<p>No-no-no!</p>')
    });

    $(document).on('click', '#comment-back-button', function(event) {
        $('#comment-submit-button').html('Send Comment');
        $('#comment-body').val('');
        $('#comments-form').attr('action', '/comments/page/create');
        $('#comments-form').removeAttr('data-comment-id');
        $('#comment-back-button').hide();
    });
});
