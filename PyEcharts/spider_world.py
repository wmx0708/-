# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# 第一步：抓取数据
# ------------------------------------------------------------------------------
import time, json, requests
import pandas as pd
import numpy as np

# pd.set_option('display.max_rows', None)#显示所有行
# pd.set_option('display.max_columns', None)#显示所有列
# 抓取腾讯疫情实时json数据
url = 'https://view.inews.qq.com/g2/getOnsInfo?name=disease_foreign&callback=&_=%d' % int(time.time() * 1000)
data = json.loads(requests.get(url=url).json()['data'])
# print(data)
# print(data.keys())

# lastUpdateTime=data['lastUpdateTime']
# chinaTotal=data['chinaTotal']
# chinaAdd=data['chinaAdd']
# print(lastUpdateTime)
# print(chinaTotal)
# print(chinaAdd)

# 统计国家信息(161个国家 美国 西班牙 法国 秘鲁 英国 意大利 德国 伊朗....)
country_list = data['foreignList']  # country_list为各国信息列表
# print(len(country_list))
# for item in country_list:
#     print(item['name'], end=" ")  # 不换行
# else:
#     print("\n")  # 换行
world_country_list = []  # 以每个国家的信息字典为元素的列表
#country_area_list = []  # 以每个国家的地区信息字典为元素的列表
for a in range(len(country_list)):
    country = country_list[a]['name']  # 各国名称列表
    # if 'childre' in country_list[a].keys():
    #     area_list = country_list[a]['children']  # 各国地区信息列表
    # else:
    #     area_list = []
    world_country_dict = {}  # 创建国字典存储各省的总数据
    world_country_dict['country'] = country  # 各国名称列表
    world_country_dict['continent'] = country_list[a]['continent']
    world_country_dict['date'] = country_list[a]['y'] +"."+ country_list[a]['date']
    world_country_dict['world_country'] = country_list[a]
    world_country_list.append(world_country_dict)  # 将各国信息字典作为元素插入国家列表
    #world_country_list.append(country_list[a])
    # if area_list != []:
    #     for i in range(len(area_list)):
    #         country_area_dict = {}  # 创建国家地区列表存储国家内各地区的数据
    #         country_area_dict['country'] = country  # 地区所属国家名称
    #         country_area_dict['area'] = area_list[i]['nameMap']  # 各省地区名
    #         country_area_dict['date'] = area_list[i]['date']
    #         country_area_dict['country_area'] = area_list[i]
    #         print(country_area_dict['country_area'])
    #         country_area_list.append(country_area_dict)  # 每一个字典的内容都是一行
    # else:
    #     continue
world_country_frame=pd.DataFrame(world_country_list)
#world_country_frame = pd.DataFrame(country_list)  # 创建国家dataframe数据
#country_area_frame = pd.DataFrame(country_area_list)  # 创建国家中的地区dataframe数据


#
# # 显示第一个省数据
# first_province = province_list[0]['children']  # 第一个省的地区各种数据
# for item in first_province:
#     print(item)
# else:
#     print("\n")
#
#
# 数据处理函数
def confirmAdd(x):  # 现有确诊
    confirmAdd = eval(str(x))['confirmAdd']
    return confirmAdd


def confirmCompare(x):  # 现有确诊
    confirmCompare = eval(str(x))['confirmCompare']
    return confirmCompare


def nowConfirm(x):  # 现有确诊
    nowConfirm = eval(str(x))['nowConfirm']
    return nowConfirm


def nowConfirmCompare(x):  # 现有确诊
    nowConfirmCompare = eval(str(x))['nowConfirmCompare']
    return nowConfirmCompare


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


def deadCompare(x):  # 现有确诊
    deadCompare = eval(str(x))['deadCompare']
    return deadCompare


def heal(x):  # 治愈病例
    heal = eval(str(x))['heal']
    return heal


def healRate(x):  # 治愈率
    healRate = eval(str(x))['healRate']
    return healRate


def wzz(x):  # 无症状感染者
    wzz = eval(str(x))['wzz']
    return wzz


def healCompare(x):  # 现有确诊
    healCompare = eval(str(x))['healCompare']
    return healCompare


def wzz_add(x):  # 无症状感染者增加
    wzz_add = eval(str(x))['wzz_add']
    return wzz_add


world_country_frame['nowConfirm'] = world_country_frame['world_country'].map(nowConfirm)
world_country_frame['nowConfirmCompare'] = world_country_frame['world_country'].map(nowConfirmCompare)
world_country_frame['confirm'] = world_country_frame['world_country'].map(confirm)
world_country_frame['confirmAdd'] = world_country_frame['world_country'].map(confirmAdd)
world_country_frame['confirmCompare'] = world_country_frame['world_country'].map(confirmCompare)
world_country_frame['suspect'] = world_country_frame['world_country'].map(suspect)
world_country_frame['dead'] = world_country_frame['world_country'].map(dead)
world_country_frame['deadCompare'] = world_country_frame['world_country'].map(deadCompare)
world_country_frame['heal'] = world_country_frame['world_country'].map(heal)
world_country_frame['healCompare'] = world_country_frame['world_country'].map(healCompare)
world_name = pd.read_excel("世界各国中英文对照.xlsx")
world_country_frame = pd.merge(world_country_frame,world_name,left_on ="country",right_on = "中文",how="inner")

world_country_frame = world_country_frame[['country','英文', 'continent','date', 'nowConfirm', 'nowConfirmCompare',
                                           'confirm', 'confirmAdd', 'confirmCompare', 'suspect', 'dead', 'deadCompare',
                                           'heal', 'healCompare']]
print(world_country_frame.head())
world_country_frame.to_excel(time.strftime("%Y-%m-%d")+'-country_list.xlsx', index=False)

# country_area_frame['confirmAdd'] = country_area_frame['country_area'].map(confirmAdd)
# country_area_frame['confirm'] = country_area_frame['country_area'].map(confirm)
# country_area_frame['suspect'] = country_area_frame['country_area'].map(suspect)
# country_area_frame['dead'] = country_area_frame['country_area'].map(dead)
# country_area_frame['heal'] = country_area_frame['country_area'].map(heal)
# country_area_frame = country_area_frame[['country', 'area', 'confirm', 'confirmAdd', 'suspect',
#                                          'dead', 'heal', ]]
# print(country_area_frame.head())
# country_area_frame.to_excel('C:\Python\Python38\PyEcharts\country_area_list.xlsx', index=False)


