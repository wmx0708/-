# -*- coding: utf-8 -*-
import time, json, requests
import pandas as pd
from pyecharts.charts import Map
from pyecharts.charts import *
from pyecharts import options as opts
from pyecharts.charts import Page, WordCloud
from pyecharts.commons.utils import JsCode
from pyecharts.globals import ThemeType, ChartType
from bs4 import BeautifulSoup

# -------------------------------------------------------------------------------------
# 第一步：读取数据
# -------------------------------------------------------------------------------------
# 由于世界的数据里没有中国只能手动加入
url = 'https://view.inews.qq.com/g2/getOnsInfo?name=disease_h5&callback=&_=%d' % int(time.time() * 1000)
data = json.loads(requests.get(url=url).json()['data'])

lastUpdateTime = data['lastUpdateTime']
chinaTotal = data['chinaTotal']
chinaTotal['确诊'] = chinaTotal['confirm']
chinaTotal['疑似'] = chinaTotal['suspect']
chinaTotal['死亡'] = chinaTotal['dead']
chinaTotal['治愈'] = chinaTotal['heal']
del chinaTotal['confirm']
del chinaTotal['suspect']
del chinaTotal['dead']
del chinaTotal['heal']

url1 = "https://api.inews.qq.com/newsqa/v1/query/inner/publish/modules/list?modules=chinaDayList,chinaDayAddList,nowConfirmStatis,provinceCompare"
get_data = json.dumps(requests.get(url=url1).json()['data'])
data1 = json.loads(get_data)
# print(data1)

chinaDayList = pd.read_excel(time.strftime("%Y-%m-%d") + '-china_Day_list.xlsx')
globalDayList = pd.read_excel(time.strftime("%Y-%m-%d") + '-world_Day_list.xlsx')
chinaAddList = pd.read_excel(time.strftime("%Y-%m-%d") + '-china_DayAdd_list.xlsx')

chinaAdd = data1['chinaDayAddList']
chinaAdd_dict = {}
chinaAdd_dict['新增确诊'] = chinaAdd[-1]['confirm']
chinaAdd_dict['新增疑似'] = chinaAdd[-1]['suspect']
chinaAdd_dict['新增死亡'] = chinaAdd[-1]['dead']
chinaAdd_dict['新增治愈'] = chinaAdd[-1]['heal']
# print(chinaAdd_dict)

province_file = time.strftime("%Y-%m-%d") + "-province_list.xlsx"
city_file = time.strftime("%Y-%m-%d") + '-city_list.xlsx'
country_file = time.strftime("%Y-%m-%d") + '-world_list.xlsx'
worldVaccine_file = time.strftime("%Y-%m-%d") + '-worldVaccine_list.xlsx'
china_data = pd.read_excel(province_file)
city_data = pd.read_excel(city_file)
world_data = pd.read_excel(country_file)
worldVaccine_data=pd.read_excel(worldVaccine_file)
# 手动加入中国的累计确诊数据
world_name_list = list(world_data['国家英文名称'])#英文即各国的英文名称
world_name_list.append("China")
world_confirm_list = list(world_data['confirm'])#confirm即各国的累计确证数据
world_confirm_list.append(chinaTotal['确诊'])
list_china_data = list(zip(list(china_data['province']), list(china_data['confirm'])))
list_china_add_data = list(zip(list(china_data['province']), list(china_data['addconfirm'])))
list_world_data = list(zip(world_name_list, world_confirm_list))
list_worldVaccine_data=list(zip(list(worldVaccine_data['国家英文名称']), list(worldVaccine_data['疫苗总接种数'])))
print(list_china_data)
print(list_world_data)

# list_zh_world_data用来制作世界疫情中文词云图
world_zh_name_list = list(world_data['国家'])
world_zh_name_list.append("中国")
list_zh_world_data = list(zip(world_zh_name_list, world_confirm_list))
print(list_zh_world_data)

# list_city_data用来制作中国疫情城市词云图
list_city_data = list(zip(list(city_data['city']), list(city_data['confirm'])))

# [('台湾', 2262), ('香港', 11826), ('上海', 2041), ('广东', 2397), ..., ('甘肃', 193), ('青海', 18)]


# -------------------------------------------------------------------------------------
# 第二步：绘制全国疫情地图
# 参考文章：https://blog.csdn.net/shineych/article/details/104231072 [shineych大神]
# -------------------------------------------------------------------------------------
# def map_cn_disease_dis() -> Map:  # ->指函数返回Map()对象
china_map = (
    Map()
        .add('中国', list_china_data, 'china')
        .set_global_opts(
        title_opts=opts.TitleOpts(title='全国新型冠状病毒疫情地图（确诊数）'),
        visualmap_opts=opts.VisualMapOpts(is_show=True,
                                          split_number=6,
                                          is_piecewise=True,  # 是否为分段型
                                          pos_top='center',
                                          pieces=[
                                              {'min': 10000, 'color': '#7f1818'},  # 不指定 max
                                              {'min': 1000, 'max': 10000},
                                              {'min': 500, 'max': 999},
                                              {'min': 100, 'max': 499},
                                              {'min': 10, 'max': 99},
                                              {'min': 0, 'max': 5}],
                                          ),
    )
)

#china_map.render('全国疫情地图.html')

# china_map2 = (
#     Map()
#         .add('中国', list_china_add_data, 'china')
#         .set_global_opts(
#         title_opts=opts.TitleOpts(title='全国新型冠状病毒疫情地图（确诊数）'),
#         visualmap_opts=opts.VisualMapOpts(is_show=True,
#                                           split_number=6,
#                                           is_piecewise=True,  # 是否为分段型
#                                           pos_top='center',
#                                           pieces=[
#                                               {'min': 10000, 'color': '#7f1818'},  # 不指定 max
#                                               {'min': 1000, 'max': 10000},
#                                               {'min': 500, 'max': 999},
#                                               {'min': 100, 'max': 499},
#                                               {'min': 10, 'max': 99},
#                                               {'min': 0, 'max': 5}],
#                                           ),
#     )
# )
# def map_wd_disease_dis() -> Map:  # ->指函数返回Map()对象
world_map = (
    Map()
        .add('世界', list_world_data, 'world')
        .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
        .set_global_opts(
        title_opts=opts.TitleOpts(title='世界（162个国家）新型冠状病毒疫情地图（确诊数）'),
        visualmap_opts=opts.VisualMapOpts(
            is_show=True,
            split_number=6,
            is_piecewise=True,  # 是否为分段型
            # background_color="transparent",
            pos_top='center',
            pieces=[
                {'min': 1000000, 'color': '#7f1818'},  # 不指定 max
                {'min': 100000, 'max': 999999},
                {'min': 50000, 'max': 99999},
                {'min': 10000, 'max': 49999},
                {'min': 1000, 'max': 9999},
                {'min': 0, 'max': 500}],
        ),
    )
)

#world_map.render("世界疫情地图.html")

worldVaccine_map = (
    Map()
        .add('世界', list_worldVaccine_data, 'world')
        .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
        .set_global_opts(
        title_opts=opts.TitleOpts(title='世界（162个国家）疫苗接种地图（疫苗总接种数）'),
        visualmap_opts=opts.VisualMapOpts(
            max_=0,
            min_=100000000,
            # is_show=True,
            # split_number=6,
            # is_piecewise=True,  # 是否为分段型
            # # background_color="transparent",
            # pos_top='center',
            # pieces=[
            #     {'min': 0, 'max': 50000} ,
            #     {'min': 100000, 'max': 999999},
            #     {'min': 1000000, 'max': 4999999},
            #     {'min': 5000000, 'max': 9999999},
            #     {'min': 10000000, 'max': 99999999},
            #     {'min': 100000000}  ],# 不指定 max
        ),
    )
)

#worldVaccine_map.render("世界疫苗接种地图.html")

total_pie = (
    Pie(init_opts=opts.InitOpts(theme=ThemeType.LIGHT, width='500px', height='350px', bg_color="transparent"))
        .add("", [list(z) for z in zip(['确     诊  ', '疑     似  ', '死     亡  ', '治     愈  '], chinaTotal.values())],
             center=["50%", "60%"], radius=[75, 100], )
        .add("", [list(z) for z in zip(chinaAdd_dict.keys(), chinaAdd_dict.values())], center=["50%", "60%"],
             radius=[0, 50])
        .set_global_opts(title_opts=opts.TitleOpts(title="全国总量", subtitle=("截止" + lastUpdateTime), pos_bottom=0,
                                                   title_textstyle_opts=opts.TextStyleOpts(color="#00FFFF")),
                         )
        .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}:{c}")))

#total_pie.render("中国数据饼图.html")

line1 = Line(init_opts=opts.InitOpts(theme=ThemeType.WESTEROS))
line1.add_xaxis(list(globalDayList["date"]))
line1.add_yaxis("治愈", list(globalDayList["heal"]), is_smooth=True)
line1.add_yaxis("死亡", list(globalDayList["dead"]), is_smooth=True)
line1.add_yaxis("治愈率", list(globalDayList["healRate(%)"]), is_smooth=True)
line1.add_yaxis("死亡率", list(globalDayList["deadRate(%)"]), is_smooth=True)
line1.set_global_opts(title_opts=opts.TitleOpts(title="全球治愈与死亡趋势"))
line1.set_series_opts(label_opts=opts.LabelOpts(is_show=True))

#line1.render("全球治愈死亡趋势.html")

line1_1 = (
    Line(init_opts=opts.InitOpts(theme=ThemeType.WESTEROS))
        .add_xaxis(list(globalDayList["date"]))
        .add_yaxis("累计确诊", list(globalDayList["confirm"]), is_smooth=True)
        .add_yaxis("新增确诊", list(globalDayList["newAddConfirm"]), is_smooth=True)
        .set_global_opts(title_opts=opts.TitleOpts(title="全球确诊趋势"))
)

line2 = Line(init_opts=opts.InitOpts(theme=ThemeType.WESTEROS))
line2.add_xaxis(list(chinaDayList["date"]))
line2.add_yaxis("本土新增", list(chinaAddList["localConfirmadd"]), is_smooth=True)
line2.add_yaxis("境外输入", list(chinaAddList["importedCase"]), is_smooth=True)
line2.set_global_opts(title_opts=opts.TitleOpts(title="国内本土新增与境外输入"))

#line2.render("国内本土新增与境外输入趋势.html")

line3 = Line(init_opts=opts.InitOpts(theme=ThemeType.WESTEROS))
line3.add_xaxis(list(chinaDayList["date"]))
line3.add_yaxis("本土现有无症状感染者", list(chinaDayList["noInfect"]), is_smooth=True)
line3.set_global_opts(title_opts=opts.TitleOpts(title="国内本土现有无症状感染者"))
line3.set_series_opts(label_opts=opts.LabelOpts(is_show=False))

#line3.render("国内本土现有无症状感染者趋势.html")

line4 = (
    Line(init_opts=opts.InitOpts(theme=ThemeType.CHALK, bg_color="transparent"))
        .add_xaxis(list(chinaAddList["date"]))
        .add_yaxis("确诊", list(chinaAddList["confirm"]), is_smooth=True, yaxis_index=1)
        .add_yaxis("疑似", list(chinaAddList["suspect"]), is_smooth=True, yaxis_index=1)
        .add_yaxis("死亡", list(chinaAddList["dead"]), is_smooth=True, yaxis_index=1)
        .add_yaxis("治愈", list(chinaAddList["heal"]), is_smooth=True, yaxis_index=1)
        .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
        .set_global_opts(title_opts=opts.TitleOpts(title="国内每日新增数据趋势"))
)

bar1 = (
    Bar(init_opts=opts.InitOpts(theme=ThemeType.WESTEROS, width='900px', height='400px'))
        .add_xaxis(list(chinaAddList["date"]))
        .add_yaxis("确诊", list(chinaAddList["confirm"]))
        .add_yaxis("疑似", list(chinaAddList["suspect"]))
        .add_yaxis("死亡", list(chinaAddList["dead"]))
        .add_yaxis("治愈", list(chinaAddList["heal"]))
        .extend_axis(yaxis=opts.AxisOpts(axislabel_opts=opts.LabelOpts(formatter="{value}")))
        .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
        .set_global_opts(title_opts=opts.TitleOpts(title="每日新增数据趋势"),
                         legend_opts=opts.LegendOpts(pos_left='center'),
                         yaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(formatter="{value}")),
                         datazoom_opts=opts.DataZoomOpts())
).overlap(line4)

#bar1.render("国内每日新增数据趋势.html")

line5 = (
    Line(init_opts=opts.InitOpts(theme=ThemeType.WESTEROS))
        .add_xaxis(list(chinaDayList["date"]))
        .add_yaxis("全国现有确诊", list(chinaDayList["nowConfirm"]), is_smooth=True)
        .add_yaxis("全国累计确诊", list(chinaDayList["confirm"]), is_smooth=True)
        .add_yaxis("全国累计治愈", list(chinaDayList["heal"]), is_smooth=True)
        .add_yaxis("全国累计死亡", list(chinaDayList["dead"]), is_smooth=True)
        .set_global_opts(title_opts=opts.TitleOpts(title="全国现有确诊"))
        .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
)
wordcloud1 = (
    WordCloud()
        .add("", list_china_data, word_size_range=[10,50], shape="circle")
        .set_global_opts(title_opts=opts.TitleOpts(title="省份疫情确诊词云"))
)

#wordcloud1.render("中国疫情确诊词云.html")

wordcloud2 = (
    WordCloud()
        .add("", list_city_data, word_size_range=[10, 50], shape="diamand")
        .set_global_opts(title_opts=opts.TitleOpts(title="城市疫情确诊词云"))
)

#wordcloud2.render("城市疫确诊词云.html")

wordcloud3 = (
    WordCloud()
        .add("", list_zh_world_data, word_size_range=[10, 50], shape="diamand")
    # .set_global_opts(title_opts=opts.TitleOpts(title="全球疫情确诊词云"))
)

#wordcloud3.render("世界疫情确诊词云.html")

page1 = (
    Page(page_title="趋势图")
        .add(line5)
        .add(line2)
        .add(line3)
        .add(bar1)
).render("趋势.html")

with open("趋势.html", "r+", encoding='utf-8') as html:
    html_bf = BeautifulSoup(html, 'lxml')
    divs = html_bf.select('.chart-container')
    divs[0]["style"] = "width:605px;height:274px;position:absolute;top:36px;left:10px;"
    divs[1]["style"] = "width:605px;height:274px;position:absolute;top:36px;right:10px;"
    divs[2]["style"] = "width:605px;height:274px;position:absolute;bottom:20px;left:0px;"
    divs[3]["style"] = "width:605px;height:274px;position:absolute;bottom:20px;right:0px;"
    body = html_bf.find("body")
    # body["style"] = "background-color:#333333;"
    html_new = str(html_bf)
    html.seek(0, 0)
    html.truncate()
    html.write(html_new)
    html.close()

page2 = (
    Page()
        .add(line1)
        .add(line1_1)
        .add(world_map)
        .add(wordcloud3)
).render("世界.html")

with open("世界.html", "r+", encoding='utf-8') as html:
    html_bf = BeautifulSoup(html, 'lxml')
    divs = html_bf.select('.chart-container')
    divs[0]["style"] = "width:390px;height:260px;position:absolute;top:0px;right:0px;"
    divs[1]["style"] = "width:390px;height:260px;position:absolute;bottom:0px;right:0px;"
    divs[2]["style"] = "width:900px;height:400px;position:absolute;top:0px;left:0px;"
    divs[3]["style"] = "width:900px;height:150px;position:absolute;bottom:0px;left:10px;"
    body = html_bf.find("body")
    # body["style"] = "background-color:#333333;"
    html_new = str(html_bf)
    html.seek(0, 0)
    html.truncate()
    html.write(html_new)
    html.close()

page3 = (
    Page()
        .add(china_map)
        .add(wordcloud1)
        .add(wordcloud2)
).render("中国.html")

with open("中国.html", "r+", encoding='utf-8') as html:
    html_bf = BeautifulSoup(html, 'lxml')
    divs = html_bf.select('.chart-container')
    divs[0]["style"] = "width:900px;height:500px;position:absolute;top:36px;left:10px;"
    divs[1]["style"] = "width:450px;height:300px;position:absolute;top:0px;right:10px;"
    divs[2]["style"] = "width:450px;height:300px;position:absolute;bottom:0px;right:10px;"
    body = html_bf.find("body")
    #body["style"] = "background-color:#333333;"
    html_new = str(html_bf)
    html.seek(0, 0)
    html.truncate()
    html.write(html_new)
    html.close()
