$(document).ready(function() {

    var chapter = 0;
    $('h2').each(function() {
        chapter++;
        $(this).attr('id', 'chapter' + chapter);
    });

});