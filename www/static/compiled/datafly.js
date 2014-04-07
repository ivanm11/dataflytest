// Generated by CoffeeScript 1.6.3
$.fn.serializeObject = function() {
  var values;
  values = this.serializeArray();
  return _.chain(values).map(function(el) {
    return [el.name, el.value];
  }).object().value();
};

Datafly.alert = function(el) {
  return $('#alert' + el).removeClass('hidden').slideDown('slow').delay(6000).slideUp('slow');
};

Datafly.notify = function(msg) {
  return $('.center').notify({
    message: {
      text: msg
    }
  }).show();
};

Datafly.error = function(msg) {
  return $('.center').notify({
    type: 'danger',
    message: {
      text: msg
    }
  }).show();
};

Datafly.submit = function(event) {
  var $form, redirect, reload, success;
  event.preventDefault();
  $form = $(this).parents('form');
  reload = $(this).data('reload');
  redirect = $(this).data('redirect');
  success = $(this).data('success');
  return $.ajax({
    url: $form.attr('action'),
    type: 'POST',
    data: $form.serialize()
  }).done(function(data) {
    success = success || data.success;
    if (reload) {
      return window.location.reload();
    } else if (success) {
      return Datafly.alert(success);
    } else if (data.error === false) {
      return location.href = redirect || data.redirect;
    } else {
      return Datafly.alert(data.error);
    }
  });
};

$(function() {
  $('#login .btn').click(Datafly.submit);
  return $('#post-logout').click(function(event) {
    return $(this).next('form').submit();
  });
});
