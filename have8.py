# -*- coding: utf8 -*-

import os
import re
import sys
from subprocess import Popen, PIPE
try: 
    from urllib import unquote
    from urlparse import urlparse
except ImportError:
    from urllib.parse import unquote, urlparse
 
from dailymotion import DM
from comm import DWM, match1, echo, start


#h8decode(data, 'dailymotion')
def h8decode(a, b):
    ss = ""
    l = len(b) + 1
    for i, s in enumerate(a):
        if 0 == i % l:
            ss += s
    return unquote("".join(reversed(ss))).split('+++')


class HAVE8(DWM):     # http://have8.com/
    handle_list = ['have8tv\.com/v/drama/\d+/\d+/dailymotion\.html']

    def get_vid(self, hutf, idx=''):
        m = re.search('adrss\[0\] \= "([^"]+)"', hutf)
        data = m.groups()[0]
        vids = h8decode(data, 'dailymotion')
        vids = [v.split('++') for v in vids]
        if not idx:
            return vids
        for i, v in vids:
            #echo(repr(i), repr(idx))
            if int(i) == int(idx):
                return v
        return None

    def query_info(self, url):
        #url = "http://have8tv.com/v/drama/2/21852/dailymotion.html?0-1-0"
        hutf = self.get_hutf(url)
        up = urlparse(url)
        sels = up.query.split('-')
        #echo(sels)
        idx = 1
        if len(sels) > 1:
            idx = sels[1]
        vid = self.get_vid(hutf, idx)
        echo(vid)
        dm = DM()
        return dm.query_info('http://www.dailymotion.com/embed/video/' + vid)

    def get_playlist(self, url):
        #url = "http://have8tv.com/v/drama/2/21852/dailymotion.html?0-1-0"
        up = urlparse(url)
        sels = up.query.split('-')
        if len(sels) < 2:
            sels = ['0', '', '0']
        hutf = self.get_hutf(url)
        vids = self.get_vid(hutf)
        urls = []
        base = up.scheme + '://' + up.netloc + up.path
        for vid in vids:
            sels[1] = vid[0]
            urls.append((None, base + "?" + '-'.join(sels)))
        return urls

    def get_playlist1(self, url):
        #url = "http://have8tv.com/v/drama/2/21852/dailymotion.html?0-1-0"
        hutf = self.get_hutf(url)
        vids = self.get_vid(hutf)
        urls = []
        dm = DM()
        for vid in vids:
            t, e, us, z = dm.query_info('http://www.dailymotion.com/embed/video/' + vid[1])
            urls.append((t, us[0]))
        return urls

    def query_info1(self, url):
        url = "http://have8tv.com/v/drama/2/21852/dailymotion.html?0-1-0"
        hutf = self.get_hutf(url)
        # get vid
        m = re.search('adrss\[0\] \= "([^"]+)"', hutf)
        data = m.groups()[0]
        vids = h8decode(data, 'dailymotion')
        vid = vids[0].split('++')[1]
        echo('vid =', vid)
        #sys.exit(1)
        # get vid url
        self.extra_headers['Referer'] = url
        #http://www.dailymotion.com/embed/video/k4BjypcByJGUTDl6Bvx
        #rurl = 'http://www.dailymotion.com/embed/video/k7alsxAgBgcMGaachYS?api=postMessage&autoplay=0&info=0'
        rurl = 'http://www.dailymotion.com/embed/video/%s?api=postMessage&autoplay=0&info=0' % vid
        hutf = self.get_hutf(rurl)
        echo(hutf)
        #m = re.search('"ad_url":"([^"]+)"', hutf)
        #aurl = m.groups()[0].replace('\\', '') + '&ps=658x435&ct=website&callback=jsonp_1482257169574_88239'
        #echo(aurl)
        # "720":[{"type":"application\/x-mpegURL","url":"http:\/\/www.dailymotion.com\/cdn\/manifest\/video\/x2hpv0i.m3u8?auth=1482432896-2562-0fq84z9d-24047244e9a36f0f3fab8388642b74c1&include=720"},{"type":"video\/mp4","url":"http:\/\/www.dailymotion.com\/cdn\/H264-1280x720\/video\/x2hpv0i.mp4?auth=1482432896-2562-pvg451ll-4c251ca9aa8a1bf6f56c88d318eccd65"}]}
        m = re.search('"type":"video\\/([^"]+)","url":"([^"]+)"', hutf)
        ext = m.group(1)
        vurl = m.group(2).replace('\\', '')
        echo("ext =", ext, ", url =", vurl)
        m = re.search('/x-mpegURL","url":"([^"]+)"', hutf)
        vurl = m.groups()[0].replace('\\', '')
        self.extra_headers['Referer'] = rurl
        # using ad url set cookie
        hutf = self.get_hutf(aurl)
        # get m3u8 list
        hutf = self.get_hutf(vurl)
        echo(hutf)
        mr = 0
        mu = ''
        for data in hutf.split('#EXT-X-STREAM-INF')[1:]:
            lines = data.split('\n')
            m = re.search('NAME="(\d+)"', lines[0])
            r = int(m.group(1))
            if r > mr:
                mr, mu = r, lines[1].strip()
        echo('mr =', mr, ', mu =', mu)
        sys.exit(1)

        #return self.title, k, [url], tsize


if __name__ == '__main__':
    start(HAVE8)