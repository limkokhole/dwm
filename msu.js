// HtmlTextLink.js

var need_show = false;
var html_content = "";
var final_url = "";


function showFrame(page) {
    need_show = false;
    html_content = html_content + page.frameContent + "\n";
    for (var i = 0; i < page.framesCount; i++) {
        page.switchToFrame(i);
        showFrame(page);
        page.switchToParentFrame();
    }
}


var pageTimeoutFunc = function() {
    if (need_show) {
        // never got to load_finished
        page.switchToMainFrame();
        showFrame(page);
    }
    done_loading();
    phantom.exit();
};


//function get_boundary() {
//    var d = new Date();
//    return "===dwm_proxy_boundary==="
//           + d.getTime().toPrecision(20)
//           + Math.random().toPrecision(10)
//           + Math.random().toPrecision(10)
//           + "==="
//}


function out_line(data) {
    console.log(data)
}


function done_loading() {
    //final_url = page.url;
    //var bd = get_boundary();
    //// output data
    //out_line(bd);
    out_line(html_content);
    //out_line(bd);
    //out_line(text_content);
    //out_line(bd);
    //out_line('quote_final_url:: ' + encodeURIComponent(final_url));
    //out_line(link_content);
}


function should_wait(page) {
    var has_refresh = page.evaluate(function () {
        var ms = document.getElementsByTagName('meta');
        //return ms.length;
        for (var i=0; i<ms.length; ++i ) {
            var m = ms.item(i);
            if (m.httpEquiv.toLowerCase() == 'refresh') {
                // content="92;URL=word_anchor.html"
                // return 92
                // content=";URL=word_anchor.html"
                // return 0
                var t = parseInt(m.content);
                return isNaN(t) ? 0 : t;
            }
        }
        return "norefresh";
    });
    //console.log('has_refresh=' + has_refresh + '; tmo_sec=' + tmo_sec);
    if (!isNaN(has_refresh) && (has_refresh < tmo_sec)) {
        //console.log('should_wait=true');
        return true;
    }
    //console.log(has_refresh);
    // if hase script, and not many content text, wait
    var has_script = page.evaluate(function () {
        var ss = document.getElementsByTagName('script');
        var ii = document.getElementsByTagName('iframe');
        return ss.length + ii.length;
    });
    if (has_script > 0 && html_content.length < 100) {
        return true;
    }
    //return false;
    //return true;
    return tmo_sec < 0
}


function load_finished(status) {
    //console.log(status);
    if (need_show) {
        page.switchToMainFrame();
        showFrame(page);
    }
    if (should_wait(page)) {
        //console.log("loading not finished1");
        return;
    }
    clearTimeout(tmo);
    done_loading();
    //console.log("loading finishedx");
    //phantom.exit();
};


//function popup(msg) {
//    text_content = text_content + "\n" + msg + "\n";
//}


/*
 * dwm.js timeout_sec url
 */

var args = require('system').args;
if (args.length != 3 && args.length != 4) {
    console.log("Usage: " + args[0] + " timeout_sec url [referer]");
    phantom.exit(0);
}

var tmo_sec = args[1];
var req_url = args[2];
var tmo = setTimeout(pageTimeoutFunc, Math.abs(tmo_sec) * 1000);
var page = require('webpage').create();
//page.settings.userAgent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.4 (KHTML, like Gecko) Safari/537.4';
page.settings.userAgent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.101 Safari/537.36';
if (args.length == 4) {
    page.customHeaders = {'Referer': args[3]};
}
page.customHeaders = {
//'Content-Type': 'application/x-www-form-urlencoded',
//'Origin': 'http://moviesunusa.net',
//'Upgrade-Insecure-Requests': '1',
'Referer': 'http://moviesunusa.net/%E7%8E%8B%E5%86%A0-%E7%AC%AC1%E5%AD%A3-%E7%AC%AC7%E9%9B%86-s1-ep7/',
//'DNT': '1',
};
page.settings.loadImages = false;
page.onLoadFinished = load_finished;
page.onLoadStarted = function() {
    need_show = true;
}
page.onUrlChanged = function(targetUrl) {
  console.log('New URL: ' + targetUrl);
};
req_url = 'http://moviesunusa.net/wp-login.php';

page.open(req_url, 'POST',
'log=sun03&pwd=sun&wp-submit=Login+%E2%86%92&redirect_to=http%3A%2F%2Fmoviesunusa.net%2F%25E7%258E%258B%25E5%2586%25A0-%25E7%25AC%25AC1%25E5%25AD%25A3-%25E7%25AC%25AC7%25E9%259B%2586-s1-ep7%2F',
//'log=sun03&pwd=sun&wp-submit=Login+%E2%86%92',
    function(status) {
      console.log('POST Status: ' + status);
      // Do other things here...
      var cookies = page.cookies;
      
      console.log('Listing POST cookies:');
      for(var i in cookies) {
        console.log(cookies[i].name + '=' + cookies[i].value);
      }
    }
);

