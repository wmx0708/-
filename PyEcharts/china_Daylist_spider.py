import time, json, requests
import demjson
import pandas as pd
import numpy as np

url = 'https://api.inews.qq.com/newsqa/v1/query/inner/publish/modules/list?modules=chinaDayList,chinaDayAddList,nowConfirmStatis,provinceCompare=%d' % int(time.time() * 1000)
get_data=json.dumps(requests.get(url=url).json()['data'])
data = json.loads(get_data)
print(data)

chinaDayList=[]
for i in range(len(data['chinaDayList'])):
    chinaDay_dict={}
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

china_day_frame=pd.DataFrame(chinaDayList)
china_day_frame.to_excel(time.strftime("%Y-%m-%d")+"-china_Day_list.xlsx",index=False)

chinaDayAddList=[]
for i in range(len(data['chinaDayAddList'])):
    chinaDayAdd_dict={}
    chinaDayAdd_dict['date'] = data['chinaDayAddList'][i]['y'] + "."+data['chinaDayAddList'][i]['date']
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

china_dayAdd_frame=pd.DataFrame(chinaDayAddList)
china_dayAdd_frame.to_excel(time.strftime("%Y-%m-%d")+"-china_DayAdd_list.xlsx",index=False)