// -*- coding: utf-8 -*-
function change_url() {
  //$('.msg').hide();
  //$('#res').hide();
}
function minimize_url() {
  var url = $('#url').val();

  url = url.replace(/^\s+|\s+$/g, '');
  if (!url.match(/^((https?):\/\/)?((\d+\.){3}\d+|([a-zA-Z0-9-]+\.)+[a-z]{2,10})(:\d+)?($|#|\/|\?)/)) {
     $('.msg .text').html('То что вы ввели не похоже на ссылку!');
     $('.msg').show();
     $('#url').focus();
     return false;
  } else {
     $('.msg').hide();
  }

  if (!url.match(/^((https?):\/\/)/)) {
     url = 'http://' + url;
  }

  $.getJSON("/api/json",
        { 'url': url },
        function(data){
          $('#res').hide().html("<a href=\""+data.smurl+"\" target=_blank>"+data.smurl+"</a>").show();
        });

  return false;
}
