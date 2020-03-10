# -*- coding: utf-8 -*-
import urllib.request as req
import re

def get_content(url):
    webpage = req.urlopen(url)
    html = webpage.read()
    html = html.decode('utf-8')
    return html

def getDataFrom(url):
    html =get_content(url)
    label = r'<ul class="on">(.*?)</ul>'
    table = re.findall(label, html, re.S)
    print('-------------table-------------')
    print(table)
    li_label = r'<li(.*?)</li>'
    li_data = re.findall(li_label,table[0],re.S)
    print('-------------li_data------------')
    print(li_data)

    # 气象数据列表
    weather_list = []
    # 指定城市名的标签
    span_city_label = r'<span class="city">(.*?)</span>'
    # 指定省名的标签
    span_pro_label = r'<span class="prov">(.*?)</span>'
    # 指定温度的标签
    span_wd_label = r'<span class="wd"(.*?)</span>'

    print('-----------Data----------------')
    for i in range(len(li_data)-2):
        # 每一行的数据组合
        sub_list = []
        if li_data[i] is not None:
            sub_list.append(i + 1)
            i = i+1
            #print('-------------------------指定span_city_label标签中数据：城市名------------------------')
            subtable_city = re.findall(span_city_label, li_data[i], re.S)
            # 取字段名称的公共标签
            field_label = r'>(.*?)<'
            if len(subtable_city) > 0:
                city_name = re.findall(field_label,subtable_city[0],re.S)
                if city_name:
                    sub_list.append(city_name[0])

            #print('-------------------------指定span_pro_label标签中数据：省名------------------------')
            subtable_pro = re.findall(span_pro_label, li_data[i], re.S)
            field_label = r'>(.*?)<'
            if len(subtable_pro) > 0:
                pro_name = re.findall(field_label, subtable_pro[0], re.S)
                if pro_name:
                    sub_list.append(pro_name[0])

            #print('------------------------- 指定span_wd_label标签中数据：温度------------------------')
            subtable_wd = re.findall(span_wd_label, li_data[i], re.S)
            field_label = r'>(.*?)<'
            if len(subtable_wd) > 0:
                wd_value = re.findall(field_label, subtable_wd[0], re.S)
                if wd_value:
                    sub_list.append(wd_value[0])

            weather_list.append(sub_list)
    print(weather_list)


if __name__ == '__main__':
    url ='http://www.weather.com.cn/'
    getDataFrom(url)