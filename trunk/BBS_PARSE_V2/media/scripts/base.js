/*------selection operations-------*/
function insertAtCursor(obj, txt) {
  obj.focus();
  //IE support
  if (document.selection) {
    sel = document.selection.createRange();
    sel.text = txt;
  }
  //MOZILLA/NETSCAPE support
  else {
    var startPos = obj.selectionStart;
    var scrollTop = obj.scrollTop;
    var endPos = obj.selectionEnd;
    obj.value = obj.value.substring(0, startPos) + txt + obj.value.substring(endPos, obj.value.length);
    startPos += txt.length;
    obj.setSelectionRange(startPos, startPos);
    obj.scrollTop = scrollTop;
  }
}
function getCaretPos(ctrl) {
	var caretPos = 0;
	if (document.selection) {
    // IE Support
    var range = document.selection.createRange();
    // We'll use this as a 'dummy'
    var stored_range = range.duplicate();
    // Select all text
    stored_range.moveToElementText( ctrl );
    // Now move 'dummy' end point to end point of original range
    stored_range.setEndPoint( 'EndToEnd', range );
    // Now we can calculate start and end points
    ctrl.selectionStart = stored_range.text.length - range.text.length;
    ctrl.selectionEnd = ctrl.selectionStart + range.text.length;
    caretPos = ctrl.selectionStart;
	} else if (ctrl.selectionStart || ctrl.selectionStart == '0')
    // Firefox support
		caretPos = ctrl.selectionStart;
	return (caretPos);
}

function getCurrentLineBlanks(obj) {
  var pos = getCaretPos(obj);
  var str = obj.value;
  var i = pos-1;
  while (i>=0) {
    if (str.charAt(i) == '\n')
      break;
    i--;
  }
  i++;
  var blanks = "";
  while (i < str.length) {
    var c = str.charAt(i);
    if (c == ' ' || c == '\t')
      blanks += c;
    else
      break;
    i++;
  }
  return blanks;
}

function check_limit(field, limit) {
  if (field.value.length > limit) {
    alert("老大，整太多了吧，最多输入 " + limit + " 个字符！");
    // Truncate at the limit
    var revertField = field.value.slice(0, limit - 10);
    field.value = revertField;
    field.focus();
  }
}

/*------cookie operations-------*/
function set_cookie(key, value, exp, path, domain, secure ) {
  var cookie_string = key + "=" + escape ( value );
  if (exp) {
    cookie_string += "; expires=" + exp.toGMTString();
  }
  if (!path)
    path = "/";
  cookie_string += "; path=" + escape(path);
  if (domain)
    cookie_string += "; domain=" + escape(domain);
  if (secure)
    cookie_string += "; secure";
  document.cookie = cookie_string;
}

function get_cookie(cookie_name) {
  var results = document.cookie.match('(^|;) ?' + cookie_name + '=([^;]*)(;|$)');

  if (results)
    return (unescape(results[2]));
  else
    return null;
}

function delete_cookie(cookie_name) {
  var cookie_date = new Date(); //current date & time
  cookie_date.setTime(cookie_date.getTime() - 1);
  document.cookie = cookie_name += "=; expires=" + cookie_date.toGMTString();
}

/*------bookmark this site------*/
function bookmark(title, url){
  if (document.all)
    window.external.AddFavorite(url, title);
  else if (window.sidebar)
    window.sidebar.addPanel(title, url, "");
}

/*------cloning functions------*/
Array.prototype.clone = function() {
  var c = [];
  var old = this;
  for (var i=0; i<old.length; i++) {
    var o = old[i];
    c[i] = o.clone ? o.clone() : o;
  }
  return c;
};

function clone_hash(obj) {
  var c = {};
  var old = this;
  for (var key in obj) {
    if (!old[key]) continue;
    var o = old[key];
    c[key] = o.clone ? o.clone() : o;
  }
  return c;
}

function set_tab_indent_for_textareas() {
  /* set all the tab indent for all the text areas */
  $("textarea").each(function() {
    $(this).keydown(function(eve){
      if (eve.target != this) return;
      if (eve.keyCode == 13)
        last_blanks = getCurrentLineBlanks(this);
        /*else if (eve.keyCode == 9) {*/
        /*eve.preventDefault();*/
        /*insertAtCursor(this, "  ");*/
        /*this.returnValue = false;*/
        /*}*/
    }).keyup(function(eve){
      if (eve.target == this && eve.keyCode == 13)
          insertAtCursor(this, last_blanks);
    });
  });
}
String.prototype.escapeHTML = function () {
  return this.replace(/&/g,'&amp;').replace(/>/g,'&gt;').replace(/</g,'&lt;').replace(/"/g,'&quot;');
};

//string buffer
function StringBuffer() {
  this.buffer = [];
}

StringBuffer.prototype.append = function append(string) {
  this.buffer.push(string);
  return this;
};

StringBuffer.prototype.toString = function toString() {
  return this.buffer.join("");
};

function set_page_info() {
  //set the page info
  var url = window.location.toString();
  result = url.match(/[\?\&]page=([^\&]+)([\b\&]|$)/);
  if (result) id = "p_" + result[1];
  else id = "p_1";
  obj = document.getElementById(id);
  if (obj) {
    obj.style.fontWeight = "bold";
    obj.style.color = "red";
  }
}

function set_current_links() {
  var url = window.location.href;
  var rxlinks = /^http:\/\/[^\/]*\/([^\/]+)\/([^\/]*)/;
  var m = url.match(rxlinks);
  if (m) {
    $("#sl_" + m[1]).addClass("current"); //subsite links in whole site
    $("#pl_" + m[2]).addClass("current"); //page links in subsite
  } else {
    $("#sl_").addClass("current");
    $("#pl_").addClass("current");
  }
}

$(document).ready(function() { set_current_links(); });

//share button
$(function(){
  var addrs = {
    'delicious':['http://delicious.com/post?v=4', 'url', 'title'],
    'baidu':['http://cang.baidu.com/do/add?tn=', 'iu', 'it'],
    'qq':['http://shuqian.qq.com/post?from=3&', 'uri', 'title'],
    'google':['http://www.google.com/bookmarks/mark?op=add', 'bkmk', 'title'],
    'douban':['http://www.douban.com/recommend/?sel=&v=1', 'url', 'title'],
    'xiaonei':['http://share.xiaonei.com/share/ShareOperate.do?action=sharelink', 'weblink', 'title'],
    'yahoo':['http://myweb.cn.yahoo.com/popadd.html?', 'url', 'title'],
    'leshou':['http://leshou.com/post?act=posturl&reuser=&intro=&tags=&tool=0', 'url', 'title'],
    '365key':['http://www.365key.com/storeit.aspx?c=', 'u', 't'],
    'digg':['http://digg.com/submit?phase=2', 'url', 'title']
  };
  $("#mysharesome li").hover(function(){$(this).css("backgroundColor", "#dddddd");}, function(){$(this).css("backgroundColor", "");});
  $("#mysharesome li").click(function(){
    var cn = $(this).attr("class").substring(3);
    if (addrs[cn]) {
      var addr = addrs[cn];
      window.location.href = addr[0] + "&" + addr[1] + "=" + encodeURIComponent(window.location.href) + "&" + addr[2] + "=" + encodeURIComponent(document.title);
    } else if (cn == "twitter") {
      window.location.href = "http://twitter.com/home?status=" + encodeURIComponent(window.location.href + " " + document.title);
    } else if (cn == "favorites") {
      bookmark(document.title, window.location.href);
    } else {
      alert("这个选项没见过，报告一下管理员吧...");
    }
  });
  $("#myshare a").attr('href', 'http://www.shibabang.com/addthis/bookmark.html?v=1&s=&uid=fayaa&url=' + encodeURIComponent(window.location.href) + '&title=' + encodeURIComponent(document.title) + '&language=cn&logo=');
});

