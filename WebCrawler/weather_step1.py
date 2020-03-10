# -*- coding: utf-8 -*-
import urllib.request as req

#获取全部hmtl网页内容
def get_content(url):
    webpage = req.urlopen(url) # 根据超链访问链接的网页
    html = webpage.read() # 读取超链网页数据
    html = html.decode('utf-8') # byte类型解码为字符串
    print(html)
    return html

if __name__ == '__main__':
    #目标网站
    url ='http://www.weather.com.cn/'
    get_content(url)
