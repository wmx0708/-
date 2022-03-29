import time, json, requests
import pandas as pd

url = 'https://api.inews.qq.com/newsqa/v1/automation/modules/list?modules=FAutoCountryMerge'
get_data=json.dumps(requests.get(url=url).json()['data'])
data = json.loads(get_data)
# print(data)

url_india = 'https://api.inews.qq.com/newsqa/v1/automation/country/daily/list?countrys=%E5%8D%B0%E5%BA%A6'
get_data_india=json.dumps(requests.get(url=url_india).json()['data'])
data_india = json.loads(get_data_india)
print(data_india)

countryList=[]
countryname_list=list(data['FAutoCountryMerge'].keys())
for i in range(len(data['FAutoCountryMerge'])):
    for j in range(len(data['FAutoCountryMerge'][countryname_list[i]]['list'])):
        country_dict = {}
        country_dict['country']=countryname_list[i]
        country_dict['date'] = data['FAutoCountryMerge'][countryname_list[i]]['list'][j]['y'] + "." + \
                                                    data['FAutoCountryMerge'][countryname_list[i]]['list'][j]['date']
        country_dict['confirm'] = data['FAutoCountryMerge'][countryname_list[i]]['list'][j]['confirm']
        countryList.append(country_dict)

for i in range(len(data_india['印度'])):
    india_dict={}
    india_dict['country']='印度'
    india_dict['date']=data_india['印度'][i]['y']+data_india['印度'][i]['date']
    india_dict['confirm']=data_india['印度'][i]['confirm']
    countryList.append(india_dict)

country_frame=pd.DataFrame(countryList)
country_frame.to_excel(time.strftime("%Y-%m-%d")+"-countryList.xlsx",index=False)
