#!/usr/bin/python
# -*- coding: UTF-8 -*-
from __future__ import unicode_literals
import datetime
import requests
import feedparser
from flask import Flask,render_template,request,make_response


#创建一个实例
app = Flask(__name__)

RSS_FEED = {"zhihu": "https://www.zhihu.com/rss",
            "netease": "http://news.163.com/special/00011K6L/rss_newsattitude.xml",
            "songshuhui": "http://songshuhui.net/feed",
            "ifeng": "http://news.ifeng.com/rss/index.xml"}
            
DEFAULTS = {'city':'北京',
			'publication':'ifeng'}

WEATHERS = {"北京":101010100,
			"上海":101020100,
			"广州":101280101,
			"深圳":101280601}


'''
路由：处理URL与函数的关系
视图函数：返回值是给客户端的响应
使用feedparser获取RSS数据
使用动态路由获取不同网站的headlines
使用jinja2模板分离业务逻辑和表现逻辑
使用模板循环显示所有文章
使用POST请求提交数据
增加天气预报功能
使用cookies记住用户选择
'''

def get_value_with_fallback(key):
	if request.args.get(key):
		return request.args.get(key)
	if request.cookies.get(key):
		return request.cookies.get(key)
	return DEFAULTS[key]





@app.route('/')
def home():
    publication = get_value_with_fallback('publication')
    city = get_value_with_fallback('city')

    weather = get_weather(city)
    articles = get_news(publication)

    response = make_response(render_template('home.html', articles=articles,
                                             weather=weather))
    expires = datetime.datetime.now()+datetime.timedelta(days=365)
    response.set_cookie('publication',  publication, expires=expires)
    response.set_cookie('city',  city, expires=expires)

    return response

def get_news(publication):
    feed = feedparser.parse(RSS_FEED[publication])
    return feed['entries']


def get_weather(city):
    code = WEATHERS.get(city, 101010100)
    url = "http://www.weather.com.cn/data/sk/{0}.html".format(code)

    r = requests.get(url)
    r.encoding = 'utf-8'

    data = r.json()['weatherinfo']
    return dict(city=data['city'], temperature=data['temp'],
                description=data['WD'])


'''
启动服务器，debug=True启用调试模式
'''
if __name__ == '__main__':
	app.run(host='127.0.0.1',port=5000,debug=True)

