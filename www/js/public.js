
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
            data: bodyval,
        })
            .fail(function(){
                $('#ajaxtest-form').html("Adding blog record failed");
            })
            .success(function(){
                $('#ajaxtest-form').html("Successfully added");
            })
        //$('#ajaxtest-form').html('<p>No-no-no!</p>')
    });

});
