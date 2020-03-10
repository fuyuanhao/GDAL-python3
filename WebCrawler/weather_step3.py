# -*- coding: utf-8 -*-
import urllib.request as req
import re
import numpy as np
import pandas as pd
import datetime

def get_content(url):
    webpage = req.urlopen(url)
    html = webpage.read()
    html = html.decode('utf-8')
    return html

def gef_from_span(span_label,li_data_i,sub_list):
    subtable_sth = re.findall(span_label, li_data_i, re.S)
    # 取字段名称的公共标签
    field_label = r'>(.*?)<'
    if len(subtable_sth) > 0:
        sth_name = re.findall(field_label, subtable_sth[0], re.S)
        if sth_name:
            sub_list.append(sth_name[0])

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

            gef_from_span(span_city_label, li_data[i], sub_list)
            gef_from_span(span_pro_label, li_data[i], sub_list)
            gef_from_span(span_wd_label, li_data[i], sub_list)
            weather_list.append(sub_list)

    print(weather_list)
    # 准备数据集
    pd_data = pd.DataFrame(weather_list)
    # 表格列名，为输出EXCEL做准备
    colunms = ['Num', 'city', 'prov', 'wd']
    # 添加列名
    pd_data.columns = colunms
    print(pd_data)
    today = datetime.date.today()
    formatted_today = today.strftime('%y%m%d')
    ExcelName = r'C:\Projects\WebCrawler\Data\WeatherArray'+str(formatted_today)+'.xlsx'
    sheetName = 'Weather'
    WriteExcel(pd_data, ExcelName, sheetName)

# 写入EXCEL
def WriteExcel(pd_data, ExcelName, sheetName):
    writer = pd.ExcelWriter(ExcelName)  # 写入Excel文件
    pd_data.to_excel(writer, sheetName, index=False)  # 写入excel的sheet名
    writer.save()
    writer.close()
    print('Done:' + ExcelName)

if __name__ == '__main__':
    url ='http://www.weather.com.cn/'
    getDataFrom(url)