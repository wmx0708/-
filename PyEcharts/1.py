import time, json, requests
import pandas as pd
from pyecharts.charts import *
from pyecharts import options as opts
from pyecharts.charts import Page, WordCloud,Bar, Grid, Line,Map
from pyecharts.commons.utils import JsCode
from pyecharts.globals import ThemeType, ChartType
from bs4 import BeautifulSoup
from pyecharts.components import Table
from pyecharts.faker import Faker
from django.shortcuts import render
from django.http import HttpResponse

# China
# 抓取腾讯疫情实时json数据
url = 'https://view.inews.qq.com/g2/getOnsInfo?name=disease_h5&callback=&_=%d' % int(time.time() * 1000)
data = json.loads(requests.get(url=url).json()['data'])
#print(data)
# print(data.keys())

# 统计省份信息(34个省份 湖北 广东 河南 浙江 湖南 安徽....)
province_list = data['areaTree'][0]['children']  # province_list为省信息列表

china_province_list = []  # 以每个省的信息字典为列表元素的列表
china_city_list = []  # 以每个城市的信息字典为列表元素的列表
for a in range(len(province_list)):
    province = province_list[a]['name']  # 省名列表
    city_list = province_list[a]['children']  # 各省下城市列表
    # 创建省字典存储各省的总数据
    china_province_dict = {}
    china_province_dict['province'] = province  # 省名
    china_province_dict['province_today'] = province_list[a]['today']  # 省日更新数据
    china_province_dict['province_total'] = province_list[a]['total']  # 省累计数据
    china_province_list.append(china_province_dict)  # 将各省字典作为元素插入省列表
    for i in range(len(city_list)):
        # 创建城市列表存储省内各地区的数据
        china_city_dict = {}
        china_city_dict['province'] = province  # 城市所述省名
        china_city_dict['city'] = city_list[i]['name']  # 城市名称
        china_city_dict['city_today'] = city_list[i]['today']  # 城市日更新数据
        china_city_dict['city_total'] = city_list[i]['total']  # 城市累计数据
        china_city_list.append(china_city_dict)  # 将个城市字典作为元素插入城市列表
china_province_frame = pd.DataFrame(china_province_list)  # 构建省dataframe数据
china_city_frame = pd.DataFrame(china_city_list)  # 构建市dataframe数据

# 显示第一个省数据
# first_province = province_list[0]['children']  # 第一个省的地区各种数据
# for item in first_province:
#     print(item)
# else:
#     print("\n")


# 数据处理函数
def nowConfirm(x):  # 现有确诊
    nowConfirm = eval(str(x))['nowConfirm']
    return nowConfirm


def confirm(x):  # 累计确诊
    confirm = eval(str(x))['confirm']
    return confirm


def suspect(x):  # 疑似病例
    suspect = eval(str(x))['suspect']
    return suspect


def dead(x):  # 死亡病例
    dead = eval(str(x))['dead']
    return dead


def deadRate(x):  # 死亡率
    deadRate = eval(str(x))['deadRate']
    return deadRate


def heal(x):  # 治愈病例
    heal = eval(str(x))['heal']
    return heal


def healRate(x):  # 治愈率
    healRate = eval(str(x))['healRate']
    return healRate


def wzz(x):  # 无症状感染者
    wzz = eval(str(x))['wzz']
    return wzz


def wzz_add(x):  # 无症状感染者增加
    wzz_add = eval(str(x))['wzz_add']
    return wzz_add


china_province_frame['nowConfirm'] = china_province_frame['province_total'].map(nowConfirm)
china_province_frame['confirm'] = china_province_frame['province_total'].map(confirm)
china_province_frame['suspect'] = china_province_frame['province_total'].map(suspect)
china_province_frame['dead'] = china_province_frame['province_total'].map(dead)
china_province_frame['deadRate(%)'] = china_province_frame['province_total'].map(deadRate)
china_province_frame['heal'] = china_province_frame['province_total'].map(heal)
china_province_frame['healRate(%)'] = china_province_frame['province_total'].map(healRate)
china_province_frame['wzz'] = china_province_frame['province_total'].map(wzz)
china_province_frame['addconfirm'] = china_province_frame['province_today'].map(confirm)
china_province_frame['wzz_add'] = china_province_frame['province_today'].map(wzz_add)
china_province_frame = china_province_frame[['province', 'nowConfirm', 'confirm', 'suspect', 'dead',
                                             'deadRate(%)', 'heal', 'healRate(%)', 'wzz', 'addconfirm', 'wzz_add']]
#print(china_province_frame.head())
china_province_frame.to_excel(time.strftime("%Y-%m-%d") + '-province_list.xlsx', index=False)

china_city_frame['nowConfirm'] = china_city_frame['city_total'].map(nowConfirm)
china_city_frame['confirm'] = china_city_frame['city_total'].map(confirm)
china_city_frame['suspect'] = china_city_frame['city_total'].map(suspect)
china_city_frame['dead'] = china_city_frame['city_total'].map(dead)
china_city_frame['deadRate(%)'] = china_city_frame['city_total'].map(deadRate)
china_city_frame['heal'] = china_city_frame['city_total'].map(heal)
china_city_frame['healRate(%)'] = china_city_frame['city_total'].map(healRate)
china_city_frame['wzz'] = china_city_frame['city_total'].map(wzz)
china_city_frame['addconfirm'] = china_city_frame['city_today'].map(confirm)
china_city_frame = china_city_frame[['province', 'city', 'nowConfirm', 'confirm', 'suspect',
                                     'dead', 'deadRate(%)', 'heal', 'healRate(%)', 'wzz', 'addconfirm']]
#print(china_city_frame.head())
# china_city_frame.to_excel('C:\Python\Python38\PyEcharts\china_city_frame.xlsx', index=False)
china_city_frame.to_excel(time.strftime("%Y-%m-%d") + '-city_list.xlsx', index=False)
print("China")

# ChinaDay
url = 'https://api.inews.qq.com/newsqa/v1/query/inner/publish/modules/list?modules=chinaDayList,chinaDayAddList,nowConfirmStatis,provinceCompare=%d' % int(
    time.time() * 1000)
get_data = json.dumps(requests.get(url=url).json()['data'])
data = json.loads(get_data)
#print(data)

chinaDayList = []
for i in range(len(data['chinaDayList'])):
    chinaDay_dict = {}
    chinaDay_dict['date'] = data['chinaDayList'][i]['y'] + "." + data['chinaDayAddList'][i]['date']
    chinaDay_dict['importedCase'] = data['chinaDayList'][i]['importedCase']
    chinaDay_dict['confirm'] = data['chinaDayList'][i]['confirm']
    chinaDay_dict['localConfirm'] = data['chinaDayList'][i]['localConfirm']
    chinaDay_dict['nowConfirm'] = data['chinaDayList'][i]['nowConfirm']
    chinaDay_dict['localConfirmH5'] = data['chinaDayList'][i]['localConfirmH5']
    chinaDay_dict['noInfect'] = data['chinaDayList'][i]['noInfect']
    chinaDay_dict['noInfectH5'] = data['chinaDayList'][i]['noInfectH5']
    chinaDay_dict['suspect'] = data['chinaDayList'][i]['suspect']
    chinaDay_dict['heal'] = data['chinaDayList'][i]['heal']
    chinaDay_dict['healRate(%)'] = data['chinaDayList'][i]['healRate']
    chinaDay_dict['dead'] = data['chinaDayList'][i]['dead']
    chinaDay_dict['deadRate(%)'] = data['chinaDayList'][i]['deadRate']
    chinaDayList.append(chinaDay_dict)

china_day_frame = pd.DataFrame(chinaDayList)
china_day_frame.to_excel(time.strftime("%Y-%m-%d") + "-china_Day_list.xlsx", index=False)

chinaDayAddList = []
for i in range(len(data['chinaDayAddList'])):
    chinaDayAdd_dict = {}
    chinaDayAdd_dict['date'] = data['chinaDayAddList'][i]['y'] + "." + data['chinaDayAddList'][i]['date']
    chinaDayAdd_dict['importedCase'] = data['chinaDayAddList'][i]['importedCase']
    chinaDayAdd_dict['confirm'] = data['chinaDayAddList'][i]['confirm']
    chinaDayAdd_dict['localConfirmadd'] = data['chinaDayAddList'][i]['localConfirmadd']
    chinaDayAdd_dict['infect'] = data['chinaDayAddList'][i]['infect']
    chinaDayAdd_dict['localinfectionadd'] = data['chinaDayAddList'][i]['localinfectionadd']
    chinaDayAdd_dict['suspect'] = data['chinaDayAddList'][i]['suspect']
    chinaDayAdd_dict['heal'] = data['chinaDayAddList'][i]['heal']
    chinaDayAdd_dict['healRate(%)'] = data['chinaDayAddList'][i]['healRate']
    chinaDayAdd_dict['dead'] = data['chinaDayAddList'][i]['dead']
    chinaDayAdd_dict['deadRate(%)'] = data['chinaDayAddList'][i]['deadRate']
    chinaDayAddList.append(chinaDayAdd_dict)

china_dayAdd_frame = pd.DataFrame(chinaDayAddList)
china_dayAdd_frame.to_excel(time.strftime("%Y-%m-%d") + "-china_DayAdd_list.xlsx", index=False)
print("ChinaDay")

# World
url = "https://api.inews.qq.com/newsqa/v1/automation/modules/list?modules=FAutoCountryConfirmAdd,WomWorld,WomAboard"
get_data = json.dumps(requests.get(url=url).json()['data'])
data = json.loads(get_data)
#print(data)

world_list = []
world_data = data['WomAboard']
for i in range(len(world_data)):
    world_dict = {}
    world_dict['国家'] = world_data[i]['name']
    world_dict['所属洲'] = world_data[i]['continent']
    world_dict['日期'] = world_data[i]['y'] + world_data[i]['date']
    world_dict['confirm'] = world_data[i]['confirm']
    world_dict['confirmAdd'] = world_data[i]['confirmAdd']
    world_dict['suspect'] = world_data[i]['suspect']
    world_dict['dead'] = world_data[i]['dead']
    world_dict['heal'] = world_data[i]['heal']
    world_dict['nowConfirm'] = world_data[i]['nowConfirm']
    world_dict['confirmCompare'] = world_data[i]['confirmCompare']
    world_dict['nowConfirmCompare'] = world_data[i]['nowConfirmCompare']
    world_dict['healCompare'] = world_data[i]['healCompare']
    world_dict['deadCompare'] = world_data[i]['deadCompare']
    world_list.append(world_dict)
world_frame = pd.DataFrame(world_list)  # world_frame为整理好的全球疫情数据dataframe结构
world_name = pd.read_excel("世界各国中英文对照.xlsx")
# 将中英文对照的dataframe与world_frame合并
world_frame = pd.merge(world_frame, world_name, left_on="国家", right_on="国家中文名称", how="inner")
world_frame = world_frame[['国家', '国家英文名称', '所属洲', '日期', 'nowConfirm', 'confirm', 'confirmAdd', 'suspect', 'dead',
                           'heal', 'confirmCompare', 'nowConfirmCompare', 'deadCompare', 'healCompare']]
world_frame.to_excel(time.strftime("%Y-%m-%d") + '-world_list.xlsx', index=False)
print("World")

# WorldDay
url = 'https://api.inews.qq.com/newsqa/v1/automation/modules/list?modules=FAutoGlobalStatis,' \
      'FAutoGlobalDailyList,FAutoCountryConfirmAdd%d' % int(time.time() * 1000)
get_data = json.dumps(requests.get(url=url).json()['data'])
data = json.loads(get_data)
#print(data)

worldDayList = []
for i in range(len(data['FAutoGlobalDailyList'])):
    worldDay_dict = {}
    worldDay_dict['date'] = data['FAutoGlobalDailyList'][i]['y'] + "." + data['FAutoGlobalDailyList'][i]['date']
    worldDay_dict['confirm'] = data['FAutoGlobalDailyList'][i]['all']['confirm']
    worldDay_dict['newAddConfirm'] = data['FAutoGlobalDailyList'][i]['all']['newAddConfirm']
    worldDay_dict['heal'] = data['FAutoGlobalDailyList'][i]['all']['heal']
    worldDay_dict['healRate(%)'] = data['FAutoGlobalDailyList'][i]['all']['healRate']
    worldDay_dict['dead'] = data['FAutoGlobalDailyList'][i]['all']['dead']
    worldDay_dict['deadRate(%)'] = data['FAutoGlobalDailyList'][i]['all']['deadRate']
    worldDayList.append(worldDay_dict)

world_day_frame = pd.DataFrame(worldDayList)
world_day_frame.to_excel(time.strftime("%Y-%m-%d") + "-world_Day_list.xlsx", index=False)
print("WorldDay")

# ChinaDayVaccine
url = 'https://api.inews.qq.com/newsqa/v1/automation/modules/list?modules=ChinaVaccineTrendData'
get_data = json.dumps(requests.get(url=url).json()['data'])
data = json.loads(get_data)
#print(data)

chinaDayVaccine = []
for i in range(len(data['ChinaVaccineTrendData'])):
    chinaDayVaccine_dict = {}
    chinaDayVaccine_dict['date'] = data['ChinaVaccineTrendData'][i]['y'] + "." + data['ChinaVaccineTrendData'][i][
        'date']
    chinaDayVaccine_dict['total_vaccinations'] = data['ChinaVaccineTrendData'][i]['total_vaccinations']
    chinaDayVaccine_dict['total_vaccinations_per_hundred'] = data['ChinaVaccineTrendData'][i][
        'total_vaccinations_per_hundred']
    chinaDayVaccine.append(chinaDayVaccine_dict)

china_day_frame = pd.DataFrame(chinaDayVaccine)
china_day_frame.to_excel(time.strftime("%Y-%m-%d") + "-china_DayVaccine_list.xlsx", index=False)
print("ChinaDayVaccine")

# WorldVaccine
url = "https://api.inews.qq.com/newsqa/v1/automation/modules/list?modules=VaccineSituationData"
get_data = json.dumps(requests.get(url=url).json()['data'])
data = json.loads(get_data)
#print(data)

worldVaccine_list = []
worldVaccine_data = data['VaccineSituationData']
for i in range(len(worldVaccine_data)):
    worldVaccine_dict = {}
    worldVaccine_dict['国家'] = worldVaccine_data[i]['country']
    worldVaccine_dict['日期'] = worldVaccine_data[i]['date']
    worldVaccine_dict['疫苗'] = worldVaccine_data[i]['vaccinations']
    worldVaccine_dict['疫苗总接种数'] = worldVaccine_data[i]['total_vaccinations']
    worldVaccine_dict['每百人疫苗总接种数'] = worldVaccine_data[i]['total_vaccinations_per_hundred']
    worldVaccine_list.append(worldVaccine_dict)
worldVaccine_frame = pd.DataFrame(worldVaccine_list)  # world_frame为整理好的全球疫情数据dataframe结构
world_name = pd.read_excel("世界各国中英文对照.xlsx")
# 将中英文对照的dataframe与world_frame合并
worldVaccine_frame = pd.merge(worldVaccine_frame, world_name, left_on="国家", right_on="国家中文名称", how="inner")
worldVaccine_frame = worldVaccine_frame[['国家', '国家英文名称', '日期', '疫苗', '疫苗总接种数', '每百人疫苗总接种数', ]]
worldVaccine_frame.to_excel(time.strftime("%Y-%m-%d") + '-worldVaccine_list.xlsx', index=False)
print("WorldVaccine")

#visualization
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

chinaDayList = pd.read_excel(time.strftime("%Y-%m-%d") + '-china_Day_list.xlsx')
globalDayList = pd.read_excel(time.strftime("%Y-%m-%d") + '-world_Day_list.xlsx')
chinaAddList = pd.read_excel(time.strftime("%Y-%m-%d") + '-china_DayAdd_list.xlsx')

chinaAdd_dict = {}
chinaAdd_dict['新增确诊'] = data["chinaAdd"]['confirm']
chinaAdd_dict['新增疑似'] = data["chinaAdd"]['suspect']
chinaAdd_dict['新增死亡'] = data["chinaAdd"]['dead']
chinaAdd_dict['新增治愈'] = data["chinaAdd"]['heal']

province_file = time.strftime("%Y-%m-%d") + "-province_list.xlsx"
city_file = time.strftime("%Y-%m-%d") + '-city_list.xlsx'
country_file = time.strftime("%Y-%m-%d") + '-world_list.xlsx'
China_DayVaccine_file = time.strftime("%Y-%m-%d") + '-china_DayVaccine_list.xlsx'
worldVaccine_file = time.strftime("%Y-%m-%d") + '-worldVaccine_list.xlsx'
china_data = pd.read_excel(province_file)
city_data = pd.read_excel(city_file)
world_data = pd.read_excel(country_file)
China_DayVaccine_data=pd.read_excel(China_DayVaccine_file)
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
# print(list_china_data)
# print(list_world_data)

# list_zh_world_data用来制作世界疫情中文词云图
world_zh_name_list = list(world_data['国家'])
world_zh_name_list.append("中国")
list_zh_world_data = list(zip(world_zh_name_list, world_confirm_list))
#print(list_zh_world_data)

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
china_map.chart_id="china_map"

# def map_wd_disease_dis() -> Map:  # ->指函数返回Map()对象
world_map = (
    Map()
        .add('全球确诊', list_world_data, 'world')
        .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
        .set_global_opts(legend_opts=opts.LegendOpts(pos_right="20%"),
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
world_map.chart_id="world_map"

#world_map.render("世界疫情地图.html")

worldVaccine_map = (
    Map()
        .add('世界', list_worldVaccine_data, 'world')
        .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
        .set_global_opts(legend_opts=opts.LegendOpts(pos_right="20%"),
        title_opts=opts.TitleOpts(title='世界（162个国家）疫苗接种地图（疫苗总接种数）'),
        visualmap_opts=opts.VisualMapOpts(
            max_=0,
            min_=100000000,
        ),
    )
)
worldVaccine_map.chart_id="worldVaccine_map"

#worldVaccine_map.render("世界疫苗接种地图.html")

funnel_list=[]
for i in range(10):
    funnel_list.append(list_worldVaccine_data[i])

funnel = (
    Funnel()
   .add("全球疫苗总接种数",funnel_list,sort_="ascending")
   #.set_global_opts(title_opts=opts.TitleOpts(title="漏斗图示例"))
   .set_series_opts(label_opts=opts.LabelOpts(position="inside"))
)
funnel.chart_id="funnel"

#funnel.render("漏斗图.html")

total_pie = (
    Pie(init_opts=opts.InitOpts(theme=ThemeType.LIGHT, width='500px', height='350px', bg_color="transparent"))
        .add("", [list(z) for z in zip(['确     诊  ', '死     亡  ',  '治     愈  ','疑     似  '],
                                       [chinaTotal["确诊"],chinaTotal["死亡"],chinaTotal["治愈"],chinaTotal["疑似"]])],
             center=["50%", "60%"], radius=[75, 100], )
        .add("", [list(z) for z in zip(chinaAdd_dict.keys(), chinaAdd_dict.values())], center=["50%", "60%"],
             radius=[0, 50])
        .set_global_opts(title_opts=opts.TitleOpts(title="全国总量", subtitle=("截止至" + lastUpdateTime), pos_top=0,pos_left="50%",
                                                   title_textstyle_opts=opts.TextStyleOpts(color="#00FFFF")),
                         legend_opts=opts.LegendOpts(pos_left="0%",orient="vertical"),
                         )
        .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}:{c}")))
total_pie.chart_id="total_pie"

#total_pie.render("中国数据饼图.html")

y1list=[i/1000000 for i in list(globalDayList["heal"])]
y2list=[i/1000000 for i in list(globalDayList["dead"])]
line1 = (
    Line(init_opts=opts.InitOpts(theme=ThemeType.WESTEROS))
    .add_xaxis(list(globalDayList["date"]))
    .add_yaxis("治愈（百万）", y1list, is_smooth=True)
    .add_yaxis("死亡（百万）", y2list, is_smooth=True)
    # .add_yaxis("治愈率", list(globalDayList["healRate(%)"]), is_smooth=True)
    # .add_yaxis("死亡率", list(globalDayList["deadRate(%)"]), is_smooth=True)
    .set_global_opts(title_opts=opts.TitleOpts(title="全球治愈与死亡趋势"))
    .set_series_opts(label_opts=opts.LabelOpts(is_show=True))
)
line1.chart_id="line1"

#line1.render("全球治愈死亡趋势.html")

y1list=[i/10000 for i in list(globalDayList["confirm"])]
y2list=[i/10000 for i in list(globalDayList["newAddConfirm"])]
line1_1 = (
    Line(init_opts=opts.InitOpts(theme=ThemeType.WESTEROS))
        .add_xaxis(list(globalDayList["date"]))
        .add_yaxis("累计确诊(万）", y1list, is_smooth=True)
        .add_yaxis("新增确诊（万）", y2list, is_smooth=True)
        .set_global_opts(title_opts=opts.TitleOpts(title="全球确诊趋势"))
)
line1_1.chart_id="line1_1"

line2 = (
    Line(init_opts=opts.InitOpts(theme=ThemeType.WESTEROS))
    .add_xaxis(list(chinaDayList["date"]))
    .add_yaxis("本土新增", list(chinaAddList["localConfirmadd"]), is_smooth=True)
    .add_yaxis("境外输入", list(chinaAddList["importedCase"]), is_smooth=True)
    #.add_yaxis("本土现有无症状感染者", list(chinaDayList["noInfect"]), is_smooth=True)
    .set_global_opts(title_opts=opts.TitleOpts(title="国内疫情增加"))
    .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
)
line2.chart_id="line2"

#line2.render("国内本土新增与境外输入趋势.html")

# line3 = (
#     Line(init_opts=opts.InitOpts(theme=ThemeType.WESTEROS))
#     .add_xaxis(list(chinaDayList["date"]))
#     .add_yaxis("本土现有无症状感染者", list(chinaDayList["noInfect"]), is_smooth=True)
#     .set_global_opts(title_opts=opts.TitleOpts(title="国内本土现有无症状感染者"))
#     .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
# )
# line3.chart_id="line3"

#line3.render("国内本土现有无症状感染者趋势.html")

line3 = (
    Line(init_opts=opts.InitOpts(theme=ThemeType.WESTEROS))
    .add_xaxis(list(chinaDayList["date"]))
    .add_yaxis("治愈率", list(chinaDayList["healRate(%)"]), is_smooth=True)
    .add_yaxis("死亡率", list(chinaDayList["deadRate(%)"]), is_smooth=True)
    .set_global_opts(title_opts=opts.TitleOpts(title="国内治愈率与死亡率"))
    .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
)
line3.chart_id="line3"

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
line4.chart_id="line4"


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
bar1.chart_id="bar1"

#bar1.render("国内每日新增数据趋势.html")

line5 = (
    Line(init_opts=opts.InitOpts(theme=ThemeType.WESTEROS))
        .add_xaxis(list(chinaDayList["date"]))
        .add_yaxis("      全国现有确诊", list(chinaDayList["nowConfirm"]), is_smooth=True)
        .add_yaxis("      全国累计确诊", list(chinaDayList["confirm"]), is_smooth=True)
        .add_yaxis("\n      全国累计治愈", list(chinaDayList["heal"]), is_smooth=True)
        .add_yaxis("\n      全国累计死亡", list(chinaDayList["dead"]), is_smooth=True)
        .set_global_opts(title_opts=opts.TitleOpts(title="国内疫情"))
        .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
)
line5.chart_id="line5"

ylist=[i/10000000 for i in list(China_DayVaccine_data["total_vaccinations"])]
line6=(
    Line(init_opts=opts.InitOpts(theme=ThemeType.WESTEROS))
    .add_xaxis(list(China_DayVaccine_data["date"]))
    .add_yaxis("\n\n全国疫苗总接种数（千万）",ylist,is_smooth=True)
    .set_global_opts(title_opts=opts.TitleOpts(title="全国每日疫苗接种趋势"),
                     yaxis_opts=opts.AxisOpts(name_location="middle",name_gap=30)

)
    # .set_series_opts(areastyle_opts=opts.AreaStyleOpts(opacity=0.5),
    #                  label_opts=opts.LabelOpts(is_show=False))
)
line6.chart_id="line6"



url1 = "https://api.inews.qq.com/newsqa/v1/automation/modules/list?modules=VaccineTopData"
get_data = json.dumps(requests.get(url=url1).json()['data'])
data = json.loads(get_data)

china_total_vaccinations_per_hundred = (Pie().
            set_global_opts(title_opts=opts.TitleOpts(title="我国每百人疫苗总接种数", pos_left='center', pos_top='center',
                                                      title_textstyle_opts=opts.TextStyleOpts(color='#000000'))))
china_total_vaccinations_per_hundred.chart_id="china_total_vaccinations_per_hundred"
china_total_vaccinations_per_hundred_num = (Pie().
                   set_global_opts(title_opts=opts.TitleOpts(title=(str(data["VaccineTopData"]["中国"]['total_vaccinations_per_hundred']) + "   "),
                                                             pos_top='15%', pos_left='center',
                                                             subtitle=("新增疫苗接种数: " + str(data["VaccineTopData"]["中国"]['new_vaccinations'])),
                                                             item_gap=1,
                                                             title_textstyle_opts=opts.TextStyleOpts(color="#FFFFFF",
                                                                                                     font_size=30),
                                                             subtitle_textstyle_opts=opts.TextStyleOpts(color="#FFFFFF")
                                                             )))
china_total_vaccinations_per_hundred_num.chart_id="china_total_vaccinations_per_hundred_num"

world_total_vaccinations_per_hundred = (Pie().
            set_global_opts(title_opts=opts.TitleOpts(title="全球每百人疫苗总接种数", pos_left='center', pos_top='center',
                                                      title_textstyle_opts=opts.TextStyleOpts(color='#000000',
                                                                                              border_width=4,
                                                                                              border_color="#000000",
                                                                                              border_radius=[25,0,0,0],))))
world_total_vaccinations_per_hundred.chart_id="world_total_vaccinations_per_hundred"
world_total_vaccinations_per_hundred_num = (Pie().
                   set_global_opts(title_opts=opts.TitleOpts(title=(str(data["VaccineTopData"]["全球"]['total_vaccinations_per_hundred']) + "   "),
                                                             pos_top='15%', pos_left='center',
                                                             subtitle=("新增疫苗接种数: " + str(data["VaccineTopData"]["全球"]['new_vaccinations'])),
                                                             item_gap=1,
                                                             title_textstyle_opts=opts.TextStyleOpts(color="#FFFFFF",
                                                                                                     font_size=30),
                                                             subtitle_textstyle_opts=opts.TextStyleOpts(color="#FFFFFF")
                                                             )))
world_total_vaccinations_per_hundred_num.chart_id="world_total_vaccinations_per_hundred_num"

lq1 = (
    Liquid()  # 下面确定名称，比例，是否显示轮廓，形状
    .add(str(list_worldVaccine_data[0][0]),
         [float(list_worldVaccine_data[0][1])/float(data["VaccineTopData"]["全球"]['total_vaccinations'])],
         color=["#c23531"], background_color="#ff9966",
         outline_itemstyle_opts={"color": "#ff9966"},
         label_opts=opts.LabelOpts(font_size=15, color="#c23531", position="inside", border_color="#c23531"))
    .set_global_opts(title_opts=opts.TitleOpts(title=str(list_worldVaccine_data[0][0])
                                               ,pos_left="center",pos_bottom="0%",
                                               title_textstyle_opts=opts.TextStyleOpts(font_size=20,color="#c23531")))
)
lq1.chart_id="lq1"

lq2= (
    Liquid()  # 下面确定名称，比例，是否显示轮廓，形状
    .add(str(list_worldVaccine_data[1][0]),
         [float(list_worldVaccine_data[1][1])/float(data["VaccineTopData"]["全球"]['total_vaccinations'])],
         color=["#2f4554"], background_color="#99CCFF",
         outline_itemstyle_opts={"color": "#99CCFF"},
         label_opts=opts.LabelOpts(font_size=15, color="#2f4554", position="inside", border_color="#c23531"))
    .set_global_opts(title_opts=opts.TitleOpts(title=str(list_worldVaccine_data[1][0])
                                               ,pos_left="center",pos_bottom="0%",
                                               title_textstyle_opts=opts.TextStyleOpts(font_size=20,color="#2f4554")))
)
lq2.chart_id="lq2"

lq3 = (
    Liquid()  # 下面确定名称，比例，是否显示轮廓，形状
    .add(str(list_worldVaccine_data[2][0]),
         [float(list_worldVaccine_data[2][1])/float(data["VaccineTopData"]["全球"]['total_vaccinations'])],
         color=["#61a0a8"], background_color="#F0FFFF",
         outline_itemstyle_opts={"color": "#F0FFFF"},
         label_opts=opts.LabelOpts(font_size=15, color="#61a0a8", position="inside", border_color="#c23531"))
    .set_global_opts(title_opts=opts.TitleOpts(title=str(list_worldVaccine_data[2][0]).replace(' ','\n')
                                               ,pos_left="center",pos_bottom="-6%",
                                               title_textstyle_opts=opts.TextStyleOpts(font_size=20,color="#61a0a8")))
)
lq3.chart_id="lq3"

lq4 = (
    Liquid()  # 下面确定名称，比例，是否显示轮廓，形状
    .add(str(list_worldVaccine_data[3][0]),
         [float(list_worldVaccine_data[3][1])/float(data["VaccineTopData"]["全球"]['total_vaccinations'])],
         color=["#D48265"], background_color="#FFD39B",
         outline_itemstyle_opts={"color": "#FFD39B"},
         label_opts=opts.LabelOpts(font_size=15, color="#D48265", position="inside", border_color="#c23531"))
    .set_global_opts(title_opts=opts.TitleOpts(title=str(list_worldVaccine_data[3][0])
                                               ,pos_left="center",pos_bottom="0%",
                                               title_textstyle_opts=opts.TextStyleOpts(font_size=20,color="#FFD39B")))
)
lq4.chart_id="lq4"


wordcloud1 = (
    WordCloud()
        .add("", list_china_data, word_size_range=[10,50], shape="circle")
        .set_global_opts(title_opts=opts.TitleOpts(title="省份疫情确诊词云"))
)
wordcloud1.chart_id="wordcloud1"

#wordcloud1.render("中国疫情确诊词云.html")

#清洗词云数据
wash_list=[]
for i in range(len(list(city_data['city']))):
    if city_data['city'][i]=="地区待确认"or city_data['city'][i]=="境外输入":
        wash_list.append(i)
for i in range(len(wash_list)):
    list_city_data.pop(wash_list[i]-i)

wordcloud2 = (
    WordCloud()
        .add("", list_city_data, word_size_range=[10, 50], shape="diamand")
        .set_global_opts(title_opts=opts.TitleOpts(title="城市疫情确诊词云"))
)
wordcloud2.chart_id="wordcloud2"

#wordcloud2.render("城市疫确诊词云.html")

wordcloud3 = (
    WordCloud()
        .add("", list_zh_world_data, word_size_range=[10, 50], shape="diamand")
    # .set_global_opts(title_opts=opts.TitleOpts(title="全球疫情确诊词云"))
)
wordcloud3.chart_id="wordcloud3"

#wordcloud3.render("世界疫情确诊词云.html")

page4_title = (
    Pie()
        .set_global_opts(
        title_opts=opts.TitleOpts(title="2021-疫苗接种",
                                  title_textstyle_opts=opts.TextStyleOpts(font_size=40, color='#000',
                                                                          border_radius=True, border_color="white"),
                                  pos_top=0)))
page4_title.chart_id="page4_title"

times = (
    Pie()
        .set_global_opts(
        title_opts=opts.TitleOpts(subtitle=("截至 " + lastUpdateTime),
                                  subtitle_textstyle_opts=opts.TextStyleOpts(font_size=13, color='#000'),
                                  pos_top=0))
)
times.chart_id="times"

page1 = (
    Page(page_title="疫情趋势展示")
        .add(total_pie)
        .add(line2)
        .add(bar1)
        .add(line3)
).render("趋势.html")#.render("page1.html")
#Page.save_resize_html("page1.html", cfg_file="chart_config.json", dest="趋势.html")

with open("趋势.html", "r+", encoding='utf-8') as html:
    html_bf = BeautifulSoup(html, 'lxml')
    divs = html_bf.select('.chart-container')
    divs[0]["style"] = "width:605px;height:274px;position:absolute;top:0px;left:10px;"
    divs[1]["style"] = "width:605px;height:274px;position:absolute;top:0px;right:10px;"
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
    Page(layout=Page.DraggablePageLayout,page_title="全球疫情展示图")
        .add(line1)
        .add(line1_1)
        .add(world_map)
        .add(wordcloud3)
).render("page2.html")
Page.save_resize_html("page2.html", cfg_file="chart_config(1).json", dest="世界.html")

# with open("世界.html", "r+", encoding='utf-8') as html:
#     html_bf = BeautifulSoup(html, 'lxml')
#     divs = html_bf.select('.chart-container')
#     divs[0]["style"] = "width:390px;height:260px;position:absolute;top:0px;right:0px;"
#     divs[1]["style"] = "width:390px;height:260px;position:absolute;bottom:0px;right:0px;"
#     divs[2]["style"] = "width:900px;height:400px;position:absolute;top:0px;left:0px;"
#     divs[3]["style"] = "width:900px;height:150px;position:absolute;bottom:0px;left:10px;"
#     body = html_bf.find("body")
#     # body["style"] = "background-color:#333333;"
#     html_new = str(html_bf)
#     html.seek(0, 0)
#     html.truncate()
#     html.write(html_new)
#     html.close()

page3 = (
    Page(page_title="全国疫情展示图")
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

page4 = (
    Page(layout=Page.DraggablePageLayout,page_title="疫苗接种情况展示")
    .add(worldVaccine_map)
    .add(funnel)
    .add(line6)
    .add(china_total_vaccinations_per_hundred)
    .add(china_total_vaccinations_per_hundred_num)
    .add(world_total_vaccinations_per_hundred)
    .add(world_total_vaccinations_per_hundred_num)
    .add(page4_title)
    .add(times)
    .add(lq1)
    .add(lq2)
    .add(lq3)
    .add(lq4)
).render("page4.html")
Page.save_resize_html("page4.html", cfg_file="chart_config(3).json", dest="疫苗.html")

with open("疫苗.html", "r+", encoding='utf-8') as html:
    html_bf = BeautifulSoup(html, 'lxml')
    divs = html_bf.select('.chart-container')
    divs[3]["style"] = "width:220px;height:31px;position:absolute;top:22px;left:920px;border-top:3px solid #000;background:#CCC; border-radius:25px 0px 0px 0px;"
    divs[4]["style"] = "width:220px;height:62px;position:absolute;top:56px;left:920px;border-style:solid;border-color:black;border-width:3px;background:#AAA"
    divs[5]["style"] = "width:220px;height:31px;position:absolute;top:121px;left:920px;border-style:solid;border-color:#DC143C;border-width:3px;background:#CCC"
    divs[6]["style"] = "width:220px;height:62px;position:absolute;top:155px;left:920px;border-style:solid;border-color:#DC143C;border-width:3px;background:	#AAA;border-radius:0px 0px 25px 0px;"
    body = html_bf.find("body")
    #body["style"] = "background-color:#333333;"
    html_new = str(html_bf)
    html.seek(0, 0)
    html.truncate()
    html.write(html_new)
    html.close()



print("Finished\(^o^)/!")