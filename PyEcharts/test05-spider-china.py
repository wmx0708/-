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
url = 'https://view.inews.qq.com/g2/getOnsInfo?name=disease_h5&callback=&_=%d' % int(time.time() * 1000)
data = json.loads(requests.get(url=url).json()['data'])
print(data)
# print(data.keys())

# lastUpdateTime=data['lastUpdateTime']
#chinaTotal=data['chinaTotal']
# chinaAdd=data['chinaAdd']
# print(lastUpdateTime)
# print(chinaTotal)
# print(chinaAdd)

# 统计省份信息(34个省份 湖北 广东 河南 浙江 湖南 安徽....)
province_list = data['areaTree'][0]['children']  # province_list为省信息列表
# print(len(province_list))
# for item in province_list:
#     print(item['name'], end=" ")  # 不换行
# else:
#     print("\n")  # 换行
china_province_list = [] #以每个省的信息字典为列表元素的列表
china_city_list = [] #以每个城市的信息字典为列表元素的列表
for a in range(len(province_list)):
    province = province_list[a]['name'] #省名列表
    city_list = province_list[a]['children'] #各省下城市列表
    # 创建省字典存储各省的总数据
    china_province_dict = {}
    china_province_dict['province'] = province #省名
    china_province_dict['province_today'] = province_list[a]['today'] #省日更新数据
    china_province_dict['province_total'] = province_list[a]['total'] #省累计数据
    china_province_list.append(china_province_dict) #将各省字典作为元素插入省列表
    for i in range(len(city_list)):
        # 创建城市列表存储省内各地区的数据
        china_city_dict = {}
        china_city_dict['province'] = province #城市所述省名
        china_city_dict['city'] = city_list[i]['name'] #城市名称
        china_city_dict['city_today'] = city_list[i]['today'] #城市日更新数据
        china_city_dict['city_total'] = city_list[i]['total'] #城市累计数据
        china_city_list.append(china_city_dict)  #将个城市字典作为元素插入城市列表
china_province_frame = pd.DataFrame(china_province_list) #构建省dataframe数据
china_city_frame = pd.DataFrame(china_city_list) #构建市dataframe数据

# 显示第一个省数据
first_province = province_list[0]['children']  # 第一个省的地区各种数据
for item in first_province:
    print(item)
else:
    print("\n")


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
print(china_province_frame.head())
china_province_frame.to_excel(time.strftime("%Y-%m-%d")+'-province_list.xlsx', index=False)

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
print(china_city_frame.head())
#china_city_frame.to_excel('C:\Python\Python38\PyEcharts\china_city_frame.xlsx', index=False)
china_city_frame.to_excel(time.strftime("%Y-%m-%d")+'-city_list.xlsx', index=False)

# # 解析确诊数据
# provnice_confirm_data = {}
# for item in province_list:
#     if item['name'] not in provnice_confirm_data:
#         provnice_confirm_data.update({item['name']: 0})
#     for province_data in item['children']:  # province_data即各省的数据
#         provnice_confirm_data[item['name']] += int(province_data['total']['confirm'])
# print(provnice_confirm_data)
# # {'台湾': 2262, '香港': 11826, '上海': 2041...'贵州': 0, '吉林': 0, '新疆': 0, '甘肃': 0, '青海': 0}
#
# # 解析疑似数据
# province_suspect_data = {}
# for item in province_list:
#     if item['name'] not in province_suspect_data:
#         province_suspect_data.update({item['name']: 0})
#     for province_data in item['children']:
#         province_suspect_data[item['name']] += int(province_data['total']['suspect'])
# print(province_suspect_data)
#
# # 解析死亡数据
# province_dead_data = {}
# for item in province_list:
#     if item['name'] not in province_dead_data:
#         province_dead_data.update({item['name']: 0})
#     for province_data in item['children']:
#         province_dead_data[item['name']] += int(province_data['total']['dead'])
# print(province_dead_data)
#
# # 解析治愈数据
# province_heal_data = {}
# for item in province_list:
#     if item['name'] not in province_heal_data:
#         province_heal_data.update({item['name']: 0})
#     for province_data in item['children']:
#         province_heal_data[item['name']] += int(province_data['total']['heal'])
# print(province_heal_data)
#
# # 解析新增确诊数据
# province_newConfirm_data = {}
# for item in province_list:
#     if item['name'] not in province_newConfirm_data:
#         province_newConfirm_data.update({item['name']: 0})
#     for province_data in item['children']:
#         province_newConfirm_data[item['name']] += int(province_data['today']['confirm'])  # today
# print(province_newConfirm_data)
#
# # ------------------------------------------------------------------------------
# # 第二步：存储数据至CSV文件
# # ------------------------------------------------------------------------------
# province_names = list(provnice_confirm_data.keys())  # 省份名称
# province_confirm_list = list(provnice_confirm_data.values())  # 确诊数据
# province_suspect_list = list(province_suspect_data.values())  # 疑似数据(全为0)
# province_dead_list = list(province_dead_data.values())  # 死亡数据
# province_heal_list = list(province_heal_data.values())  # 治愈数据
# province_newConfirm_list = list(province_newConfirm_data.values())  # 新增确诊病例
# print(province_names)
# print(province_confirm_list)
# print(province_suspect_list)
# print(province_dead_list)
# print(province_heal_list)
# print(province_newConfirm_list)
#
# # 获取当前日期命名(2020-02-13-all.csv)
# n = time.strftime("%Y-%m-%d") + "-china.csv"
# fw = open(n, 'w', encoding='utf-8')
# fw.write('province,confirm,dead,heal,new_confirm\n')
# i = 0
# if i >= len(province_names):
#     print("Over write file!")
#     fw.close()
# else:
#     while i < len(province_names):
#         fw.write(province_names[i] + ',' + str(province_confirm_list[i]) + ',' + str(province_dead_list[i]) + ','
#                  + str(province_heal_list[i]) + ',' + str(province_newConfirm_list[i]) + '\n')
#         i = i + 1
