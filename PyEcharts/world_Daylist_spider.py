import pandas as pd
import time, json, requests

url = 'https://api.inews.qq.com/newsqa/v1/automation/modules/list?modules=FAutoGlobalStatis,' \
      'FAutoGlobalDailyList,FAutoCountryConfirmAdd%d' % int(time.time() * 1000)
get_data=json.dumps(requests.get(url=url).json()['data'])
data = json.loads(get_data)
print(data)

worldDayList=[]
for i in range(len(data['FAutoGlobalDailyList'])):
    worldDay_dict={}
    worldDay_dict['date'] = data['FAutoGlobalDailyList'][i]['y'] + "." + data['FAutoGlobalDailyList'][i]['date']
    worldDay_dict['confirm'] = data['FAutoGlobalDailyList'][i]['all']['confirm']
    worldDay_dict['newAddConfirm'] = data['FAutoGlobalDailyList'][i]['all']['newAddConfirm']
    worldDay_dict['heal'] = data['FAutoGlobalDailyList'][i]['all']['heal']
    worldDay_dict['healRate(%)'] = data['FAutoGlobalDailyList'][i]['all']['healRate']
    worldDay_dict['dead'] = data['FAutoGlobalDailyList'][i]['all']['dead']
    worldDay_dict['deadRate(%)'] = data['FAutoGlobalDailyList'][i]['all']['deadRate']
    worldDayList.append(worldDay_dict)

world_day_frame=pd.DataFrame(worldDayList)
world_day_frame.to_excel(time.strftime("%Y-%m-%d")+"-world_Day_list.xlsx",index=False)