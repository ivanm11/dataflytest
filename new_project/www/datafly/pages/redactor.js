// Generated by CoffeeScript 1.6.3
Datafly.redactor_buttons = ['formatting', '|', 'bold', 'italic', 'link', '|', 'unorderedlist', 'orderedlist', '|', 'alignment', '|', 'indent', 'outdent', 'table', '|', 'image', 'file', 'video', 'html'];

$(function() {
  $('.dropdown-toggle').dropdown();
  $('#versions a').click(function() {
    var id, v;
    v = $(this).text();
    id = $(this).data('id');
    $.ajax({
      url: "/admin/api/pages/" + id + "/version",
      type: 'GET'
    }).done(function(data) {
      return $('[data-clip]').each(function() {
        var clip, html;
        clip = $(this).data('clip');
        html = data[clip];
        return $(this).redactor('set', html);
      });
    });
    return Datafly.notify("Loaded from " + v);
  });
  $('[data-clip]').each(function() {
    var clip;
    clip = $(this).data('clip');
    $('.toolbar-redactor').append("<div id=\"toolbar-" + clip + "\"></div>");
    return $(this).redactor({
      buttons: Datafly.redactor_buttons,
      imageUpload: '/admin/upload/img',
      fileUpload: '/admin/upload/file',
      imageUploadCallback: function(image, json) {
        console.log(image);
        return console.log(json);
      },
      toolbarExternal: "#toolbar-" + clip,
      plugins: ['externalswitcher']
    });
  });
  $('[data-clip]').first().redactor('focus');
  $('#save').click(function() {
    var id, page, url;
    page = {
      meta: $('form#meta').serializeObject()
    };
    $('[data-clip]').each(function() {
      var clip, html;
      clip = $(this).data('clip');
      html = $(this).redactor('get');
      return page[clip] = html;
    });
    page['id'] = id = $(this).data('page-id');
    url = "/admin/api/pages/id/" + id;
    $.ajax({
      url: url,
      type: 'POST',
      data: JSON.stringify({
        page: page
      }),
      dataType: 'json',
      contentType: 'application/json'
    });
    return Datafly.notify('New version published!');
  });
  return $('#cancel').click(function() {
    return location.reload();
  });
});
