# -*- coding: utf8 -*-

import re
import sys
import json
from subprocess import Popen, PIPE

from mybs import SelStr
from comm import DWM, echo, start


class KANTV6(DWM):
    handle_list = ['//kantv6\.com/', '//www\.kantv6\.com/']

    def query_info(self, url):
        # https://www.kantv6.com/tvdrama/301948271219001-161948271219033
        # https://www.kantv6.com/index.php/video/play?tvid=301948271219001&part_id=161948271219033&line=1&seo=tvdrama
        #hutf = self.chrome_hutf(url)
        #title = SelStr("h4.mtg-videoplay-title", hutf)[0].text
        #echo(title)
        #title = title.replace("&nbsp;", "_")
        #echo(title)
        #return
        title = self.get_title(url)
        m = re.search("/(tvdrama)/(\d+)-(\d+)", url)
        sect, tvid, ptid = m.groups()
        du = "https://www.kantv6.com/index.php/video/play"
        du = "%s?tvid=%s&part_id=%s&line=1&seo=%s" % (du, tvid, ptid, sect)
        dat = self.get_hutf(du)
        dat = json.loads(dat)
        #u38 = 'https:' + dat['data']['url']
        us = self.try_m3u8('https:' + dat['data']['url'])
        return title, None, us, None

    def get_playlist(self, url):
        ns = SelStr('div.entry-content.rich-content tr td a',
                    self.get_hutf(url))
        return [(a.text, a['href']) for a in ns]

    def test(self, argv):
        url = 'https://www.kantv6.com/tvdrama/301948271219001-161948271219033'
        self.get_title(url)

    def get_title(self, url):
        while True:
            til = self.get_title_one(url)
            if til:
                break
        echo("title", til)
        return til
    
    def get_title_one(self, url):
        hutf = self.chrome_hutf(url)
        #echo(hutf)
        h4 = SelStr("h4.mtg-videoplay-title", hutf)[0]
        t = h4("span")[0].text.strip()
        p = h4("span#cPartNum")[0].text.strip()
        if t and p:
            return t + '_' + p
        return ""
        
        #title = title.replace("&nbsp;", "_")
        #echo(title)


if __name__ == '__main__':
    start(KANTV6)
