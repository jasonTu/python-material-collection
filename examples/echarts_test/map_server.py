# coding: utf-8
from pyecharts import Bar, Map


def get_html_content():
    bar = Bar()
    bar.add_xaxis(["衬衫", "毛衣", "领带", "裤子", "风衣", "高跟鞋", "袜子"])
    bar.add_yaxis("商家A", [114, 55, 27, 101, 125, 27, 105])
    bar.add_yaxis("商家B", [57, 134, 137, 129, 145, 60, 49])
    bar.render()

def get_china_map_test():
    # value =[155, 10, 66, 78, 33, 80, 190, 53, 49.6]
    # attr =["福建", "山东", "北京", "上海", "甘肃", "新疆", "河南", "广西", "西藏"]
    value =[155]
    attr =["Tokyo"]
    map=Map("Map 结合 VisualMap 示例",width=1200, height=600)
    map.add("", attr, value, maptype='japan', is_visualmap=True, visual_text_color='#000')
    map.render()

def application(env, start_response):
    start_response('200 OK', [('Content-Type','text/html')])
    # get_china_map_test()
    # get_html_content()
    with open('./render.html', 'rb') as fp:
        data = fp.read()
    # return [b"Hello World"]
    return [data]
