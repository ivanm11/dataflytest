// Generated by CoffeeScript 1.6.3
Datafly.redactor_buttons = ['formatting', '|', 'bold', 'italic', 'link', '|', 'unorderedlist', 'orderedlist', '|', 'alignment', '|', 'indent', 'outdent', 'table', '|', 'image', 'file', 'video', 'html'];

$(function() {
  $('.dropdown-toggle').dropdown();
  $('#versions a').click(function() {
    var id, v;
    $('#versions li').removeClass('active');
    $(this).parent('li').addClass('active');
    v = $(this).text();
    id = $(this).data('id');
    $.ajax({
      url: "/admin/api/pages/" + id + "/version",
      type: 'GET'
    }).done(function(data) {
      return $('[data-clip]').each(function() {
        var clip, html, src;
        clip = $(this).attr('data-clip');
        if ($(this).is('img')) {
          src = data.img[clip];
          return $(this).attr('src', src);
        } else {
          html = data[clip];
          return $(this).redactor('set', html);
        }
      });
    });
    return Datafly.notify("Loaded from " + v);
  });
  $('div[data-clip]').each(function() {
    var clip;
    clip = $(this).data('clip');
    $('.toolbar-redactor').append("<div id=\"toolbar-" + clip + "\"></div>");
    return $(this).redactor({
      buttons: Datafly.redactor_buttons,
      imageUpload: '/admin/upload/img',
      fileUpload: '/admin/upload/file',
      toolbarExternal: "#toolbar-" + clip,
      plugins: ['externalswitcher']
    });
  });
  $('div[data-clip]').first().redactor('focus');
  $('#save').click(function() {
    var id, page, url, valid;
    valid = true;
    $('form#meta [data-required]').each(function() {
      var label;
      label = $(this).prev('label');
      if ($(this).val() === '') {
        label.css('color', 'red');
        return valid = false;
      } else {
        return label.css('color', '#aaa');
      }
    });
    if (!valid) {
      return Datafly.error('Please fill all required fields.');
    }
    page = {
      img: {},
      meta: $('form#meta').serializeObject()
    };
    $('[data-clip]').each(function() {
      var clip, html, src;
      clip = $(this).data('clip');
      if ($(this).is('img')) {
        src = $(this).attr('src');
        return page.img[clip] = src;
      } else {
        html = $(this).redactor('get');
        return page[clip] = html;
      }
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
      contentType: 'application/json',
      success: function(res) {
        return $('#save').data('page-id', res.id);
      }
    });
    return Datafly.notify('New version published!');
  });
  $('#hidden-upload-redactor').redactor({
    buttons: Datafly.redactor_buttons,
    imageUpload: '/admin/upload/img',
    fileUpload: '/admin/upload/file',
    imageUploadCallback: function(image, json) {
      var replaceImage;
      replaceImage = $("[data-clip=" + Datafly.replaceImage + "]");
      return replaceImage.attr('src', json.filelink);
    }
  });
  return $('.content').on('click', 'img[data-clip]', function(event) {
    var crop, fitHeight, fitWidth, img, options;
    img = $(event.currentTarget);
    Datafly.replaceImage = img.attr('data-clip');
    options = $('#hidden-upload-redactor').redactor('getObject').opts;
    options.imageUpload = "/admin/upload/img";
    fitWidth = img.data('fit-width');
    fitHeight = img.data('fit-height');
    crop = img.data('crop') || 'yes';
    if (fitWidth && fitHeight) {
      options.imageUpload = options.imageUpload + ("?width=" + fitWidth + "&height=" + fitHeight + "&crop=" + crop);
    }
    return $('#hidden-upload .redactor_btn_image').click();
  });
});
