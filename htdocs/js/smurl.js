// -*- coding: utf-8 -*-
function show_msg(text) {
  $('.msg .text').html(text);
  $('.msg').show();
}
function change_url() {
  $('.msg').hide();
  $('#res').hide();
}
function minimize_url() {
  var subdomain = sel_val("#subdomain input");
  var alias = sel_val("#alias input");
  if (!subdomain_validate(subdomain)) {
     $("#subdomain input").focus();
     return false;
  } else if (!alias_validate(alias)) {
     $("#alias input").focus();
     return false;
  }

  var url = $('#url').val().replace(/^\s+|\s+$/g, '');
  if (url == '') {
     show_msg('Вы не ввели ссылку!');
     $('#url').focus();
     return false;
  } else if (!url.match(/^((https?):\/\/)?((\d+\.){3}\d+|([a-zA-Z0-9-]+\.)+[a-z]{2,10})(:\d+)?($|#|\/|\?)/)) {
     show_msg('То, что вы ввели, не похоже на ссылку!');
     $('#url').focus();
     return false;
  } else {
     $('.msg').hide();
  }

  if (!url.match(/^((https?):\/\/)/)) {
     url = 'http://' + url;
  }

  $.getJSON("/api/json",
        { 'url': url, 'subdomain': subdomain, 'alias': alias },
        function(data){
          if (data.errors) {
             if (data.errors[0].match(/^alias/)) {
               show_msg('К сожалению, запрошенный урл уже занят.');
             } else {
               show_msg('Что-то где-то сломалось?');
             }
          } else {
             $('#res').hide().html("<input value=\""+html_quote(data.smurl)+"\" onfocus=\"this.select();\"><br><a href=\""+html_quote(data.smurl)+"\" target=_blank>проверка &rarr;</a>").show();
             $('#alias input').val('');
             alias_close();
             $('#res input').select();
          }
        });

  return false;
}

function fp_init() {
    var subdomain = Cookies.get('subdomain');
    if (subdomain == null || subdomain == '') {
        var m = document.location.hostname.match('^(.*)\.smurl\.ru$');
        if (m) subdomain = m[1];
    }
    subdomain_close(subdomain);
    alias_close();
    $('#url').focus();
}

function sel_val(sel, def) {
  var els = $(sel);
  return els.length ? els.val() : (def == null ? '' : def);
}
function html_quote(val) {
  return val.replace(/\&/g, '&amp;').replace(/</g, '&lt;').replace(/\>/g, '&gt;').replace(/\"/g, '&quot;');
}

//////////// subdomain
function subdomain_validate(val) {
  if (val != '' && !val.match(/^[a-zA-Z0-9-]+$/)) {
     show_msg('То, что вы ввели, не похоже на домен!');
     return false;
  }
  return true;
}
function subdomain_edit() {
  var val = sel_val('#subdomain input');
  $('#subdomain').html("<input size=10 onblur='subdomain_close();' class=underlined value=\""+html_quote(val)+"\" onkeypress=\"$('.msg').hide();\"><span class=dot>.</span>");
  $('#subdomain input').focus();
}
function subdomain_close(def) {
  var val = sel_val('#subdomain input', def).replace(/\s/g, '');
  if (val == '') {
    Cookies.remove('subdomain', 'smurl.ru', '/');
    $('#subdomain').html("<span class=underlined onclick='subdomain_edit()'>&nbsp;&nbsp;&nbsp;</span>");
  } else if (subdomain_validate(val)) {
    Cookies.set('subdomain', val, 365*24, 'smurl.ru', '/');
    $('#subdomain').html("<span class=underlined onclick='subdomain_edit()'><input type=hidden value=\""+html_quote(val)+"\">" + html_quote(val) + "</span><span class=dot>.</span>");
  }
}

///////////// alias
function alias_validate(val) {
  if (val != '' && !val.match(/^[a-zA-Z0-9-]+$/)) {
     show_msg('Допустимы латинские буквы, цифры и знак \"-\"!');
     return false;
  }
  return true;
}
function alias_edit() {
  var val = sel_val('#alias input');
  $('#alias').html("<input size=10 onblur='alias_close();' value=\""+html_quote(val)+"\" onkeypress=\"$('.msg').hide();\" class=underlined>");
  $('#alias input').focus();
}
function alias_close() {
  var val = sel_val('#alias input').replace(/\s/g, '');
  if (val == '') {
    $('#alias').html("<span class='underlined gray' onclick='alias_edit()'>&lt;auto&gt;</span>");
  } else if (alias_validate(val)) {
    $('#alias').html("<span class=underlined onclick='alias_edit()'><input type=hidden value=\""+html_quote(val)+"\">" + html_quote(val) + "</span>");
  }
}


///////////// coockie
function getHeader(name, value, time, domain, path) {
    var kookie = [];
    kookie.push(name + '=' + encodeURIComponent(value));
    if (typeof time == 'number') {
        var expire = new Date();

        expire.setTime(expire.getTime() + (time * 3600000));
        kookie.push('expires=' + expire.toGMTString());
    }
    kookie.push('domain=' + (domain || window.location.hostname));
    kookie.push('path=' + (path || '/'));
    return kookie.join(';');
}
function setHeader(name, value, time, domain, path) {
    document.cookie = getHeader(name, value, time, domain, path);
}
Cookies = {
    set: function(name, value, time, domain, path) {
        if (value !== null && value !== '') {
            setHeader(name, value, time, domain, path);
        }
    },
    get: function(name) {
        var res = document.cookie.match(new RegExp(name + '=([^;]*)'));
        return (res && res[1] ? decodeURIComponent(res[1]) : null);
    },
    remove: function(name, domain, path) {
        setHeader(name, '', -365 * 24, domain, path);
    }
};
