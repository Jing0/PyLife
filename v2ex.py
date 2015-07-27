# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import requests, re

class V2ex(object):
    url = "http://v2ex.com/"
    signin_url = url + "signin"
    useragent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_4) AppleWebKit/600.7.12 (KHTML, like Gecko) Version/8.0.7 Safari/600.7.12"
    dailymission_url = "http://v2ex.com/mission/daily"
    session = requests.Session()
    isLogin = False

    def __init__(self, username, password):
        self.username = username
        self.password = password
        print "username:" + username
        self.login()

    def getLoginCode(self):
        return re.findall('value="(\d+)" name="once"', self.session.get(self.signin_url).text)[0]

    def login(self):
        params = {
            'u'   :self.username,
            'p'   :self.password,
            'once':self.getLoginCode(),
            'next':'/'
        }
        signin = self.session.post(self.signin_url, data = params, headers = {'Referer': self.signin_url })
        if signin.text.find("signout") == -1:
            print "login failed"
        else:
            print "login successfully"
            self.isLogin = True
    def dailymission(self):
        if self.session.get(self.dailymission_url).text.find("fa-ok-sign") != -1:
            print "daily mission already completed"
            successiveDays = re.findall('(?<=已连续登录 )\d+',self.session.get(self.dailymission_url).text)[0]
            print "You have completed dailymission for " + successiveDays + " days"
        else:
            try:
                missiononce = re.findall('mission/daily/redeem\?once=\d+',self.session.get(self.dailymission_url).text)[0]
                mission = self.session.get(self.url + missiononce, headers = {"Referer":"http://www.v2ex.com/mission/daily"})
            except Exception, e:
                print "daily mission failed"
            else:
                print "daily mission succeeded" 
                successiveDays = re.findall('(?<=已连续登录 )\d+',self.session.get(self.dailymission_url).text)[0]
                print "You have completed dailymission for " + successiveDays + " days"

username = "XXX"
password = "XXX"
v2ex = V2ex(username, password)
if v2ex.isLogin :
    v2ex.dailymission()
