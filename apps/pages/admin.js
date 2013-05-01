Datafly.alert = function(msg){
    $('#alert').html('<p>' + msg + '</p>');
    $('#alert').show(0).delay(5000).hide(0);
}

Datafly.redactor_buttons = [
    'html',
    'formatting', '|',
    'bold', 'italic', 'link', '|',
    'unorderedlist', 'orderedlist', '|',
    'alignment', '|',
    'indent', 'outdent', '|',
    'image', 'video'
]

_.templateSettings = {
    interpolate : /\{\{(.+?)\}\}/g
};

$(document).ready(function(){

    if (! $('#redactor').length )
        return;

    $('#redactor').redactor({
        imageUpload: '/admin/pages/upload',
        fileUpload: '/admin/pages/upload',
        autoresize: false,
        buttons: Datafly.redactor_buttons
    });

    $('#versions').change(function() {
        var url = $(this).data('url'),
            version = $(this).val();
        if (version === 'current') {
            location.href = url;
        } else {
            location.href = url + '?v=' + version;
        }
    })

    $('#save').click(function(){
        var textarea = $('#redactor'),
            title = $('input[name=title]');
        // save changes
        $.post(textarea.data('post-to'), {
            'html': textarea.val(),
            'title': title.val()
        }, function(data) {
            var option = _.template('<option value="{{ id }}">{{ datetime }}</option>');
            $('#versions option.current').after(option(data));
            $('#versions option.current').prop('selected', true);
            $('header h2').text(title.val());
        });
        // show alert
        Datafly.alert('All changes are saved');
    });

});