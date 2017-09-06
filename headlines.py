from __future__ import unicode_literals

import feedparser
from flask import Flask


#创建一个实例
app = Flask(__name__)

ZHIHU_FEED = "http://www.zhihu.com/rss"

'''
路由：处理URL与函数的关系
视图函数：返回值是给客户端的响应
'''
@app.route('/')
def get_news():
	feed = feedparser.parse(ZHIHU_FEED)
	first_content = feed['entries'][0]
	html_format = """
	<html> <body>
		<h1> Zhihu headlines </h1>
		<b> {0} </b> <br/>
		<i> {1} </i> <br/>
		<p> {2} </p> <br/>
	</body> </html>
		"""
	return html_format.format(first_content.get('title'),
                              first_content.get('published'),
                              first_content.get('summary'))
                              

'''
启动服务器，debug=True启用调试模式
'''
if __name__ == '__main__':
	app.run(host='0.0.0.0',port=5000,debug=True)

