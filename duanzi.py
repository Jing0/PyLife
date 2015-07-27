# -*- coding:utf-8 -*-
from __future__ import unicode_literals
import urllib2
import re
import random

# TODO:deal with </br>
#      dic query(dealWithTag)

class DuanZi(object):
    headers = {
        'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_4) AppleWebKit/600.7.12 (KHTML, like Gecko) Version/8.0.7 Safari/600.7.12',
        'Connection': 'keep-alive',
    }

    def __init__(self):
        pass

    def request(self, url):
        request = urllib2.Request(url, headers = self.headers)
        response = urllib2.urlopen(request)
        htmlText = response.read()
        return htmlText

    def getDuanFrom(self, key):
        urlDict = {
            'Qiu':'http://www.qiushibaike.com/text',
            #'Jan':'http://jandan.net/duan',
            'Leng':'http://lengxiaohua.com',
            'isShuo':'http://ishuo.cn'
            #'lify':'http://www.lify.info',
            #'juzhang':'http://www.douban.com/people/chunsue/statuses'
        }
        regDict = {
            'Qiu':'(?<=<div class="content">\n\n).*',
            'Jan':'(?<=</span><p>)[^<]*(?=</p>)',
            'Leng':'(?<="first_char">).*(?=</pre>\s*</div>)',
            'isShuo':'(?<=<div class="content">)[^<]{45,}?(?=</div>)',
            'lify':'(?<=[ ]{12}).*?(?=[ ]{5}</div>)',
            'juzhang':'(?<=ying">[\n]{4}<blockquote>[\s]{3}<p>).*(?=</p>)'
        }
        htmlText = self.request(urlDict[key])
        return re.findall(regDict[key], htmlText)

    def dealWithTags(self, text):
        tags = {u'<br/>':'\n', u'</span>':'', u'&quot;':'"'}
        keys = tags.iterkeys()
        for key in keys:
            text = tags[key].join(text.split(key))
        return text

    def getRandomDuan(self):
        duanList = self.getAllDuan()
        if len(duanList) == 0:
            return '貌似没有新的段子哦😲 😲'
        randomText = random.choice(duanList)
        return self.dealWithTags(randomText.decode('utf-8'))

    def getAllDuan(self):
        keyList = ['Qiu', 'Leng', 'isShuo']
        duanList = []
        for key in keyList:
            duanList += self.getDuanFrom(key)
        return duanList

duanZi = DuanZi()
print len(duanZi.getAllDuan())
print duanZi.getRandomDuan()
